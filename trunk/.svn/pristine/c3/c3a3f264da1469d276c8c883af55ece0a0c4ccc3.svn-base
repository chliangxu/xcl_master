from typing import Dict, Optional
from src.core.plugin.base_plugin import BasePlugin


class PluginManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._plugins: Dict[str, BasePlugin] = {}

    @classmethod
    def instance(cls):
        return cls()

    def register_plugin(self, plugin: BasePlugin):
        self._plugins[plugin.plugin_name] = plugin

    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        return self._plugins.get(plugin_name)

    def load_all_plugins(self):
        for plugin in self._plugins.values():
            plugin.load()

    def unload_all_plugins(self):
        for plugin in self._plugins.values():
            plugin.unload()
