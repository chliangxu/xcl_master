from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from PyQt5.QtCore import Qt
from src.common.base import BaseWidget


class ModuleContainerWidget(BaseWidget):
    def __init__(self):
        super().__init__()
        self._module_widgets = {}

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

    def set_module_view(self, module_key: str, module_view: QWidget):
        if module_key not in self._module_widgets:
            self._module_widgets[module_key] = module_view
            self.stacked_widget.addWidget(module_view)

        widget = self._module_widgets[module_key]
        self.stacked_widget.setCurrentWidget(widget)

    def apply_styles(self):
        cfg = self.cfg()

        self.setStyleSheet(f"""
            ModuleContainerWidget {{
                background-color: {cfg.colors.background};
            }}
        """)
