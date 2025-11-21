from typing import Dict, List, Optional, Type
from dataclasses import dataclass


@dataclass
class ModuleMetadata:
    module_key: str
    name: str
    icon: str
    order: int = 999
    visible: bool = True
    controller_class: Type = None


class ModuleManager:
    _instance = None
    _modules: Dict[str, ModuleMetadata] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, module_key: str, name: str, icon: str,
                 controller_class: Type, order: int = 999, visible: bool = True):
        instance = cls()
        instance._modules[module_key] = ModuleMetadata(
            module_key=module_key,
            name=name,
            icon=icon,
            order=order,
            visible=visible,
            controller_class=controller_class
        )

    @classmethod
    def get_module(cls, module_key: str) -> Optional[ModuleMetadata]:
        instance = cls()
        return instance._modules.get(module_key)

    @classmethod
    def get_all_modules(cls) -> List[ModuleMetadata]:
        instance = cls()
        return sorted(instance._modules.values(), key=lambda m: m.order)

    @classmethod
    def get_visible_modules(cls) -> List[ModuleMetadata]:
        return [m for m in cls.get_all_modules() if m.visible]

    @classmethod
    def clear(cls):
        instance = cls()
        instance._modules.clear()
