from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, \
    QMessageBox
from src.core.event import EventSystem
from ..controller.permission_events import PermissionEvents
from .dialogs import UserSelectionDialog


class GroupUsersPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_group_id = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        add_btn = QPushButton("添加用户")
        add_btn.clicked.connect(self._on_add_user_clicked)
        layout.addWidget(add_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["用户ID", "操作"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

    def set_current_group_id(self, group_id: int):
        self.current_group_id = group_id

    def _on_add_user_clicked(self):
        if not self.current_group_id:
            QMessageBox.warning(self, "警告", "请先选择一个用户组")
            return
        EventSystem.instance().send_event(PermissionEvents.USER_ADD_TO_GROUP_REQUESTED,
                                          self.current_group_id)

    def _on_remove_user_clicked(self, user_id: str):
        if not self.current_group_id:
            return
        EventSystem.instance().send_event(PermissionEvents.USER_REMOVE_FROM_GROUP_REQUESTED, {
            'user_id': user_id,
            'group_id': self.current_group_id
        })

    def display_group_users(self, users):
        self.table.setRowCount(0)
        for user in users:
            row = self.table.rowCount()
            self.table.insertRow(row)

            user_item = QTableWidgetItem(user['user_id'])
            self.table.setItem(row, 0, user_item)

            remove_btn = QPushButton("移除")
            remove_btn.clicked.connect(
                lambda checked, uid=user['user_id']: self._on_remove_user_clicked(uid)
            )
            self.table.setCellWidget(row, 1, remove_btn)

    def show_user_selection_dialog(self, available_users: list):
        dialog = UserSelectionDialog(available_users, self)
        if dialog.exec_():
            user_id = dialog.get_selected_user()
            if user_id and self.current_group_id:
                EventSystem.instance().send_event(PermissionEvents.USER_ADDED_TO_GROUP, {
                    'user_id': user_id,
                    'group_id': self.current_group_id
                })
