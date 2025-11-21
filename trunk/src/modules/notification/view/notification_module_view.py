from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QCheckBox
from PyQt5 import uic
from src.common.base import BaseWidget
from PyQt5.QtCore import Qt
from src.common.utils import ResourceUtils


class NotificationModuleView(BaseWidget):
    def init_ui(self):
        uic.loadUi(ResourceUtils.get_ui_path(__file__, "notification.ui"), self)

        # 获取UI文件中的tabWidget
        self.tab_widget = self.findChild(QTabWidget, "tabWidget")

        if self.tab_widget:
            # 如果找到了tabWidget，设置布局
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.tab_widget)

            # 获取UI文件中的复选框并连接信号（如果需要）
            self.setup_checkboxes()
        else:
            print("警告：未找到tabWidget，但UI文件应该已加载")

    def setup_checkboxes(self):
        """设置UI文件中复选框的信号连接"""
        try:
            # 获取UI文件中的复选框
            version_checkbox = self.findChild(QCheckBox, "versionCheckBox")
            error_checkbox = self.findChild(QCheckBox, "ErrorCheckBox")
            release_checkbox = self.findChild(QCheckBox, "releaseCheckBox")

            # 连接信号（根据你的需求添加）
            if version_checkbox:
                version_checkbox.stateChanged.connect(self.on_version_notification_changed)
            if error_checkbox:
                error_checkbox.stateChanged.connect(self.on_error_notification_changed)
            if release_checkbox:
                release_checkbox.stateChanged.connect(self.on_hotfix_notification_changed)

        except Exception as e:
            print(f"设置复选框时出错: {e}")

    def on_version_notification_changed(self, state):
        """版本通知复选框状态改变"""
        checked = state == Qt.Checked
        print(f"版本通知: {'开启' if checked else '关闭'}")

    def on_error_notification_changed(self, state):
        """构建报错通知复选框状态改变"""
        checked = state == Qt.Checked
        print(f"构建报错通知: {'开启' if checked else '关闭'}")

    def on_hotfix_notification_changed(self, state):
        """热更发布通知复选框状态改变"""
        checked = state == Qt.Checked
        print(f"热更发布通知: {'开启' if checked else '关闭'}")

    def apply_styles(self):
        cfg = self.cfg()

        self.setStyleSheet(f"""
            NotificationModuleView {{
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