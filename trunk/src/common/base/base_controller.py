from typing import Optional
from PyQt5.QtCore import QObject


class BaseController(QObject):

    MODULE_KEY: str = None

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @property
    def name(self) -> str:
        class_name = self.__class__.__name__
        return class_name.replace('Logic', '').replace('Controller', '').lower()

    def get_module_view(self):
        """获取模块视图，子类必须重写"""
        return None

    def initialize(self) -> bool:
        """初始化模块，子类重写"""
        self._initialized = True
        return True
