from src.common.base import BaseController
from src.modules.version_info.model.version_info_models import VersionInfoRepository
from src.modules.version_info.view.version_info_module_view import VersionInfoModuleView
from src.core.log import LogSystem
from src.core import DataService


class VersionInfoController(BaseController):
    MODULE_KEY = "VersionInfo"

    def __init__(self):
        super().__init__()
        self._version_repo = VersionInfoRepository()
        DataService.get_instance().register_repository('version_info', self._version_repo)
        self._module_view = None

    def get_module_view(self):
        if not self._module_view:
            self._module_view = VersionInfoModuleView()
        return self._module_view

    def initialize(self) -> bool:
        try:
            LogSystem.instance().info(f"[{self.MODULE_KEY}] 版本信息模块初始化成功")
            return super().initialize()
        except Exception as error:
            LogSystem.instance().error(f"[{self.MODULE_KEY}] 版本信息模块初始化失败: {error}")
            return False
