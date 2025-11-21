from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from src.core.event import EventSystem
from ..controller.permission_events import PermissionEvents


class CurrentUserTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        self.user_info_label = QLabel("用户: 未登录")
        layout.addWidget(self.user_info_label)

        self.groups_label = QLabel("所属用户组: 无")
        layout.addWidget(self.groups_label)

        refresh_btn = QPushButton("刷新权限")
        refresh_btn.clicked.connect(self._on_refresh_clicked)
        layout.addWidget(refresh_btn)

        self.permission_tree = QTreeWidget()
        self.permission_tree.setHeaderLabels(["模块", "权限"])
        self.permission_tree.setColumnWidth(0, 300)
        layout.addWidget(self.permission_tree)

    def _on_refresh_clicked(self):
        EventSystem.instance().send_event(PermissionEvents.PERMISSION_CHANGED)

    def display_user_info(self, user_id: str, groups: list):
        self.user_info_label.setText(f"用户: {user_id}")
        groups_text = ", ".join(groups) if groups else "无"
        self.groups_label.setText(f"所属用户组: {groups_text}")

    def display_permissions(self, all_modules, user_permissions):
        self.permission_tree.clear()
        permission_set = set(user_permissions)

        for module in all_modules:
            parent_item = QTreeWidgetItem(self.permission_tree)
            parent_item.setText(0, module.module_name)
            has_permission = module.module_key in permission_set
            parent_item.setText(1, "✓" if has_permission else "✗")

            for child in module.children:
                child_item = QTreeWidgetItem(parent_item)
                child_item.setText(0, child.module_name)
                child_has_permission = child.module_key in permission_set
                child_item.setText(1, "✓" if child_has_permission else "✗")

        self.permission_tree.expandAll()
