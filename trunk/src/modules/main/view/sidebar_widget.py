from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QButtonGroup, QSpacerItem, QSizePolicy, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from src.common.base import BaseWidget
from src.core import ModuleManager


class SidebarWidget(BaseWidget):
    category_changed = pyqtSignal(str)

    def init_ui(self):
        cfg = self.cfg()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.button_group = QButtonGroup()
        self.category_buttons = {}

        modules = ModuleManager.get_visible_modules()

        for i, module in enumerate(modules):
            btn = QPushButton(f"  {module.icon}  {module.name}")
            btn.setCheckable(True)
            btn.setProperty("module_key", module.module_key)
            btn.clicked.connect(lambda checked, k=module.module_key: self.category_changed.emit(k))
            btn.setFont(self.get_default_font(cfg.fonts.size_default))
            self.button_group.addButton(btn, i)
            main_layout.addWidget(btn)
            self.category_buttons[module.module_key] = btn

            if i == 0:
                btn.setChecked(True)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def update_module_visibility(self, module_permissions):
        first_visible_key = None

        for module_key, btn in self.category_buttons.items():
            has_permission = module_permissions.get(module_key, True)
            btn.setVisible(has_permission)

            if has_permission and first_visible_key is None:
                first_visible_key = module_key

        if first_visible_key and not any(btn.isChecked() and btn.isVisible()
                                         for btn in self.category_buttons.values()):
            self.category_buttons[first_visible_key].setChecked(True)
            self.category_changed.emit(first_visible_key)

    def set_active_category(self, module_key: str):
        if module_key in self.category_buttons:
            self.category_buttons[module_key].setChecked(True)

    def apply_styles(self):
        cfg = self.cfg()

        self.setStyleSheet(f"""
            SidebarWidget {{
                background-color: {self.get_secondary_background()};
                border-right: {cfg.styles.border_width}px solid {self.get_border_color()};
            }}
            QPushButton {{
                background-color: {cfg.colors.transparent};
                border: none;
                color: {self.get_secondary_text_color()};
                font-size: {cfg.fonts.size_default}px;
                font-weight: bold;
                padding: 15px 20px;
                text-align: left;
                border-radius: {cfg.styles.border_radius_small}px;
                margin: 3px 10px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background-color: {cfg.colors.dark_gray};
                color: {self.get_text_color()};
            }}
            QPushButton:checked {{
                background-color: {self.get_primary_color()};
                color: {cfg.colors.black};
            }}
            QPushButton:checked:hover {{
                background-color: {cfg.colors.primary_active};
            }}
        """)
