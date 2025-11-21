from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFont
from src.core import ConfigSystem


class BaseWidget(QWidget):
    _config = None

    def __init__(self, parent=None):
        super().__init__(parent)
        if BaseWidget._config is None:
            BaseWidget._config = ConfigSystem.instance()
        self.init_ui()
        self.apply_styles()

    def init_ui(self) -> None:
        pass

    def setup_ui(self) -> None:
        self.init_ui()

    def apply_styles(self) -> None:
        pass

    @classmethod
    def cfg(cls):
        if cls._config is None:
            cls._config = ConfigSystem.instance()
        return cls._config

    @classmethod
    def get_color(cls, name: str) -> str:
        colors = cls.cfg().colors
        return getattr(colors, name, '#ffffff')

    @classmethod
    def get_background_color(cls) -> str:
        return cls.cfg().colors.background

    @classmethod
    def get_secondary_background(cls) -> str:
        return cls.cfg().colors.background_secondary

    @classmethod
    def get_text_color(cls) -> str:
        return cls.cfg().colors.text

    @classmethod
    def get_secondary_text_color(cls) -> str:
        return cls.cfg().colors.text_secondary

    @classmethod
    def get_primary_color(cls) -> str:
        return cls.cfg().colors.primary

    @classmethod
    def get_border_color(cls) -> str:
        return cls.cfg().colors.border

    @classmethod
    def get_disabled_text_color(cls) -> str:
        return cls.cfg().colors.text_disabled

    @classmethod
    def get_default_font(cls, size: int = None, bold: bool = False) -> QFont:
        cfg = cls.cfg()
        if size is None:
            size = cfg.fonts.size_default
        font = QFont(cfg.fonts.family, size)
        font.setBold(bold)
        return font

    @classmethod
    def get_title_font(cls, size: int = None) -> QFont:
        cfg = cls.cfg()
        if size is None:
            size = cfg.fonts.size_large
        font = QFont(cfg.fonts.family, size)
        font.setBold(True)
        return font

    @classmethod
    def get_button_style(cls, button_type: str = 'primary') -> str:
        cfg = cls.cfg()

        if button_type == 'primary':
            return f"""
                QPushButton {{
                    background-color: {cfg.colors.primary};
                    border: none;
                    border-radius: 6px;
                    color: {cfg.colors.black};
                    padding: 8px 16px;
                }}
                QPushButton:hover {{
                    background-color: {cfg.colors.primary_hover};
                }}
                QPushButton:pressed {{
                    background-color: {cfg.colors.primary_active};
                }}
            """
        elif button_type == 'secondary':
            return f"""
                QPushButton {{
                    background-color: {cfg.colors.background_secondary};
                    border: 1px solid {cfg.colors.border};
                    border-radius: 6px;
                    color: {cfg.colors.text};
                    padding: 8px 16px;
                }}
                QPushButton:hover {{
                    background-color: {cfg.colors.surface_hover};
                    border-color: {cfg.colors.primary};
                }}
            """
        return ""

    @classmethod
    def get_scrollbar_style(cls) -> str:
        cfg = cls.cfg()

        return f"""
            QScrollBar:vertical {{
                background-color: {cfg.colors.background};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {cfg.colors.border};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {cfg.colors.surface_hover};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar:horizontal {{
                background-color: {cfg.colors.background};
                height: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {cfg.colors.border};
                border-radius: 6px;
                min-width: 20px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {cfg.colors.surface_hover};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """

    def set_loading(self, loading: bool) -> None:
        self.setEnabled(not loading)
