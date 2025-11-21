from abc import ABC, abstractmethod
from typing import Dict, Any


class BasePlugin(ABC):
    def __init__(self, plugin_name: str):
        self._plugin_name = plugin_name
        self._is_loaded = False

    @property
    def plugin_name(self) -> str:
        return self._plugin_name

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    @abstractmethod
    def load(self) -> bool:
        pass

    @abstractmethod
    def unload(self) -> bool:
        pass

    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        pass
