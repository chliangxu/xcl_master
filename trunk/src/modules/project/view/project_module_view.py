import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QCheckBox
from PyQt5 import uic
from src.common.base import BaseWidget
from PyQt5.QtCore import Qt

from src.core import EventSystem
from src.modules.project.controller.project_events import ProjectEvents
from src.modules.project.controller.project_macros import ProjectMacros
from src.modules.project.view.project_config_widget import ProjectConfigWidget
from src.modules.project.view.project_install_widget import ProjectInstallWidget


class ProjectModuleView(BaseWidget):
    check_tools_version_trigger = pyqtSignal()
    tools_download_complete = pyqtSignal(int, str)
    
    def __init__(self, parent=None):
        self.project_config_widget = None
        self.tab_widget = None
        self.project_install_widget = None
        super().__init__(parent)

    def init_ui(self):
        # 加载UI文件
        ui_file_path = os.path.join(os.path.dirname(__file__), 'project.ui')
        if not os.path.exists(ui_file_path):
            raise FileNotFoundError(f"UI文件不存在: {ui_file_path}")
        uic.loadUi(ui_file_path, self)  # UI文件路径

        # 获取UI文件中的tabWidget
        self.tab_widget = self.findChild(QTabWidget, "tabWidget")

        if self.tab_widget:
            # 如果找到了tabWidget，设置布局
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.tab_widget)

            # 初始化各个选项卡的内容
            self.setup_install_tab()
            self.setup_config_tab()
            self.setup_pull_tab()
            self.setup_info_tab()
        else:
            print("警告：未找到tabWidget，但UI文件应该已加载")

    def setup_install_tab(self):
        """初始化工具安装选项卡"""
        install_tab = self.findChild(QWidget, "installTab")
        if install_tab:
            self.project_install_widget = ProjectInstallWidget(self)
            install_layout = QVBoxLayout(install_tab)
            install_layout.addWidget(self.project_install_widget)
            EventSystem.instance().send_event(ProjectEvents.CHECK_TOOLS_VERSION_START)
            # 这里可以添加更多的工具安装相关控件

    def setup_config_tab(self):
        """初始化工程配置选项卡"""
        config_tab = self.findChild(QWidget, "configurationTab")
        if config_tab:
            self.project_config_widget = ProjectConfigWidget(self)
            config_layout = QVBoxLayout(config_tab)
            config_layout.addWidget(self.project_config_widget)
            # 这里可以添加更多的工程配置相关控件

    def setup_pull_tab(self):
        """初始化工程拉取选项卡"""
        pull_tab = self.findChild(QWidget, "pullTab")
        if pull_tab:
            pull_layout = QVBoxLayout(pull_tab)
            # 这里可以添加更多的工程拉取相关控件

    def setup_info_tab(self):
        """初始化工程信息选项卡"""
        info_tab = self.findChild(QWidget, "infoLab")
        if info_tab:
            info_layout = QVBoxLayout(info_tab)
            # 这里可以添加更多的工程信息相关控件
        
    def apply_styles(self):
        cfg = self.cfg()

        self.setStyleSheet(f"""
            ProjectModuleView {{
                background-color: {cfg.colors.background};
            }}
            QTabWidget::pane {{
                border: 1px solid {self.get_border_color()};
                background-color: {cfg.colors.background};
            }}
            QTabBar::tab {{
                background-color: {cfg.colors.surface};
                color: {cfg.colors.text_secondary};
                padding: 10px 20px;
                margin-right: 2px;
                border: 1px solid {self.get_border_color()};
                border-bottom: none;
            }}
            QTabBar::tab:selected {{
                background-color: {cfg.colors.background};
                color: {self.get_primary_color()};
                border-bottom: 2px solid {self.get_primary_color()};
            }}
            QTabBar::tab:hover {{
                background-color: {cfg.colors.surface_hover};
            }}
        """)
