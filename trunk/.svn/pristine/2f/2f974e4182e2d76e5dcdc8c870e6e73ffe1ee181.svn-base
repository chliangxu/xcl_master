from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from src.core.event import EventSystem
from ..controller.permission_events import PermissionEvents
from .dialogs import CreateGroupDialog


class GroupListPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        header = QLabel("用户组列表")
        layout.addWidget(header)

        create_btn = QPushButton("+ 新建用户组")
        create_btn.clicked.connect(self._on_create_clicked)
        layout.addWidget(create_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["组名", "用户数", "权限数"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self.table)

    def _on_create_clicked(self):
        dialog = CreateGroupDialog(self)
        if dialog.exec_():
            info = dialog.get_group_info()
            if info['name']:
                EventSystem.instance().send_event(PermissionEvents.GROUP_CREATE_REQUESTED, {
                    'name': info['name'],
                    'description': info['description']
                })

    def _on_selection_changed(self):
        selected_rows = self.table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            group_id = self.table.item(row, 0).data(Qt.UserRole)
            if group_id:
                EventSystem.instance().send_event(PermissionEvents.GROUP_SELECTED, group_id)

    def display_groups(self, groups):
        self.table.setRowCount(0)
        for group in groups:
            row = self.table.rowCount()
            self.table.insertRow(row)

            name_item = QTableWidgetItem(group['name'])
            name_item.setData(Qt.UserRole, group['id'])
            self.table.setItem(row, 0, name_item)

            self.table.setItem(row, 1, QTableWidgetItem(str(group.get('user_count', 0))))
            self.table.setItem(row, 2, QTableWidgetItem(str(group.get('permission_count', 0))))
