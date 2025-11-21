from src.common.base import BaseController
from src.modules.tools.model.tool_models import Tool, ToolCategory, ToolType, ToolRepository
from src.modules.tools.model.tool_launcher import ToolLauncher
from src.modules.tools.view.tools_module_view import ToolsModuleView
from src.core.log import LogSystem
from src.core import ConfigSystem, DataService


class ToolsController(BaseController):
    MODULE_KEY = "Tools"

    def __init__(self):
        super().__init__()
        self._tool_launcher = ToolLauncher()
        self._tool_repo = ToolRepository()
        DataService.get_instance().register_repository('tool', self._tool_repo)
        self._module_view = None

    def get_module_view(self):
        if not self._module_view:
            self._module_view = ToolsModuleView()
            self._module_view.tool_launched.connect(self.launch_tool)
            self._module_view.favorite_toggled.connect(self.toggle_favorite)
        return self._module_view

    def initialize(self) -> bool:
        try:
            self._load_tools_from_config()
            LogSystem.instance().info(f"[{self.MODULE_KEY}] 工具模块初始化成功")
            return super().initialize()
        except Exception as error:
            LogSystem.instance().error(f"[{self.MODULE_KEY}] 工具模块初始化失败: {error}")
            return False

    def _load_tools_from_config(self):
        tools_data = ConfigSystem.instance().tools.get_all_tools()
        category_map = {'production_pipeline': ToolCategory.PRODUCTION_PIPELINE,
                        'personal_workspace': ToolCategory.PERSONAL_WORKSPACE,
                        'tool_market': ToolCategory.TOOL_MARKET}
        type_map = {'programming': ToolType.PROGRAMMING, 'planning': ToolType.PLANNING,
                    'art': ToolType.ART, 'operations': ToolType.OPERATIONS, 'common': ToolType.COMMON}
        repository = DataService.get_instance().tool_repository

        for tool_data in tools_data:
            if not tool_data.get('enabled', True):
                continue
            tool = Tool(id=tool_data['id'], name=tool_data['name'], description=tool_data['description'],
                       category=category_map.get(tool_data['category'], ToolCategory.PRODUCTION_PIPELINE),
                       tool_type=type_map.get(tool_data['tool_type'], ToolType.COMMON),
                       icon_path=tool_data.get('icon', ''), executable_path=tool_data['executable_path'])
            repository.add_tool(tool)
        repository._load_favorites()

    def get_tools_by_category(self, category_key: str):
        category_map = {"production_pipeline": ToolCategory.PRODUCTION_PIPELINE,
                        "personal_workspace": ToolCategory.PERSONAL_WORKSPACE,
                        "tool_market": ToolCategory.TOOL_MARKET}
        category = category_map.get(category_key)
        if category:
            return DataService.get_instance().tool_repository.get_tools_by_category(category)
        return []

    def launch_tool(self, tool_id: str) -> bool:
        try:
            repository = DataService.get_instance().tool_repository
            tool = repository.get_tool(tool_id)
            if not tool:
                LogSystem.instance().error(f"[{self.MODULE_KEY}] 未找到工具: {tool_id}")
                return False
            repository.add_to_recent(tool_id)
            success = self._tool_launcher.launch_tool(tool)
            if success:
                LogSystem.instance().info(f"[{self.MODULE_KEY}] 成功启动工具: {tool.name}")
                if self._module_view:
                    self._module_view.refresh_tools()
            else:
                LogSystem.instance().error(f"[{self.MODULE_KEY}] 启动工具失败: {tool.name}")
            return success
        except Exception as error:
            LogSystem.instance().error(f"[{self.MODULE_KEY}] 启动工具失败: {error}")
            return False

    def toggle_favorite(self, tool_id: str):
        try:
            repository = DataService.get_instance().tool_repository
            tool = repository.get_tool(tool_id)
            if not tool:
                return
            if tool.is_favorite:
                repository.remove_from_favorites(tool_id)
                LogSystem.instance().info(f"[{self.MODULE_KEY}] 已从收藏中移除")
            else:
                repository.add_to_favorites(tool_id)
                LogSystem.instance().info(f"[{self.MODULE_KEY}] 已添加到收藏")
            if self._module_view:
                self._module_view.refresh_tools()
        except Exception as error:
            LogSystem.instance().error(f"[{self.MODULE_KEY}] 切换收藏失败: {error}")
