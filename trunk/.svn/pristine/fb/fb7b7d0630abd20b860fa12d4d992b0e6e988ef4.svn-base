from PyQt5.QtCore import QTimer

from src.common.base import BaseController
from src.core.log import LogSystem
from src.core.event import EventSystem
from src.modules.project.controller.project_async_download_logic import ProjectAsyncDownloadLogic
from src.modules.project.controller.project_events import ProjectEvents
from src.modules.project.controller.project_tools_logic import ProjectToolsLogic
from src.modules.project.view.project_module_view import ProjectModuleView
from typing import Dict, Optional


class ProjectController(BaseController):
    MODULE_KEY = "Project"

    def __init__(self):
        super().__init__()
        self._module_view = None
        self.tools_logic = ProjectToolsLogic(self)
        self.async_download_logic = ProjectAsyncDownloadLogic(self)
        self._register_events()

    def get_module_view(self):
        if not self._module_view:
            self._module_view = ProjectModuleView()
        return self._module_view

    def initialize(self) -> bool:
        try:
            LogSystem.instance().info(f"[{self.MODULE_KEY}] 项目模块初始化成功")
            return super().initialize()
        except Exception as error:
            LogSystem.instance().error(f"[{self.MODULE_KEY}] 项目模块初始化失败: {error}")
            return False

    def _register_events(self):
        event_system = EventSystem.instance()
        event_system.register_event(ProjectEvents.TOOLS_INSTALL_CLICK, self.async_download_logic.on_install_dev_tools)
        event_system.register_event(ProjectEvents.DOWNLOAD_TOOLS_ERROR, self.async_download_logic.on_download_tools_error)
        event_system.register_event(ProjectEvents.CHECK_TOOLS_VERSION_START, self.tools_logic.check_tools_version)
        self.get_module_view().tools_download_complete.connect(self.async_download_logic.on_tools_download_complete)
