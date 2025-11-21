from src.modules.main.view.main_window import MainWindow
from src.core import DataService, ModuleManager
from src.core.log import LogSystem
from src.core.event import EventSystem
from src.common.base import BaseController
from src.core.event import Events
from src.modules.login.model.user_models import User
from src.core.module.module_config import register_all_modules
from src.core.services.permission_service import PermissionService


class MainController(BaseController):
    def __init__(self):
        super().__init__()

        register_all_modules()

        self.window = MainWindow()
        self._modules = {}
        self._init_modules()
        self._register_events()
        self._initialize()

    def _init_modules(self):
        for module_meta in ModuleManager.get_all_modules():
            module = module_meta.controller_class()
            self._modules[module_meta.module_key] = module

    def _register_events(self):
        event_system = EventSystem.instance()
        event_system.register_event(Events.USER_INFO_CHANGED, self._on_user_permission_changed)
        event_system.register_event(Events.STATUS_BAR, self._on_status_bar)

        self.window.category_changed.connect(self._on_category_changed)
        self.window.user_profile.profile_updated.connect(
            lambda data: EventSystem.instance().send_event(Events.USER_PROFILE_UPDATED, data))

    def _initialize(self):
        for module in self._modules.values():
            if not module.initialize():
                module_name = module.MODULE_KEY if module.MODULE_KEY else module.name
                LogSystem.instance().error(f"{module_name} 初始化失败")
                return False

        # 直接从DataService获取当前用户
        user_repo = DataService.get_instance().user_repository
        if user_repo:
            current_user = user_repo.get_current_user()
            if current_user:
                self.window.header.update_user_display()
                # 加载当前用户权限
                permission_service = PermissionService.get_instance()
                permission_service.load_current_user_permissions()
                self._update_sidebar_visibility()

    def _on_category_changed(self, module_key: str):
        module = self._modules.get(module_key)
        if module:
            module_view = module.get_module_view()
            if module_view:
                self.window.update_content(module_view)
                LogSystem.instance().info(f"切换到模块: {module_key}")

    def _on_user_permission_changed(self, user):
        self._update_sidebar_visibility()
        LogSystem.instance().info(f"已更新侧边栏模块显示: {user.name}")

    def _update_sidebar_visibility(self):
        permission_service = PermissionService.get_instance()

        module_permissions = {}
        for module_key in self.window.sidebar.category_buttons.keys():
            has_permission = permission_service.has_module_permission(module_key)
            module_permissions[module_key] = has_permission

        self.window.sidebar.update_module_visibility(module_permissions)

    def _on_status_bar(self, data):
        if data is None or (isinstance(data, dict) and data.get("clear")):
            self.window.clear_status()
        else:
            message = data if isinstance(data, str) else data.get("message", "")
            timeout = 0 if isinstance(data, str) else data.get("timeout", 0)
            self.window.show_status(message, timeout)

    def show(self):
        if self.window:
            self.window.show()
