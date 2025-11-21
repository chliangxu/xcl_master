"""
协同表格主控制器 - 管理多个Tab的控制逻辑，同时作为模块的统一入口
"""

from PyQt5.QtCore import QObject, pyqtSignal
from typing import Dict, List, Optional, Any

from src.common.base import BaseController
from ..model.collaborative_table_main_model import CollaborativeTableMainModel
from ..view.collaborative_table_main_view import CollaborativeTableMainView
from .collaborative_table_controller import CollaborativeTableController


class CollaborativeTableMainController(BaseController):
    """协同表格主控制器类"""

    MODULE_KEY: str = "CollaborativeSheet"
    
    # 定义业务信号
    tab_created = pyqtSignal(str, str)        # Tab创建 (tab_key, tab_title)
    tab_removed = pyqtSignal(str)             # Tab移除 (tab_key)
    tab_switched = pyqtSignal(str, str)       # Tab切换 (old_key, new_key)
    data_synchronized = pyqtSignal(str, int)  # 数据同步 (tab_key, record_count)
    error_occurred = pyqtSignal(str)          # 错误发生
    operation_completed = pyqtSignal(str, bool)  # 操作完成 (operation, success)
    
    # 对外信号（作为模块入口）
    initialized = pyqtSignal(bool)                    # 初始化完成
    tab_operation_completed = pyqtSignal(str, bool)   # Tab操作完成
    
    def __init__(self, dependencies: Optional[Dict[str, object]] = None):
        super().__init__(dependencies)
        
        # 创建MVC组件
        self._main_model = CollaborativeTableMainModel()
        self._main_view = CollaborativeTableMainView()
        
        # Tab控制器管理
        self.tab_controllers: Dict[str, CollaborativeTableController] = {}
        self.current_tab_key: str = ""
        
        # 设置MVC关联
        self._setup_mvc_connections()
        
        print("✅ 协同表格主控制器创建完成")
        
    def _setup_mvc_connections(self):
        """设置MVC连接"""
        # 连接模型信号
        self._main_model.tab_config_changed.connect(self._on_model_tab_config_changed)
        self._main_model.tab_data_updated.connect(self._on_model_tab_data_updated)
        self._main_model.tabs_reordered.connect(self._on_model_tabs_reordered)
        
        # 连接视图信号
        self._main_view.tab_changed.connect(self._on_view_tab_changed)
        
        # 连接控制器信号到对外信号（作为模块入口）
        self.error_occurred.connect(self.error_occurred.emit)
        self.operation_completed.connect(self.tab_operation_completed.emit)
        
        print("✅ 主控制器MVC连接设置完成")

    def get_module_view(self) -> CollaborativeTableMainView:
        """获取模块视图
        
        Returns:
            CollaborativeTableMainView: 协同表格视图实例
        """
        return self.get_main_view()
        
    def get_main_view(self) -> CollaborativeTableMainView:
        """获取主视图"""
        return self._main_view
        
    def get_main_model(self) -> CollaborativeTableMainModel:
        """获取主模型"""
        return self._main_model
        
    def initialize(self) -> bool:
        """初始化控制器"""
        try:
            print("🚀 初始化主控制器...")
            
            # 初始化所有默认Tab
            self._initialize_default_tabs()
            
            # 设置当前Tab
            tab_order = self._main_model.get_tab_order()
            if tab_order:
                self.current_tab_key = tab_order[0]
                
            print("✅ 主控制器初始化成功")
            self.operation_completed.emit("初始化", True)
            self.initialized.emit(True)
            return True
            
        except Exception as e:
            error_msg = f"主控制器初始化失败: {e}"
            print(f"❌ {error_msg}")
            self.error_occurred.emit(error_msg)
            self.initialized.emit(False)
            return False
            
    def _initialize_default_tabs(self):
        """初始化默认Tab"""
        tab_configs = self._main_model.get_all_tab_configs()
        tab_order = self._main_model.get_tab_order()
        
        # 清空视图中的现有Tab
        self._main_view.clear_all_tabs()
        
        # 按顺序创建Tab
        for tab_key in tab_order:
            if tab_key in tab_configs:
                config = tab_configs[tab_key]
                create_result = self._create_tab_in_view(tab_key, config.tab_title)
                
                if create_result:
                    # 加载示例数据
                    self._main_model.load_sample_data_for_tab(tab_key)
                else:
                    print(f"❌ Tab创建失败，跳过数据加载: {tab_key}")
                
        print(f"✅ 初始化了 {len(tab_order)} 个默认Tab")
        
    def _create_tab_in_view(self, tab_key: str, tab_title: str) -> bool:
        """在视图中创建Tab"""
        try:
            # 在视图中添加Tab
            tab_index = self._main_view.add_table_tab(tab_key, tab_title)
            if tab_index == -1:
                return False
                
            # 获取Tab的表格视图
            table_view = self._main_view.get_table_view(tab_key)
            if not table_view:
                print(f"❌ 无法获取Tab '{tab_key}' 的表格视图")
                return False
                
            # 创建Tab控制器
            tab_controller = CollaborativeTableController()
            
            # 获取Tab的数据模型
            tab_model = self._main_model.get_tab_model(tab_key)
            if tab_model:
                tab_controller.set_model(tab_model)
                
            # 设置视图
            tab_controller.set_view(table_view)
            
            # 初始化Tab控制器
            tab_controller.initialize()
            
            # 存储Tab控制器
            self.tab_controllers[tab_key] = tab_controller
            
            # 连接Tab控制器信号
            self._connect_tab_controller_signals(tab_key, tab_controller)
            
            print(f"✅ 在视图中创建Tab: '{tab_title}' (键: {tab_key})")
            self.tab_created.emit(tab_key, tab_title)
            
            return True
            
        except Exception as e:
            error_msg = f"创建Tab失败: {e}"
            print(f"❌ {error_msg}")
            self.error_occurred.emit(error_msg)
            return False
            
    def _connect_tab_controller_signals(self, tab_key: str, controller: CollaborativeTableController):
        """连接Tab控制器信号"""
        if hasattr(controller, 'error_occurred'):
            controller.error_occurred.connect(
                lambda msg: self._on_tab_error(tab_key, msg)
            )
        if hasattr(controller, 'operation_completed'):
            controller.operation_completed.connect(
                lambda op, success: self._on_tab_operation_completed(tab_key, op, success)
            )
            
    def add_custom_tab(self, tab_key: str, tab_title: str, tab_type: str = "custom", data: Optional[List[Dict[str, Any]]] = None) -> bool:
        """添加自定义Tab"""
        try:
            # 在模型中添加Tab配置
            if not self._main_model.add_tab_config(tab_key, tab_title, tab_type):
                return False
                
            # 在视图中创建Tab
            if not self._create_tab_in_view(tab_key, tab_title):
                # 如果视图创建失败，回滚模型操作
                self._main_model.remove_tab_config(tab_key)
                return False
                
            # 更新数据
            if data:
                self._main_model.update_tab_data(tab_key, data)
                
            print(f"✅ 成功添加自定义Tab: '{tab_title}' (键: {tab_key})")
            self.operation_completed.emit("添加Tab", True)
            return True
            
        except Exception as e:
            error_msg = f"添加自定义Tab失败: {e}"
            print(f"❌ {error_msg}")
            self.error_occurred.emit(error_msg)
            return False
            
    def remove_tab(self, tab_key: str) -> bool:
        """移除Tab"""
        try:
            # 检查Tab是否存在
            if tab_key not in self.tab_controllers:
                print(f"❌ Tab '{tab_key}' 不存在")
                return False
                
            # 获取Tab标题用于日志
            config = self._main_model.get_tab_config(tab_key)
            tab_title = config.tab_title if config else tab_key
            
            # 从视图中移除Tab
            self._main_view.remove_table_tab(tab_key)
            
            # 清理Tab控制器
            if tab_key in self.tab_controllers:
                del self.tab_controllers[tab_key]
                
            # 从模型中移除Tab配置
            self._main_model.remove_tab_config(tab_key)
            
            # 如果移除的是当前Tab，切换到第一个可用Tab
            if self.current_tab_key == tab_key:
                tab_order = self._main_model.get_tab_order()
                self.current_tab_key = tab_order[0] if tab_order else ""
                
            print(f"✅ 成功移除Tab: '{tab_title}' (键: {tab_key})")
            self.tab_removed.emit(tab_key)
            self.operation_completed.emit("移除Tab", True)
            return True
            
        except Exception as e:
            error_msg = f"移除Tab失败: {e}"
            print(f"❌ {error_msg}")
            self.error_occurred.emit(error_msg)
            return False
            
    def rename_tab(self, tab_key: str, new_title: str) -> bool:
        """重命名Tab"""
        try:
            # 更新模型中的标题
            if not self._main_model.update_tab_title(tab_key, new_title):
                return False
                
            # 更新视图中的标题
            tab_order = self._main_model.get_tab_order()
            if tab_key in tab_order:
                tab_index = tab_order.index(tab_key)
                self._main_view.rename_tab(tab_index, new_title)
                
            print(f"✅ 成功重命名Tab: '{tab_key}' -> '{new_title}'")
            self.operation_completed.emit("重命名Tab", True)
            return True
            
        except Exception as e:
            error_msg = f"重命名Tab失败: {e}"
            print(f"❌ {error_msg}")
            self.error_occurred.emit(error_msg)
            return False
            
    def get_current_tab_controller(self) -> Optional[CollaborativeTableController]:
        """获取当前Tab的控制器"""
        if self.current_tab_key:
            return self.tab_controllers.get(self.current_tab_key)
        return None
        
    def get_tab_controller(self, tab_key: str) -> Optional[CollaborativeTableController]:
        """获取指定Tab的控制器"""
        return self.tab_controllers.get(tab_key)
        
    def update_tab_data(self, tab_key: str, data: List[Dict[str, Any]]) -> bool:
        """更新Tab数据"""
        return self._main_model.update_tab_data(tab_key, data)
        
    def get_tab_statistics(self) -> Dict[str, Any]:
        """获取Tab统计信息"""
        return self._main_model.get_tab_statistics()
        
    def search_across_all_tabs(self, keyword: str) -> Dict[str, List[Dict[str, Any]]]:
        """跨所有Tab搜索"""
        return self._main_model.search_across_tabs(keyword)
        
    def refresh_all_tabs(self):
        """刷新所有Tab"""
        try:
            for tab_key, controller in self.tab_controllers.items():
                if hasattr(controller, 'refresh_data'):
                    controller.refresh_data()
                    
            print("✅ 刷新所有Tab完成")
            self.operation_completed.emit("刷新所有Tab", True)
            
        except Exception as e:
            error_msg = f"刷新所有Tab失败: {e}"
            print(f"❌ {error_msg}")
            self.error_occurred.emit(error_msg)
            
    # 事件处理方法
    def _on_model_tab_config_changed(self, tab_key: str, config: Dict[str, Any]):
        """模型Tab配置变化处理"""
        print(f"📊 Tab配置变化: {tab_key} - {config.get('tab_title', 'Unknown')}")
        
    def _on_model_tab_data_updated(self, tab_key: str, data: List[Dict[str, Any]]):
        """模型Tab数据更新处理"""
        print(f"📋 Tab数据更新: {tab_key} - {len(data)} 条记录")
        self.data_synchronized.emit(tab_key, len(data))
        
    def _on_model_tabs_reordered(self, new_order: List[str]):
        """模型Tab重新排序处理"""
        print(f"🔄 Tab重新排序: {new_order}")
        
    def _on_view_tab_changed(self, index: int, tab_name: str):
        """视图Tab切换处理"""
        # 根据索引找到对应的tab_key
        tab_order = self._main_model.get_tab_order()
        if 0 <= index < len(tab_order):
            old_tab_key = self.current_tab_key
            new_tab_key = tab_order[index]
            self.current_tab_key = new_tab_key
            
            print(f"🔄 Tab切换: {old_tab_key} -> {new_tab_key}")
            self.tab_switched.emit(old_tab_key, new_tab_key)
            
    def _on_tab_error(self, tab_key: str, error_msg: str):
        """Tab错误处理"""
        full_msg = f"Tab '{tab_key}' 错误: {error_msg}"
        print(f"❌ {full_msg}")
        self.error_occurred.emit(full_msg)
        
    def _on_tab_operation_completed(self, tab_key: str, operation: str, success: bool):
        """Tab操作完成处理"""
        status = "成功" if success else "失败"
        print(f"{'✅' if success else '❌'} Tab '{tab_key}' {operation}: {status}")
        self.operation_completed.emit(f"Tab {operation}", success)
        
    # ==================== 模块入口便捷方法 ====================
    
    def get_main_view(self) -> CollaborativeTableMainView:
        """获取主视图 - 用于嵌入到其他窗口"""
        return self._main_view
        
    def get_main_controller(self) -> 'CollaborativeTableMainController':
        """获取主控制器 - 用于高级操作"""
        return self
        
    def get_main_model(self) -> CollaborativeTableMainModel:
        """获取主模型 - 用于数据访问"""
        return self._main_model
        
    def add_simple_tab(self, tab_key: str, tab_title: str, data: Optional[List[Dict[str, Any]]] = None) -> bool:
        """添加简单Tab（便捷方法）"""
        return self.add_custom_tab(tab_key, tab_title, "custom", data)
        
    def get_tab_data(self, tab_key: str) -> List[Dict[str, Any]]:
        """获取Tab数据"""
        return self._main_model.get_tab_data(tab_key)
        
    def search_all_tabs(self, keyword: str) -> Dict[str, List[Dict[str, Any]]]:
        """搜索所有Tab"""
        return self.search_across_all_tabs(keyword)
        
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self.get_tab_statistics()
        
    def refresh_all(self):
        """刷新所有Tab"""
        self.refresh_all_tabs()
        
    def get_tab_list(self) -> List[Dict[str, str]]:
        """获取Tab列表"""
        tab_configs = self._main_model.get_all_tab_configs()
        tab_order = self._main_model.get_tab_order()
        
        tab_list = []
        for tab_key in tab_order:
            if tab_key in tab_configs:
                config = tab_configs[tab_key]
                tab_list.append({
                    "key": tab_key,
                    "title": config.tab_title,
                    "type": config.tab_type,
                    "active": config.is_active,
                    "data_count": config.data_count
                })
                
        return tab_list
        
    def set_tab_active(self, tab_key: str, active: bool) -> bool:
        """设置Tab激活状态"""
        return self._main_model.set_tab_active(tab_key, active)
        
    def get_current_tab_key(self) -> str:
        """获取当前激活的Tab键"""
        return self.current_tab_key
        
    def switch_to_tab(self, tab_key: str) -> bool:
        """切换到指定Tab"""
        tab_order = self._main_model.get_tab_order()
        if tab_key in tab_order:
            tab_index = tab_order.index(tab_key)
            if hasattr(self._main_view, 'tabWidget'):
                self._main_view.tabWidget.setCurrentIndex(tab_index)
                return True
        return False
        
    def export_tab_data(self, tab_key: str, format: str = "json") -> Optional[str]:
        """导出Tab数据"""
        data = self.get_tab_data(tab_key)
        if not data:
            return None
            
        if format.lower() == "json":
            import json
            return json.dumps(data, ensure_ascii=False, indent=2)
        elif format.lower() == "csv":
            import csv
            import io
            output = io.StringIO()
            if data:
                writer = csv.DictWriter(output, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
                return output.getvalue()
        
        return None
        
    def import_tab_data(self, tab_key: str, data_str: str, format: str = "json") -> bool:
        """导入Tab数据"""
        try:
            if format.lower() == "json":
                import json
                data = json.loads(data_str)
            elif format.lower() == "csv":
                import csv
                import io
                reader = csv.DictReader(io.StringIO(data_str))
                data = list(reader)
            else:
                return False
                
            return self.update_tab_data(tab_key, data)
            
        except Exception as e:
            self.error_occurred.emit(f"导入数据失败: {e}")
            return False
            
    def cleanup(self):
        """清理资源"""
        try:
            # 这里可以添加清理逻辑
            print("🧹 协同表格系统资源清理完成")
        except Exception as e:
            print(f"⚠️ 资源清理时出现问题: {e}")
            
    def __del__(self):
        """析构函数"""
        self.cleanup()