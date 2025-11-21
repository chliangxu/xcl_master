from src.common.base import BaseController
from src.modules.login.model.user_models import UserModel, User, UserRole
from src.core.event import Events, EventSystem
from src.core.log import LogSystem
from src.core import ConfigSystem, DataService


class LoginController(BaseController):
    MODULE_KEY = "Login"

    def __init__(self):
        super().__init__()
        self.user_model = UserModel.get_instance()
        DataService.get_instance().register_repository('user', self.user_model)
        self._register_events()

    def _register_events(self):
        EventSystem.instance().register_event(Events.USER_PROFILE_UPDATED, self._on_profile_updated)

    def initialize(self) -> bool:
        try:
            current_user = self.user_model.get_current_user()
            if not current_user:
                config = ConfigSystem.instance()
                saved_name = config.user.user_name
                saved_role_str = config.user.user_role

                role_map = {
                    "策划": UserRole.PLANNER,
                    "客户端程序": UserRole.CLIENT_PROGRAMMER,
                    "服务器程序": UserRole.SERVER_PROGRAMMER,
                    "美术": UserRole.ARTIST,
                    "运营": UserRole.OPERATIONS
                }
                role = role_map.get(saved_role_str, UserRole.CLIENT_PROGRAMMER)

                default_user = User(
                    id=saved_name,
                    name=saved_name,
                    role=role,
                    avatar_path="",
                    preferences={}
                )
                self.user_model.add_user(default_user)
                self.user_model.set_current_user(default_user)

            LogSystem.instance().info(f"[{self.MODULE_KEY}] 登录模块初始化成功")
            return super().initialize()
        except Exception as error:
            LogSystem.instance().error(f"[{self.MODULE_KEY}] 登录模块初始化失败: {error}")
            return False

    def _on_profile_updated(self, profile_data: dict):
        role_map = {
            "策划": UserRole.PLANNER,
            "客户端程序": UserRole.CLIENT_PROGRAMMER,
            "服务器程序": UserRole.SERVER_PROGRAMMER,
            "美术": UserRole.ARTIST,
            "运营": UserRole.OPERATIONS
        }

        current_user = self.user_model.get_current_user()
        if current_user:
            new_name = profile_data.get('name')
            role_text = profile_data.get('role')
            changed = False

            if new_name and new_name != current_user.name:
                current_user.id = new_name
                current_user.name = new_name
                changed = True

            if role_text and role_text in role_map and current_user.role != role_map[role_text]:
                current_user.role = role_map[role_text]
                changed = True

            if changed:
                from src.core.event import EventSystem
                self.user_model.update_user(current_user)
                ConfigSystem.instance().user.save_user_info(current_user.name, current_user.role.value)
                EventSystem.instance().send_event(Events.USER_INFO_CHANGED, current_user)
                LogSystem.instance().info(f"用户信息已更新: {current_user.name} - {current_user.role.value}")
