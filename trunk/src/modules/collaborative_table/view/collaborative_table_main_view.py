"""
协同表格主视图 - TabView版本
包含多个表格Tab的主界面
"""

import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic

from src.common.base import BaseWidget
from src.core.config.config_system import ConfigSystem
from src.common.utils import ResourceUtils
from .collaborative_table_view import CollaborativeTableView


class CollaborativeTableMainView(BaseWidget):
    """协同表格主视图类 - 包含TabView的主界面"""
    
    # 定义信号
    tab_changed = pyqtSignal(int, str)  # Tab切换信号 (index, tab_name)
    
    def __init__(self, parent=None):
        # 初始化属性（在super().__init__之前）
        self.table_views = {}  # 存储各个Tab的表格视图
        self.current_tab_index = 0
        
        super().__init__(parent)
        
    def init_ui(self):
        """设置UI界面 - 直接加载.ui文件"""
        # 直接加载.ui文件
        self.load_ui()
        
        # 设置Tab页面
        self.setup_tabs()
        
        # 设置信号连接
        self.setup_connections()
        
    def apply_styles(self):
        """应用样式 - 重写BaseWidget的方法"""
        super().apply_styles()  # 调用父类的样式方法
        
        # 添加自定义样式
        cfg = ConfigSystem.instance()
        
        self.setStyleSheet(f"""
            ProjectModuleView {{
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
        
    def load_ui(self):
        """加载UI文件"""
        try:
            ui_file = ResourceUtils.get_ui_path(__file__, 'collaborative_table_main.ui')
            
            if not os.path.exists(ui_file):
                raise FileNotFoundError(f"UI文件不存在: {ui_file}")
                
            # 加载UI文件
            uic.loadUi(ui_file, self)
            print(f"✅ 成功加载UI文件: {ui_file}")
            
        except Exception as e:
            print(f"❌ 加载UI文件失败: {e}")
            # 如果加载失败，创建基本布局
            self.create_fallback_ui()
            
    def create_fallback_ui(self):
        """创建备用UI（当UI文件加载失败时使用）"""
        from PyQt5.QtWidgets import QTabWidget
        
        layout = QVBoxLayout(self)
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        
        # 不创建默认Tab，等待动态创建
        layout.addWidget(self.tabWidget)
        print("✅ 创建备用UI布局 - 等待动态创建Tab")
        
    def setup_tabs(self):
        """设置Tab页面内容 - 现在所有Tab都通过动态方式创建"""
        # 不再创建默认Tab，所有Tab都通过控制器动态创建
        print("✅ Tab页面设置完成 - 等待动态创建Tab")
        
    def connect_table_signals(self, table_view, tab_key):
        """连接表格视图的信号"""
        if hasattr(table_view, 'item_selected'):
            table_view.item_selected.connect(
                lambda items: self.on_table_item_selected(tab_key, items)
            )
        if hasattr(table_view, 'item_action_triggered'):
            table_view.item_action_triggered.connect(
                lambda action, row, item_id: self.on_table_action_triggered(tab_key, action, row, item_id)
            )
        if hasattr(table_view, 'search_triggered'):
            table_view.search_triggered.connect(
                lambda text: self.on_table_search_triggered(tab_key, text)
            )
        if hasattr(table_view, 'filter_changed'):
            table_view.filter_changed.connect(
                lambda filter_type: self.on_table_filter_changed(tab_key, filter_type)
            )
        if hasattr(table_view, 'page_changed'):
            table_view.page_changed.connect(
                lambda page: self.on_table_page_changed(tab_key, page)
            )
        if hasattr(table_view, 'batch_action_triggered'):  
            table_view.batch_action_triggered.connect(
                lambda action, item_ids: self.on_table_batch_action_triggered(tab_key, action, item_ids)
            )
            
    def setup_connections(self):
        """设置信号连接"""
        if hasattr(self, 'tabWidget'):
            self.tabWidget.currentChanged.connect(self.on_tab_changed)
            
    def on_tab_changed(self, index):
        """Tab切换事件处理"""
        self.current_tab_index = index
        tab_names = ["main", "secondary", "archive"]
        tab_name = tab_names[index] if index < len(tab_names) else f"tab_{index}"
        
        print(f"🔄 切换到Tab: {tab_name} (索引: {index})")
        self.tab_changed.emit(index, tab_name)
        
    def get_current_table_view(self):
        """获取当前激活的表格视图"""
        tab_names = ["main", "secondary", "archive"]
        if self.current_tab_index < len(tab_names):
            tab_key = tab_names[self.current_tab_index]
            return self.table_views.get(tab_key)
        return None
        
    def get_table_view(self, tab_key):
        """根据Tab键获取表格视图"""
        return self.table_views.get(tab_key)
        
    # 表格事件处理方法
    def on_table_item_selected(self, tab_key, items):
        """表格项选中事件"""
        print(f"📋 [{tab_key}] 选中项目: {len(items)} 个")
        
    def on_table_action_triggered(self, tab_key, action, row, item_id):
        """表格操作事件"""
        print(f"⚡ [{tab_key}] 操作: {action} - 行:{row} - ID:{item_id}")
        
    def on_table_search_triggered(self, tab_key, text):
        """表格搜索事件"""
        print(f"🔍 [{tab_key}] 搜索: '{text}'")
        
    def on_table_filter_changed(self, tab_key, filter_type):
        """表格过滤事件"""
        print(f"🔽 [{tab_key}] 过滤: '{filter_type}'")
        
    def on_table_page_changed(self, tab_key, page):
        """表格分页事件"""
        print(f"📄 [{tab_key}] 切换到第 {page} 页")
        
    def on_table_batch_action_triggered(self, tab_key, action, item_ids):
        """表格批量操作事件"""
        print(f"📦 [{tab_key}] 批量操作: {action} - IDs:{item_ids}")
        
    # 公共接口方法
    def update_data(self, tab_key=None, data=None):
        """更新指定Tab的数据"""
        if tab_key and tab_key in self.table_views:
            table_view = self.table_views[tab_key]
            if hasattr(table_view, 'update_data') and data:
                table_view.update_data(data)
                print(f"✅ 更新 [{tab_key}] 数据: {len(data)} 条记录")
        elif not tab_key:
            # 更新当前Tab的数据
            current_view = self.get_current_table_view()
            if current_view and hasattr(current_view, 'update_data') and data:
                current_view.update_data(data)
                
    def refresh_current_tab(self):
        """刷新当前Tab"""
        current_view = self.get_current_table_view()
        if current_view and hasattr(current_view, 'refresh_data'):
            current_view.refresh_data()
            
    def set_tab_enabled(self, tab_index, enabled):
        """设置Tab是否可用"""
        if hasattr(self, 'tabWidget'):
            self.tabWidget.setTabEnabled(tab_index, enabled)
            
    def add_table_tab(self, tab_key, tab_title, data=None):
        """动态添加表格Tab"""
        if not hasattr(self, 'tabWidget'):
            print("❌ TabWidget不存在，无法添加Tab")
            return -1
            
        # 检查Tab键是否已存在
        if tab_key in self.table_views:
            print(f"⚠️ Tab键 '{tab_key}' 已存在")
            return -1
            
        # 创建新的表格视图
        table_view = CollaborativeTableView()
        
        # 创建Tab窗口部件
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(table_view)
        
        # 添加到TabWidget
        tab_index = self.tabWidget.addTab(tab_widget, tab_title)
        
        # 存储表格视图引用
        self.table_views[tab_key] = table_view
        
        # 连接信号
        self.connect_table_signals(table_view, tab_key)
        
        # 如果有数据，更新表格
        if data and hasattr(table_view, 'update_data'):
            table_view.update_data(data)
            
        print(f"✅ 成功添加Tab: '{tab_title}' (键: {tab_key}, 索引: {tab_index})")
        return tab_index
        
    def remove_table_tab(self, tab_key_or_index):
        """移除表格Tab"""
        if not hasattr(self, 'tabWidget'):
            print("❌ TabWidget不存在，无法移除Tab")
            return False
            
        tab_index = -1
        tab_key = None
        
        # 根据参数类型确定要移除的Tab
        if isinstance(tab_key_or_index, str):
            # 通过tab_key查找
            tab_key = tab_key_or_index
            if tab_key not in self.table_views:
                print(f"❌ Tab键 '{tab_key}' 不存在")
                return False
            # 找到对应的索引
            for i in range(self.tabWidget.count()):
                widget = self.tabWidget.widget(i)
                # 检查这个widget是否包含我们的表格视图
                if widget and widget.layout():
                    for j in range(widget.layout().count()):
                        item = widget.layout().itemAt(j)
                        if item and item.widget() == self.table_views[tab_key]:
                            tab_index = i
                            break
                if tab_index != -1:
                    break
        elif isinstance(tab_key_or_index, int):
            # 通过索引查找
            tab_index = tab_key_or_index
            if tab_index < 0 or tab_index >= self.tabWidget.count():
                print(f"❌ Tab索引 {tab_index} 超出范围")
                return False
            # 找到对应的tab_key
            widget = self.tabWidget.widget(tab_index)
            if widget and widget.layout():
                for key, view in self.table_views.items():
                    for i in range(widget.layout().count()):
                        item = widget.layout().itemAt(i)
                        if item and item.widget() == view:
                            tab_key = key
                            break
                    if tab_key:
                        break
        
        if tab_index == -1 or not tab_key:
            print("❌ 无法找到要移除的Tab")
            return False
            
        # 移除Tab
        tab_title = self.tabWidget.tabText(tab_index)
        self.tabWidget.removeTab(tab_index)
        
        # 清理表格视图引用
        if tab_key in self.table_views:
            del self.table_views[tab_key]
            
        print(f"✅ 成功移除Tab: '{tab_title}' (键: {tab_key}, 索引: {tab_index})")
        return True
        
    def get_tab_count(self):
        """获取Tab数量"""
        if hasattr(self, 'tabWidget'):
            return self.tabWidget.count()
        return 0
        
    def get_tab_info(self):
        """获取所有Tab信息"""
        if not hasattr(self, 'tabWidget'):
            return []
            
        tab_info = []
        for i in range(self.tabWidget.count()):
            title = self.tabWidget.tabText(i)
            enabled = self.tabWidget.isTabEnabled(i)
            tab_info.append({
                'index': i,
                'title': title,
                'enabled': enabled
            })
        return tab_info
        
    def rename_tab(self, tab_index, new_title):
        """重命名Tab"""
        if hasattr(self, 'tabWidget') and 0 <= tab_index < self.tabWidget.count():
            old_title = self.tabWidget.tabText(tab_index)
            self.tabWidget.setTabText(tab_index, new_title)
            print(f"✅ Tab重命名: '{old_title}' -> '{new_title}'")
            return True
        return False
        
    def clear_all_tabs(self):
        """清空所有Tab"""
        if not hasattr(self, 'tabWidget'):
            return
            
        count = self.tabWidget.count()
        self.tabWidget.clear()
        self.table_views.clear()
        print(f"✅ 清空所有Tab，共移除 {count} 个Tab")
        
    def move_tab(self, from_index, to_index):
        """移动Tab位置"""
        if not hasattr(self, 'tabWidget'):
            return False
            
        if (0 <= from_index < self.tabWidget.count() and 
            0 <= to_index < self.tabWidget.count() and 
            from_index != to_index):
            
            # 获取Tab信息
            widget = self.tabWidget.widget(from_index)
            title = self.tabWidget.tabText(from_index)
            enabled = self.tabWidget.isTabEnabled(from_index)
            
            # 移除原Tab
            self.tabWidget.removeTab(from_index)
            
            # 在新位置插入
            self.tabWidget.insertTab(to_index, widget, title)
            self.tabWidget.setTabEnabled(to_index, enabled)
            
            print(f"✅ Tab移动: 从索引 {from_index} 移动到 {to_index}")
            return True
        return False