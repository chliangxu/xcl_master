from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from src.common.base import BaseWidget
from src.modules.main.view.sidebar_widget import SidebarWidget
from src.modules.main.view.header_widget import HeaderWidget
from src.modules.main.view.module_container_widget import ModuleContainerWidget
from src.modules.main.view.status_bar import StatusBar
from src.modules.login.view import UserProfileWidget
from src.core import ConfigSystem
from src.core.event import EventSystem, Events


class MainWindow(QMainWindow):
    category_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.config = ConfigSystem.instance()
        self.init_ui()
        self.setup_connections()

    def init_ui(self):
        cfg = self.config

        self.setWindowTitle(cfg.app.title)
        self.setMinimumSize(cfg.window.min_width, cfg.window.min_height)
        self.resize(cfg.window.width, cfg.window.height)

        if cfg.window.maximized:
            self.showMaximized()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.header = HeaderWidget()
        main_layout.addWidget(self.header)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.sidebar = SidebarWidget()
        self.sidebar.setFixedWidth(cfg.layout.sidebar_width)
        content_layout.addWidget(self.sidebar)

        self.content_area = ModuleContainerWidget()
        content_layout.addWidget(self.content_area)

        content_widget = QWidget()
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)

        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)

        self.user_profile = UserProfileWidget()
        self.user_profile.hide()

        self.apply_styles()

    def setup_connections(self):
        self.header.user_profile_clicked.connect(self.show_user_profile)
        self.sidebar.category_changed.connect(self.category_changed.emit)
        EventSystem.instance().register_event(Events.USER_INFO_CHANGED, self._on_user_info_changed)

    def apply_styles(self):
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {BaseWidget.get_background_color()};
                color: {BaseWidget.get_text_color()};
            }}
        """)

    def show_user_profile(self):
        self.user_profile.show()
        self.user_profile.raise_()

    def update_content(self, module_view):
        self.content_area.set_module_view(module_view.__class__.__name__, module_view)

    def set_active_category(self, category_key: str):
        self.sidebar.set_active_category(category_key)

    def _on_user_info_changed(self, user):
        self.header.update_user_display()

    def show_status(self, message: str, timeout: int = 0):
        self.status_bar.show_message(message, timeout)

    def clear_status(self):
        self.status_bar.clear()

    def closeEvent(self, event):
        self.config.window.save_state(
            self.width(),
            self.height(),
            self.isMaximized()
        )
        super().closeEvent(event)
