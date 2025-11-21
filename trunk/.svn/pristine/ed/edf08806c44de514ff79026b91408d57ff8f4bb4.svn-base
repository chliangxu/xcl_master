from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QScrollArea, QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal
from src.common.base import BaseWidget
from src.modules.tools.view.tool_card_widget import ToolCardWidget


class ToolsModuleView(BaseWidget):
    tool_launched = pyqtSignal(str)
    favorite_toggled = pyqtSignal(str)

    def __init__(self):
        self._favorite_grid = None
        self._toolset_grid = None
        self._favorite_container = None
        self._toolset_container = None
        super().__init__()

        from PyQt5.QtCore import QTimer
        QTimer.singleShot(0, self._load_tools)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tab_widget = QTabWidget()

        favorite_tab = self._create_favorite_tab()
        toolset_tab = self._create_toolset_tab()

        import_tab = QWidget()
        import_layout = QVBoxLayout(import_tab)
        import_layout.addWidget(QLabel("导入工具"))

        self.tab_widget.addTab(favorite_tab, "我的收藏")
        self.tab_widget.addTab(toolset_tab, "工具集")
        self.tab_widget.addTab(import_tab, "导入工具")

        layout.addWidget(self.tab_widget)

    def _create_favorite_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self._favorite_container = QWidget()
        container_layout = QVBoxLayout(self._favorite_container)
        cfg = self.cfg()
        container_layout.setContentsMargins(
            cfg.layout.content_padding,
            cfg.layout.content_spacing,
            cfg.layout.content_padding,
            cfg.layout.content_spacing
        )

        self._favorite_grid = QGridLayout()
        self._favorite_grid.setSpacing(cfg.layout.card_spacing)
        container_layout.addLayout(self._favorite_grid)
        container_layout.addStretch()

        scroll_area.setWidget(self._favorite_container)
        layout.addWidget(scroll_area)

        return tab

    def _create_toolset_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self._toolset_container = QWidget()
        container_layout = QVBoxLayout(self._toolset_container)
        cfg = self.cfg()
        container_layout.setContentsMargins(
            cfg.layout.content_padding,
            cfg.layout.content_spacing,
            cfg.layout.content_padding,
            cfg.layout.content_spacing
        )

        self._toolset_grid = QGridLayout()
        self._toolset_grid.setSpacing(cfg.layout.card_spacing)
        container_layout.addLayout(self._toolset_grid)
        container_layout.addStretch()

        scroll_area.setWidget(self._toolset_container)
        layout.addWidget(scroll_area)

        return tab

    def _load_tools(self):
        from src.core import DataService
        data_service = DataService.get_instance()
        if not data_service or not data_service.tool_repository:
            return

        tool_repo = data_service.tool_repository

        favorite_tools = tool_repo.get_favorites()
        self._update_tool_grid(self._favorite_grid, favorite_tools)

        all_tools = []
        for tool_id, tool in tool_repo._tools.items():
            all_tools.append(tool)
        self._update_tool_grid(self._toolset_grid, all_tools)

    def _update_tool_grid(self, grid_layout, tools):
        if grid_layout is None:
            return

        while grid_layout.count():
            item = grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not tools:
            no_tools_label = QLabel("暂无工具")
            no_tools_label.setAlignment(Qt.AlignCenter)
            cfg = self.cfg()
            no_tools_label.setFont(self.get_default_font(cfg.fonts.size_large))
            no_tools_label.setStyleSheet(f"""
                QLabel {{
                    color: {self.get_disabled_text_color()};
                    padding: 50px;
                }}
            """)
            grid_layout.addWidget(no_tools_label, 0, 0)
            return

        for i, tool in enumerate(tools):
            tool_card = ToolCardWidget(tool)

            tool_card.tool_launched.connect(self.tool_launched.emit)
            tool_card.favorite_toggled.connect(self.favorite_toggled.emit)

            row = i // 3
            col = i % 3
            grid_layout.addWidget(tool_card, row, col)

    def refresh_tools(self):
        self._load_tools()

    def apply_styles(self):
        cfg = self.cfg()

        self.setStyleSheet(f"""
            ToolsModuleView {{
                background-color: {cfg.colors.background};
            }}
            QTabWidget::pane {{
                border: 1px solid {self.get_border_color()};
                background-color: {cfg.colors.background};
            }}
            QTabBar::tab {{
                background-color: {cfg.colors.surface};
                color: {cfg.colors.text_secondary};
                padding: 10px 20px;
                margin-right: 2px;
                border: 1px solid {self.get_border_color()};
                border-bottom: none;
            }}
            QTabBar::tab:selected {{
                background-color: {cfg.colors.background};
                color: {self.get_primary_color()};
                border-bottom: 2px solid {self.get_primary_color()};
            }}
            QTabBar::tab:hover {{
                background-color: {cfg.colors.surface_hover};
            }}
            QScrollArea {{
                border: none;
                background-color: {cfg.colors.background};
            }}
            {self.get_scrollbar_style()}
        """)
