from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from src.common.base import BaseWidget
from src.core import ConfigSystem, DataService


class HeaderWidget(BaseWidget):
    user_profile_clicked = pyqtSignal()
    def init_ui(self):
        cfg = self.cfg()

        self.setFixedHeight(cfg.layout.header_height)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            cfg.layout.header_padding_h,
            cfg.layout.header_padding_v,
            cfg.layout.header_padding_h,
            cfg.layout.header_padding_v
        )
        layout.setSpacing(cfg.layout.header_spacing)

        self.logo_label = QLabel(cfg.app.name)
        logo_font = self.get_title_font(cfg.fonts.size_title)
        self.logo_label.setFont(logo_font)
        self.logo_label.setStyleSheet(f"""
            QLabel {{
                color: {self.get_primary_color()};
                padding: 5px 0px;
                margin: 0px;
            }}
        """)
        self.logo_label.setMinimumHeight(40)
        self.logo_label.setAlignment(Qt.AlignVCenter)
        layout.addWidget(self.logo_label)

        subtitle_label = QLabel(cfg.app.subtitle)
        subtitle_font = self.get_default_font(cfg.fonts.size_small)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet(f"""
            QLabel {{
                color: {self.get_secondary_text_color()};
                margin-left: 10px;
                padding: 5px 0px;
            }}
        """)
        subtitle_label.setAlignment(Qt.AlignVCenter)
        layout.addWidget(subtitle_label)

        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.user_btn = QPushButton()
        btn_size = cfg.components.user_button_size
        self.user_btn.setFixedSize(btn_size, btn_size)
        self.user_btn.clicked.connect(self.user_profile_clicked.emit)
        layout.addWidget(self.user_btn)

    def apply_styles(self):
        cfg = self.cfg()
        radius = cfg.components.user_button_size // 2

        self.setStyleSheet(f"""
            HeaderWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.get_secondary_background()}, 
                    stop:1 {self.get_background_color()});
                border-bottom: {cfg.styles.border_width}px solid {self.get_border_color()};
            }}
            QPushButton {{
                background-color: {self.get_secondary_background()};
                border: {cfg.styles.border_width}px solid {cfg.colors.border_hover};
                border-radius: {radius}px;
                color: {self.get_text_color()};
                font-weight: bold;
                font-size: {cfg.fonts.size_medium}px;
            }}
            QPushButton:hover {{
                background-color: {cfg.colors.medium_gray};
                border-color: {self.get_primary_color()};
            }}
            QPushButton:pressed {{
                background-color: {cfg.colors.gray};
            }}
        """)

    def update_user_display(self):
        user_repo = DataService.get_instance().user_repository
        if user_repo:
            user = user_repo.get_current_user()
            if user and user.name:
                display_text = user.name[:2].upper()
                self.user_btn.setText(display_text)
            else:
                self.user_btn.setText("用户")
        else:
            self.user_btn.setText("用户")
