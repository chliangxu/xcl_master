from src.common.base import BaseController
from src.modules.task.view.task_bug_view import TaskBugView
from src.modules.task.model.task_tapd_model import TaskTapdModel, TAPD_WEB_URL
from src.modules.login.model.user_models import UserModel
from src.core.log import LogSystem
import webbrowser


class TaskController(BaseController):
    MODULE_KEY = "Task"

    def __init__(self):
        super().__init__()
        self._module_view = None
        self._tapd_model = None
        self._user_model = UserModel.get_instance()

    def get_module_view(self):
        if not self._module_view:
            self._module_view = TaskBugView()
            self._module_view.tapd_button_clicked.connect(self._open_tapd)

            if self._tapd_model:
                self._load_tapd_data()

        return self._module_view

    def initialize(self) -> bool:
        try:
            self._tapd_model = TaskTapdModel()
            LogSystem.instance().info(f"[{self.MODULE_KEY}] 任务模块初始化成功")
            return super().initialize()
        except Exception as error:
            LogSystem.instance().error(f"[{self.MODULE_KEY}] 任务模块初始化失败: {error}")
            return False

    def _get_current_username(self) -> str:
        # 测试用
        return "v_jcjccchen"
        current_user = self._user_model.get_current_user()
        if current_user:
            return current_user.id
        return ""

    def _load_tapd_data(self):
        try:
            if not self._tapd_model:
                self._tapd_model = TaskTapdModel()

            username = self._get_current_username()
            need_count = self._tapd_model.get_need_data_count(username)
            bug_count = self._tapd_model.get_bug_data_count(username)

            self._module_view.set_need_count(need_count)
            self._module_view.set_bug_count(bug_count)
        except Exception as e:
            print(f"加载TAPD数据失败: {e}")
            self._module_view.show_error("加载失败")

    def _open_tapd(self):
        print("执行跳转TAPD操作...")
        webbrowser.open(TAPD_WEB_URL)
