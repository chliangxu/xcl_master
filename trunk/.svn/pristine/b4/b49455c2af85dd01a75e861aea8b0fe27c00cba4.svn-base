from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt
from ..model.permission_models import PermissionRepository
from ..controller.permission_events import PermissionEvents
from src.core.event import EventSystem


class ThirdPartyPermissionTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.repository = PermissionRepository.get_instance()
        self._init_ui()
        self._load_data()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        info_label = QLabel("第三方权限申请管理 - 点击链接跳转到对应的权限管理页面")
        info_label.setStyleSheet("font-size: 14px; color: #666; padding: 10px;")
        layout.addWidget(info_label)

        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("刷新列表")
        refresh_btn.clicked.connect(self._load_data)
        refresh_btn.setMaximumWidth(120)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["权限名称", "权限描述", "管理链接"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 500)
        self.table.cellDoubleClicked.connect(self._on_cell_clicked)

        layout.addWidget(self.table)

    def _load_data(self):
        try:
            permissions = self.repository.get_third_party_permissions()
            if not permissions:
                self.table.setRowCount(0)
                QMessageBox.information(self, "提示", "暂无第三方权限数据")
                return
            self._populate_table(permissions)
        except Exception as e:
            QMessageBox.warning(self, "加载失败", f"加载第三方权限数据失败\n错误: {str(e)}")
            self.table.setRowCount(0)

    def _populate_table(self, permissions):
        self.table.setRowCount(len(permissions))

        for row_idx, permission in enumerate(permissions):
            name_item = QTableWidgetItem(permission.typename)
            self.table.setItem(row_idx, 0, name_item)

            desc_item = QTableWidgetItem(permission.type)
            self.table.setItem(row_idx, 1, desc_item)

            url_item = QTableWidgetItem(permission.jumpurl)
            url_item.setForeground(Qt.blue)
            url_item.setToolTip("点击打开链接")
            url_item.setData(Qt.UserRole, permission.jumpurl)
            self.table.setItem(row_idx, 2, url_item)

    def _on_cell_clicked(self, row, col):
        if col == 2:
            url_item = self.table.item(row, col)
            if url_item:
                url = url_item.data(Qt.UserRole)
                EventSystem.instance().send_event(PermissionEvents.THIRD_PARTY_URL_OPEN_REQUESTED, url)
