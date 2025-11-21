from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
from src.core import ConfigSystem


class ToolCategory(Enum):
    PRODUCTION_PIPELINE = "制作管线"
    PERSONAL_WORKSPACE = "个人工作区"
    TOOL_MARKET = "工具市场"


class ToolType(Enum):
    PLANNING = "策划工具"
    PROGRAMMING = "程序工具"
    ART = "美术工具"
    OPERATIONS = "运营工具"
    COMMON = "通用工具"


@dataclass
class Tool:
    id: str
    name: str
    description: str
    category: ToolCategory
    tool_type: ToolType
    icon_path: str
    executable_path: str
    version: str = "1.0.0"
    usage_count: int = 0
    is_favorite: bool = False
    config: Dict[str, Any] = None

    def __post_init__(self):
        if self.config is None:
            self.config = {}


class ToolRepository:
    def __init__(self):
        self._tools = {}
        self._categories = {category: [] for category in ToolCategory}
        self._favorites = []
        self._recent_tools = []
        self._config = None

    def _load_favorites(self):
        self._config = ConfigSystem.instance()
        if self._config:
            saved_favorites = self._config.favorites.get_favorites()
            self._favorites.clear()
            for tool_id in saved_favorites:
                if tool_id in self._tools:
                    self._favorites.append(tool_id)
                    self._tools[tool_id].is_favorite = True

    def _save_favorites(self):
        if self._config:
            self._config.favorites.save_favorites(self._favorites)

    def add_tool(self, tool: Tool):
        self._tools[tool.id] = tool
        self._categories[tool.category].append(tool.id)

    def get_tool(self, tool_id: str) -> Optional[Tool]:
        return self._tools.get(tool_id)

    def get_tools_by_category(self, category: ToolCategory) -> List[Tool]:
        tool_ids = self._categories.get(category, [])
        return [self._tools[tool_id] for tool_id in tool_ids if tool_id in self._tools]

    def get_tools_by_type(self, tool_type: ToolType) -> List[Tool]:
        return [tool for tool in self._tools.values() if tool.tool_type == tool_type]

    def add_to_favorites(self, tool_id: str):
        if tool_id in self._tools and tool_id not in self._favorites:
            self._favorites.append(tool_id)
            self._tools[tool_id].is_favorite = True
            self._save_favorites()

    def remove_from_favorites(self, tool_id: str):
        if tool_id in self._favorites:
            self._favorites.remove(tool_id)
            if tool_id in self._tools:
                self._tools[tool_id].is_favorite = False
            self._save_favorites()

    def get_favorites(self) -> List[Tool]:
        return [self._tools[tool_id] for tool_id in self._favorites if tool_id in self._tools]

    def add_to_recent(self, tool_id: str):
        if tool_id in self._tools:
            if tool_id in self._recent_tools:
                self._recent_tools.remove(tool_id)
            self._recent_tools.insert(0, tool_id)
            self._recent_tools = self._recent_tools[:10]
            self._tools[tool_id].usage_count += 1

    def get_recent_tools(self) -> List[Tool]:
        return [self._tools[tool_id] for tool_id in self._recent_tools if tool_id in self._tools]
