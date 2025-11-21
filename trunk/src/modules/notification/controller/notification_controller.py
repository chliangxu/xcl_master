from src.common.base import BaseController
from src.modules.notification.view.notification_module_view import NotificationModuleView
from src.core.log import LogSystem


class NotificationController(BaseController):
    MODULE_KEY = "Notification"
    
    def __init__(self):
        super().__init__()
        self._module_view = None

    def get_module_view(self):
        if not self._module_view:
            self._module_view = NotificationModuleView()
        return self._module_view

    def initialize(self) -> bool:
        try:
            LogSystem.instance().info(f"[{self.MODULE_KEY}] 通知模块初始化成功")
            return super().initialize()
        except Exception as error:
            LogSystem.instance().error(f"[{self.MODULE_KEY}] 通知模块初始化失败: {error}")
            return False
