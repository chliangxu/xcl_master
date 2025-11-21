from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QDialogButtonBox, QListWidget, QListWidgetItem


class CreateGroupDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新建用户组")
        self.setMinimumWidth(400)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("组名:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        desc_layout = QVBoxLayout()
        desc_layout.addWidget(QLabel("描述:"))
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        desc_layout.addWidget(self.desc_input)
        layout.addLayout(desc_layout)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_group_info(self):
        return {
            'name': self.name_input.text().strip(),
            'description': self.desc_input.toPlainText().strip()
        }


class UserSelectionDialog(QDialog):

    def __init__(self, available_users, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择用户")
        self.setMinimumWidth(400)
        self.setMinimumHeight(500)
        self.available_users = available_users
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("搜索:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入用户ID筛选...")
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        self.user_list = QListWidget()
        self.user_list.setSelectionMode(QListWidget.SingleSelection)
        layout.addWidget(self.user_list)

        self._update_user_list()
        self.search_input.textChanged.connect(self._update_user_list)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _update_user_list(self, filter_text=""):
        if not filter_text:
            filter_text = self.search_input.text()

        self.user_list.clear()
        for user_id in self.available_users:
            if not filter_text or filter_text.lower() in user_id.lower():
                self.user_list.addItem(QListWidgetItem(user_id))

    def get_selected_user(self):
        selected_items = self.user_list.selectedItems()
        return selected_items[0].text() if selected_items else None
