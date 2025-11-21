from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal
from src.common.base import BaseWidget
from src.core import DataService


class UserProfileWidget(QDialog):
    profile_updated = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.user = None
        self.cfg = BaseWidget.cfg()
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        self.setWindowTitle("用户资料")
        self.setFixedSize(
            self.cfg.components.dialog_width,
            self.cfg.components.dialog_height
        )
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        header_layout = QVBoxLayout()
        header_layout.setSpacing(10)

        self.avatar_label = QLabel()
        avatar_size = self.cfg.components.avatar_size
        self.avatar_label.setFixedSize(avatar_size, avatar_size)
        self.avatar_label.setStyleSheet(f"""
            QLabel {{
                background-color: {BaseWidget.get_primary_color()};
                border-radius: {avatar_size // 2}px;
                color: {self.cfg.colors.black};
                font-weight: bold;
                font-size: {self.cfg.fonts.size_title + 4}px;
            }}
        """)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.avatar_label, 0, Qt.AlignCenter)

        self.name_label = QLabel("用户名")
        self.name_label.setFont(BaseWidget.get_title_font(self.cfg.fonts.size_large))
        self.name_label.setStyleSheet(f"color: {BaseWidget.get_text_color()};")
        self.name_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.name_label)

        layout.addLayout(header_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(f"color: {BaseWidget.get_border_color()};")
        layout.addWidget(separator)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        name_layout = QVBoxLayout()
        name_layout.setSpacing(5)
        name_label = QLabel("姓名:")
        name_label.setFont(BaseWidget.get_default_font(self.cfg.fonts.size_small, bold=True))
        name_label.setStyleSheet(f"color: {BaseWidget.get_text_color()};")
        name_layout.addWidget(name_label)

        self.name_edit = QLineEdit()
        self.name_edit.setFont(BaseWidget.get_default_font(self.cfg.fonts.size_small))
        name_layout.addWidget(self.name_edit)
        form_layout.addLayout(name_layout)

        role_layout = QVBoxLayout()
        role_layout.setSpacing(5)
        role_label = QLabel("角色:")
        role_label.setFont(BaseWidget.get_default_font(self.cfg.fonts.size_small, bold=True))
        role_label.setStyleSheet(f"color: {BaseWidget.get_text_color()};")
        role_layout.addWidget(role_label)

        self.role_combo = QComboBox()
        self.role_combo.setFont(BaseWidget.get_default_font(self.cfg.fonts.size_small))
        self.role_combo.addItems(["策划", "客户端程序", "服务器程序", "美术", "运营"])
        role_layout.addWidget(self.role_combo)
        form_layout.addLayout(role_layout)

        layout.addLayout(form_layout)
        layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        cancel_btn = QPushButton("取消")
        cancel_btn.setFixedSize(
            self.cfg.components.button_width,
            self.cfg.components.button_height
        )
        cancel_btn.setFont(BaseWidget.get_default_font(self.cfg.fonts.size_small))
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        button_layout.addStretch()

        save_btn = QPushButton("保存")
        save_btn.setFixedSize(
            self.cfg.components.button_width,
            self.cfg.components.button_height
        )
        save_btn.setFont(BaseWidget.get_default_font(self.cfg.fonts.size_small, bold=True))
        save_btn.clicked.connect(self.save_profile)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)

    def apply_styles(self):
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {BaseWidget.get_background_color()};
                color: {BaseWidget.get_text_color()};
            }}
            QLineEdit {{
                background-color: {BaseWidget.get_secondary_background()};
                border: 1px solid {BaseWidget.get_border_color()};
                border-radius: 6px;
                padding: 8px;
                color: {BaseWidget.get_text_color()};
            }}
            QLineEdit:focus {{
                border-color: {BaseWidget.get_primary_color()};
            }}
            QComboBox {{
                background-color: {BaseWidget.get_secondary_background()};
                border: 1px solid {BaseWidget.get_border_color()};
                border-radius: 6px;
                padding: 8px;
                color: {BaseWidget.get_text_color()};
            }}
            QComboBox:focus {{
                border-color: {BaseWidget.get_primary_color()};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {BaseWidget.get_text_color()};
            }}
            QPushButton {{
                background-color: {BaseWidget.get_secondary_background()};
                border: 1px solid {BaseWidget.get_border_color()};
                border-radius: 6px;
                color: {BaseWidget.get_text_color()};
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {self.cfg.colors.dark_gray};
                border-color: {BaseWidget.get_primary_color()};
            }}
            QPushButton:pressed {{
                background-color: {self.cfg.colors.medium_gray};
            }}
        """)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_user_info()
    
    def load_user_info(self):
        user_repo = DataService.get_instance().user_repository
        if user_repo:
            user = user_repo.get_current_user()
            if user:
                self.user = user
                self.name_label.setText(user.name)
                self.avatar_label.setText(user.name[:2].upper())
                self.name_edit.setText(user.name)

                role_map = {
                    "策划": 0,
                    "客户端程序": 1,
                    "服务器程序": 2,
                    "美术": 3,
                    "运营": 4
                }
                role_index = role_map.get(user.role.value, 0)
                self.role_combo.setCurrentIndex(role_index)

    def save_profile(self):
        if self.user:
            new_name = self.name_edit.text().strip()
            role_text = self.role_combo.currentText()

            if new_name:
                profile_data = {
                    'name': new_name,
                    'role': role_text
                }
                self.profile_updated.emit(profile_data)
                self.accept()
