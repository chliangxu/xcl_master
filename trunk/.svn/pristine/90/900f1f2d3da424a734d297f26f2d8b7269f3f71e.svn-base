from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QStackedWidget, QLabel
from PyQt5.QtCore import Qt
from src.common.base import BaseWidget
from .current_user_tab import CurrentUserTab
from .group_manage_tab import GroupManageTab
from .third_party_permission_tab import ThirdPartyPermissionTab


class PermissionModuleView(BaseWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_group_id = None

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget()

        loading_widget = QWidget()
        loading_layout = QVBoxLayout(loading_widget)
        loading_layout.setAlignment(Qt.AlignCenter)
        loading_label = QLabel("加载中...")
        loading_label.setStyleSheet("font-size: 16px; color: #666;")
        loading_layout.addWidget(loading_label)

        self.tab_widget = QTabWidget()
        self.current_user_tab = CurrentUserTab()
        self.tab_widget.addTab(self.current_user_tab, "当前用户权限")

        self.group_manage_tab = GroupManageTab()
        self.tab_widget.addTab(self.group_manage_tab, "用户组管理")
        
        self.third_party_tab = ThirdPartyPermissionTab()
        self.tab_widget.addTab(self.third_party_tab, "第三方权限管理")

        self.stacked_widget.addWidget(self.tab_widget)
        self.stacked_widget.addWidget(loading_widget)

        layout.addWidget(self.stacked_widget)

    def show_loading(self):
        self.stacked_widget.setCurrentIndex(1)

    def hide_loading(self):
        self.stacked_widget.setCurrentIndex(0)

    def display_user_info(self, user_id: str, groups: list):
        self.current_user_tab.display_user_info(user_id, groups)

    def display_permissions(self, all_modules, user_permissions):
        self.current_user_tab.display_permissions(all_modules, user_permissions)

    def display_groups(self, groups):
        self.group_manage_tab.display_groups(groups)

    def show_detail_loading(self):
        self.group_manage_tab.show_detail_loading()

    def hide_detail_loading(self):
        self.group_manage_tab.hide_detail_loading()

    def set_current_group_id(self, group_id: int):
        self.current_group_id = group_id
        self.group_manage_tab.set_current_group_id(group_id)

    def display_group_detail(self, group_name: str):
        self.group_manage_tab.display_group_detail(group_name)

    def display_group_users(self, users):
        self.group_manage_tab.display_group_users(users)

    def render_group_permissions(self, all_modules, selected_module_keys):
        self.group_manage_tab.render_group_permissions(all_modules, selected_module_keys)

    def show_user_selection_dialog(self, available_users: list):
        self.group_manage_tab.show_user_selection_dialog(available_users)

    def apply_styles(self):
        cfg = self.cfg()

        self.setStyleSheet(f"""
            PermissionModuleView {{
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
        """)
