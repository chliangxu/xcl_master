from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PyQt5.QtCore import Qt
from .group_list_panel import GroupListPanel
from .group_detail_panel import GroupDetailPanel


class GroupManageTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_group_id = None
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Horizontal)

        self.list_panel = GroupListPanel()
        splitter.addWidget(self.list_panel)

        self.detail_panel = GroupDetailPanel()
        splitter.addWidget(self.detail_panel)

        splitter.setSizes([320, 700])
        layout.addWidget(splitter)

    def set_current_group_id(self, group_id: int):
        self.current_group_id = group_id
        self.detail_panel.set_current_group_id(group_id)

    def display_groups(self, groups):
        self.list_panel.display_groups(groups)

    def show_detail_loading(self):
        self.detail_panel.show_loading()

    def hide_detail_loading(self):
        self.detail_panel.hide_loading()

    def display_group_detail(self, group_name: str):
        self.detail_panel.display_group_detail(group_name)

    def display_group_users(self, users):
        self.detail_panel.display_group_users(users)

    def render_group_permissions(self, all_modules, selected_module_keys):
        self.detail_panel.render_group_permissions(all_modules, selected_module_keys)

    def show_user_selection_dialog(self, available_users: list):
        self.detail_panel.users_panel.show_user_selection_dialog(available_users)
