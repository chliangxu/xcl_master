from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from src.common.base import BaseCardWidget, BaseWidget


class ToolCardWidget(BaseCardWidget):
    tool_launched = pyqtSignal(str)
    favorite_toggled = pyqtSignal(str)

    def __init__(self, tool):
        self.tool = tool
        self._fav_btn = None
        super().__init__()

    def init_ui(self):
        cfg = self.cfg()

        # 创建布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            cfg.layout.card_padding,
            cfg.layout.card_padding,
            cfg.layout.card_padding,
            cfg.layout.card_padding
        )
        layout.setSpacing(8)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        icon_label = QLabel()
        icon_size = cfg.components.icon_size
        icon_label.setFixedSize(icon_size, icon_size)
        icon_label.setStyleSheet(f"""
            QLabel {{
                background-color: {BaseWidget.get_primary_color()};
                border-radius: {icon_size // 2}px;
                color: {cfg.colors.black};
                font-weight: bold;
                font-size: {cfg.fonts.size_large}px;
            }}
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setText(self.tool.name[:2])
        header_layout.addWidget(icon_label)

        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        name_label = QLabel(self.tool.name)
        name_label.setFont(BaseWidget.get_default_font(13, bold=True))
        name_label.setStyleSheet(f"color: {BaseWidget.get_text_color()};")
        title_layout.addWidget(name_label)

        type_label = QLabel(self.tool.tool_type.value)
        type_label.setFont(BaseWidget.get_default_font(9))
        type_label.setStyleSheet(f"color: {BaseWidget.get_disabled_text_color()};")
        title_layout.addWidget(type_label)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        desc_label = QLabel(self.tool.description)
        desc_label.setFont(BaseWidget.get_default_font(cfg.fonts.size_small))
        desc_label.setStyleSheet(f"""
            QLabel {{
                color: {BaseWidget.get_secondary_text_color()};
                line-height: 1.4;
            }}
        """)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        desc_label.setMaximumHeight(60)
        layout.addWidget(desc_label)

        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(1)
        footer_layout.setContentsMargins(0, 0, 0, 0)

        self._fav_btn = QPushButton()
        self._update_favorite_icon()
        fav_size = cfg.components.favorite_button_size
        self._fav_btn.setFixedSize(fav_size, fav_size)
        self._fav_btn.setCursor(Qt.PointingHandCursor)
        self._fav_btn.clicked.connect(self._on_favorite_clicked)
        self._apply_favorite_style()
        footer_layout.addWidget(self._fav_btn)

        footer_layout.addStretch()

        launch_btn = QPushButton("启动")
        launch_btn.setFixedSize(65, 30)
        launch_btn.setCursor(Qt.PointingHandCursor)
        launch_btn.setFont(BaseWidget.get_default_font(11, bold=True))
        launch_btn.setStyleSheet(BaseWidget.get_button_style())
        launch_btn.clicked.connect(lambda: self.tool_launched.emit(self.tool.id))
        footer_layout.addWidget(launch_btn)

        layout.addLayout(footer_layout)

        # 强制设置固定大小和大小策略
        self.setFixedSize(cfg.layout.card_width, cfg.layout.card_height)
        self.setMinimumSize(cfg.layout.card_width, cfg.layout.card_height)
        self.setMaximumSize(cfg.layout.card_width, cfg.layout.card_height)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.set_clickable(False)

    def _on_favorite_clicked(self):
        self.favorite_toggled.emit(self.tool.id)
        self._update_favorite_icon()
        self._apply_favorite_style()

    def _update_favorite_icon(self):
        if self._fav_btn:
            self._fav_btn.setText("★" if self.tool.is_favorite else "☆")

    def _apply_favorite_style(self):
        if not self._fav_btn:
            return

        cfg = self.cfg()
        fav_size = cfg.components.favorite_button_size

        if self.tool.is_favorite:
            self._fav_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(0, 184, 230, 0.1);
                    border: 1px solid {BaseWidget.get_primary_color()};
                    border-radius: {fav_size // 2}px;
                    color: #ffd700;
                    font-size: {cfg.fonts.size_medium}px;
                }}
                QPushButton:hover {{
                    background-color: rgba(0, 184, 230, 0.2);
                    border-color: {cfg.colors.primary_hover};
                    color: #ffed4e;
                }}
                QPushButton:pressed {{
                    background-color: rgba(0, 184, 230, 0.3);
                }}
            """)
        else:
            self._fav_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {cfg.colors.transparent};
                    border: 1px solid {BaseWidget.get_border_color()};
                    border-radius: {fav_size // 2}px;
                    color: {BaseWidget.get_disabled_text_color()};
                    font-size: {cfg.fonts.size_medium}px;
                }}
                QPushButton:hover {{
                    background-color: {BaseWidget.get_secondary_background()};
                    border-color: {BaseWidget.get_primary_color()};
                    color: #ffd700;
                }}
                QPushButton:pressed {{
                    background-color: {cfg.colors.dark_gray};
                }}
            """)

    def update_tool(self, tool):
        self.tool = tool
        self._update_favorite_icon()
        self._apply_favorite_style()

    def apply_styles(self):
        cfg = self.cfg()
        radius = cfg.layout.card_border_radius

        self.setStyleSheet(f"""
            ToolCardWidget {{
                background-color: {self.get_color('surface')};
                border: 1px solid {self.get_color('border')};
                border-radius: {radius}px;
            }}
            ToolCardWidget:hover {{
                background-color: {self.get_color('surface_hover')};
                border-color: {self.get_color('primary')};
            }}
        """)
