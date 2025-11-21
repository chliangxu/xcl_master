from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QGridLayout, QFrame, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from src.common.base import BaseWidget
from src.modules.tools.view.tool_card_widget import ToolCardWidget


class ToolsMainView(BaseWidget):
    tool_launched = pyqtSignal(str)
    favorite_toggled = pyqtSignal(str)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.banner_widget = self.create_banner()
        layout.addWidget(self.banner_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        cfg = self.cfg()
        self.content_layout.setContentsMargins(
            cfg.layout.content_padding,
            cfg.layout.content_spacing,
            cfg.layout.content_padding,
            cfg.layout.content_spacing
        )

        self.scroll_area.setWidget(self.content_container)
        layout.addWidget(self.scroll_area)

    def create_banner(self):
        cfg = self.cfg()
        banner = QFrame()
        banner.setFixedHeight(cfg.layout.banner_height)

        layout = QVBoxLayout(banner)
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(15)

        title = QLabel(cfg.app.name)
        title.setFont(self.get_title_font(28))
        title.setStyleSheet(f"""
            QLabel {{
                color: {self.get_text_color()};
                background: transparent;
                padding: 10px 0px;
                margin: 0px;
            }}
        """)
        title.setAlignment(Qt.AlignVCenter)
        title.setMinimumHeight(50)
        layout.addWidget(title)

        subtitle = QLabel(cfg.app.subtitle)
        subtitle.setFont(self.get_default_font(cfg.fonts.size_large, bold=True))
        subtitle.setStyleSheet(f"""
            QLabel {{
                color: {self.get_secondary_text_color()};
                background: transparent;
                margin-top: 5px;
                padding: 5px 0px;
            }}
        """)
        layout.addWidget(subtitle)

        layout.addStretch()

        banner.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e3c72, stop:1 #2a5298);
                border-radius: 15px;
                margin: 20px;
            }
        """)

        return banner

    def update_tools(self, category, tools):
        cfg = self.cfg()
        self.clear_content()

        if not tools:
            no_tools_label = QLabel("暂无工具")
            no_tools_label.setAlignment(Qt.AlignCenter)
            no_tools_label.setFont(self.get_default_font(cfg.fonts.size_large))
            no_tools_label.setStyleSheet(f"""
                QLabel {{
                    color: {self.get_disabled_text_color()};
                    padding: 50px;
                }}
            """)
            self.content_layout.addWidget(no_tools_label)
            return

        category_name = cfg.categories.get_name(category)
        category_label = QLabel(f"{category_name} 工具")
        category_label.setFont(self.get_title_font(18))
        category_label.setStyleSheet(f"""
            QLabel {{
                color: {self.get_text_color()};
                padding: 20px 0px 10px 0px;
                margin-bottom: 10px;
            }}
        """)
        self.content_layout.addWidget(category_label)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(cfg.layout.card_spacing)

        for i, tool in enumerate(tools):
            tool_card = ToolCardWidget(tool)
            tool_card.tool_launched.connect(self.tool_launched.emit)
            tool_card.favorite_toggled.connect(self.favorite_toggled.emit)

            row = i // 3
            col = i % 3
            grid_layout.addWidget(tool_card, row, col)

        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)
        self.content_layout.addWidget(grid_widget)

        self.content_layout.addStretch()

    def clear_content(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def apply_styles(self):
        self.setStyleSheet(f"""
            ToolsMainView {{
                background-color: {self.get_background_color()};
            }}
            QScrollArea {{
                border: none;
                background-color: {self.get_background_color()};
            }}
            {self.get_scrollbar_style()}
        """)
