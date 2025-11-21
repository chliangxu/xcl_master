from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QLabel, QFrame, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.core.event import EventSystem
from ..controller.permission_events import PermissionEvents


class GroupPermissionsPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_group_id = None
        self._module_rows = []
        self._updating_checks = False
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        save_btn = QPushButton("保存权限")
        save_btn.clicked.connect(self._on_save_clicked)
        layout.addWidget(save_btn)

        self.permissions_container = QWidget()
        self.permissions_layout = QVBoxLayout(self.permissions_container)
        self.permissions_layout.setContentsMargins(0, 0, 0, 0)
        self.permissions_layout.setSpacing(10)
        layout.addWidget(self.permissions_container)
        layout.addStretch()

    def set_current_group_id(self, group_id: int):
        self.current_group_id = group_id

    def _on_save_clicked(self):
        if not self.current_group_id:
            return

        module_ids = []
        for row_widget in self._module_rows:
            parent_checkbox = row_widget.findChild(QCheckBox, "parent_checkbox")
            if parent_checkbox and parent_checkbox.isChecked():
                module_id = parent_checkbox.property("module_id")
                if module_id:
                    module_ids.append(module_id)

            child_checkboxes = row_widget.findChildren(QCheckBox)
            for checkbox in child_checkboxes:
                if checkbox.objectName() == "child_checkbox" and checkbox.isChecked():
                    module_id = checkbox.property("module_id")
                    if module_id:
                        module_ids.append(module_id)

        EventSystem.instance().send_event(PermissionEvents.GROUP_PERMISSION_UPDATE_REQUESTED, {
            'group_id': self.current_group_id,
            'module_ids': module_ids
        })

    def render_group_permissions(self, all_modules, selected_module_keys):
        selected_set = set(selected_module_keys)

        while self.permissions_layout.count():
            child = self.permissions_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self._module_rows = []

        for module in all_modules:
            row_widget = self._create_module_row(module, selected_set)
            container_layout.addWidget(row_widget)
            self._module_rows.append(row_widget)

        self.permissions_layout.addWidget(container_widget)

    def _create_module_row(self, module, selected_set):
        row_widget = QWidget()
        row_widget.setObjectName("moduleRow")
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(15, 10, 15, 10)
        row_layout.setSpacing(10)

        left_panel = self._create_parent_panel(module, selected_set, row_widget)
        row_layout.addWidget(left_panel, 1)

        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #ccc; min-width: 1px; max-width: 1px;")
        separator.setMinimumHeight(20)
        row_layout.addWidget(separator)

        right_panel = self._create_children_panel(module, selected_set, row_widget)
        row_layout.addWidget(right_panel, 2)

        return row_widget

    def _create_parent_panel(self, module, selected_set, row_widget):
        panel = QWidget()
        panel.setObjectName("leftPanel")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        parent_checkbox = QCheckBox()
        parent_checkbox.setObjectName("parent_checkbox")
        parent_checkbox.setProperty("module_id", module.id)
        parent_checkbox.setChecked(module.module_key in selected_set)
        parent_checkbox.setCursor(Qt.PointingHandCursor)

        parent_label = QLabel(module.module_name)
        parent_font = QFont()
        parent_font.setBold(True)
        parent_font.setPointSize(10)
        parent_label.setFont(parent_font)
        parent_label.setTextInteractionFlags(Qt.NoTextInteraction)
        parent_label.setFocusPolicy(Qt.NoFocus)

        layout.addWidget(parent_checkbox)
        layout.addWidget(parent_label)
        layout.addStretch()

        row_data = {
            'type': 'parent',
            'id': module.id,
            'parent_id': None,
            'row_widget': row_widget
        }
        parent_checkbox.stateChanged.connect(
            lambda state, data=row_data: self._on_checkbox_changed(state, data)
        )

        return panel

    def _create_children_panel(self, module, selected_set, row_widget):
        panel = QWidget()
        panel.setObjectName("rightPanel")
        layout = QGridLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(8)

        if module.children:
            max_cols = 4
            for idx, child in enumerate(module.children):
                row_idx = idx // max_cols
                col_idx = idx % max_cols

                child_container = self._create_child_checkbox(child, module, selected_set, row_widget)
                layout.addWidget(child_container, row_idx, col_idx)
        else:
            no_children_label = QLabel("无子模块")
            no_children_label.setStyleSheet("color: #999; font-style: italic;")
            no_children_label.setTextInteractionFlags(Qt.NoTextInteraction)
            no_children_label.setFocusPolicy(Qt.NoFocus)
            layout.addWidget(no_children_label, 0, 0)

        return panel

    def _create_child_checkbox(self, child, parent_module, selected_set, row_widget):
        container = QWidget()
        container.setObjectName("childContainer")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        child_checkbox = QCheckBox()
        child_checkbox.setObjectName("child_checkbox")
        child_checkbox.setProperty("module_id", child.id)
        child_checkbox.setChecked(child.module_key in selected_set)
        child_checkbox.setCursor(Qt.PointingHandCursor)

        child_label = QLabel(child.module_name)
        child_label.setTextInteractionFlags(Qt.NoTextInteraction)
        child_label.setFocusPolicy(Qt.NoFocus)

        layout.addWidget(child_checkbox)
        layout.addWidget(child_label)
        layout.addStretch()

        row_data = {
            'type': 'child',
            'id': child.id,
            'parent_id': parent_module.id,
            'row_widget': row_widget
        }
        child_checkbox.stateChanged.connect(
            lambda state, data=row_data: self._on_checkbox_changed(state, data)
        )

        return container

    def _on_checkbox_changed(self, state, row_data):
        if self._updating_checks:
            return

        self._updating_checks = True
        try:
            module_type = row_data['type']
            row_widget = row_data.get('row_widget')

            if module_type == 'parent':
                if row_widget:
                    child_checkboxes = row_widget.findChildren(QCheckBox)
                    for checkbox in child_checkboxes:
                        if checkbox.objectName() == "child_checkbox":
                            checkbox.setChecked(state)
            else:
                if state == Qt.Checked and row_widget:
                    parent_checkbox = row_widget.findChild(QCheckBox, "parent_checkbox")
                    if parent_checkbox:
                        parent_checkbox.setChecked(True)
        finally:
            self._updating_checks = False
