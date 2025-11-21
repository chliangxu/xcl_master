from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QStackedWidget
from PyQt5.QtCore import Qt
from .group_users_panel import GroupUsersPanel
from .group_permissions_panel import GroupPermissionsPanel


class GroupDetailPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_group_id = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.detail_stacked = QStackedWidget()
        detail_content = self._create_detail_content()
        loading_widget = self._create_loading_widget()

        self.detail_stacked.addWidget(detail_content)
        self.detail_stacked.addWidget(loading_widget)
        self.detail_stacked.setCurrentWidget(detail_content)

        layout.addWidget(self.detail_stacked)

    def _create_detail_content(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.group_detail_label = QLabel("选择一个用户组查看详情")
        layout.addWidget(self.group_detail_label)

        tabs = QTabWidget()

        self.users_panel = GroupUsersPanel()
        tabs.addTab(self.users_panel, "组内用户")

        self.permissions_panel = GroupPermissionsPanel()
        tabs.addTab(self.permissions_panel, "组权限")

        layout.addWidget(tabs)
        return widget

    def _create_loading_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        label = QLabel("加载中...")
        label.setStyleSheet("font-size: 14px; color: #666;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return widget

    def set_current_group_id(self, group_id: int):
        self.current_group_id = group_id
        self.users_panel.set_current_group_id(group_id)
        self.permissions_panel.set_current_group_id(group_id)

    def show_loading(self):
        self.detail_stacked.setCurrentIndex(1)

    def hide_loading(self):
        self.detail_stacked.setCurrentIndex(0)

    def display_group_detail(self, group_name: str):
        self.group_detail_label.setText(f"用户组: {group_name}")

    def display_group_users(self, users):
        self.users_panel.display_group_users(users)

    def render_group_permissions(self, all_modules, selected_module_keys):
        self.permissions_panel.render_group_permissions(all_modules, selected_module_keys)
