"""
协同表格控制器 - MVC架构中的控制器层
处理视图和模型之间的交互逻辑
"""

from PyQt5.QtCore import QObject, pyqtSignal
from typing import Dict, Optional, List, Any

from src.common.base import BaseController
from src.modules.collaborative_table.model.collaborative_table_models import CollaborativeTableModel
from src.modules.collaborative_table.view.collaborative_table_view import CollaborativeTableView

class CollaborativeTableController(BaseController):
    """协同表格控制器类"""
    
    # 定义业务信号
    data_updated = pyqtSignal(list)  # 数据更新
    status_updated = pyqtSignal(int, str)  # 状态更新 (总数, 更新时间)
    operation_completed = pyqtSignal(str, bool)  # 操作完成 (操作名, 是否成功)
    
    def __init__(self):
        super().__init__()
        self.current_filter = "类型"
        self.current_search = ""
        self.current_page = 1
        self.page_size = 20
        self._model = CollaborativeTableModel()
        self._view = CollaborativeTableView()
        self.set_model(self._model)
        self.set_view(self._view)
        
    def set_model(self, model: CollaborativeTableModel) -> None:
        """设置模型"""
        self._model = model
        if model:
            # 连接模型信号
            model.data_changed.connect(self.on_data_changed)
            model.operation_finished.connect(self.on_operation_finished)
            model.error_occurred.connect(self.on_model_error)
            
    def set_view(self, view: CollaborativeTableView) -> None:
        """设置视图"""
        self._view = view
        if view:
            # 连接视图信号
            view.item_action_triggered.connect(self.handle_item_action)
            view.search_triggered.connect(self.handle_search)
            view.filter_changed.connect(self.handle_filter_change)
            view.page_changed.connect(self.handle_page_change)
            view.item_selected.connect(self.handle_item_selection)
            
            # 连接新增的批量操作信号
            if hasattr(view, 'batch_action_triggered'):
                view.batch_action_triggered.connect(self.handle_batch_action)
            
            # 连接控制器信号到视图
            self.data_updated.connect(view.update_data)
            self.status_updated.connect(view.update_status_info)
        
    def initialize(self) -> bool:
        """初始化控制器"""
        try:
            self.load_data()
            return True
        except Exception as e:
            self.error_occurred.emit(f"初始化失败: {str(e)}")
            return False
        
    def load_data(self, page: int = 1) -> None:
        """加载数据"""
        if not self._model:
            return
            
        try:
            self.current_page = page
            # 从模型获取数据
            data = self._model.get_items(
                filter_type=self.current_filter,
                search_text=self.current_search,
                page=self.current_page,
                page_size=self.page_size
            )
            
            if data:
                self.data_updated.emit(data['items'])
                
                # 更新分页信息
                if self._view:
                    total_pages = (data['total'] + self.page_size - 1) // self.page_size
                    self._view.set_total_pages(total_pages)
                    
                # 更新状态信息 
                self.status_updated.emit(data['total'], data.get('last_update', ''))
                
        except Exception as e:
            self.error_occurred.emit(f"加载数据失败: {str(e)}")
            
    def handle_item_action(self, action: str, row: int, item_id: str) -> None:
        """处理项目操作"""
        if not self._model:
            return
            
        try:
            if action == "delete":
                if "," in item_id:  # 批量删除
                    ids = item_id.split(",")
                    success = self._model.delete_items(ids)
                else:  # 单个删除
                    success = self._model.delete_item(item_id)
                    
                if success:
                    self.operation_completed.emit("删除", True)
                    self.load_data(self.current_page)  # 重新加载数据
                else:
                    self.operation_completed.emit("删除", False)
                    
            elif action == "lock":
                if "," in item_id:  # 批量锁定
                    ids = item_id.split(",")
                    success = self._model.lock_items(ids)
                else:  # 单个锁定
                    success = self._model.lock_item(item_id)
                    
                if success:
                    self.operation_completed.emit("锁定", True)
                    self.load_data(self.current_page)
                else:
                    self.operation_completed.emit("锁定", False)
                    
            elif action == "copy":
                if "," in item_id:  # 批量复制
                    ids = item_id.split(",")
                    success = self._model.copy_items(ids)
                else:  # 单个复制
                    success = self._model.copy_item(item_id)
                    
                if success:
                    self.operation_completed.emit("复制", True)
                    self.load_data(self.current_page)
                else:
                    self.operation_completed.emit("复制", False)
                    
            elif action == "view":
                # 查看操作，打开详情页面
                self._model.view_item(item_id)
                
        except Exception as e:
            self.error_occurred.emit(f"操作失败: {str(e)}")
            
    def handle_search(self, search_text: str) -> None:
        """处理搜索"""
        self.current_search = search_text
        self.current_page = 1  # 搜索时重置到第一页
        self.load_data(self.current_page)
        
    def handle_filter_change(self, filter_type: str) -> None:
        """处理过滤器变化"""
        if filter_type in ["全部", "类型"]:
            filter_type = ""  # 空字符串表示不过滤
        self.current_filter = filter_type
        self.current_page = 1  # 过滤时重置到第一页
        self.load_data(self.current_page)
        
    def handle_page_change(self, page: int) -> None:
        """处理页面变化"""
        self.load_data(page)
        
    def handle_item_selection(self, selected_items: List[str]) -> None:
        """处理项目选择"""
        # 可以在这里处理选择逻辑，比如更新工具栏状态
        if self._view:
            # 根据选择状态更新UI
            has_selection = len(selected_items) > 0
            # 这里可以启用/禁用批量操作按钮等
            pass
    
    def handle_batch_action(self, action: str, item_ids: List[str]) -> None:
        """处理批量操作"""
        if not self._model or not item_ids:
            return
            
        try:
            success = False
            
            if action == "delete":
                success = self._model.delete_items(item_ids)
            elif action == "lock":
                success = self._model.lock_items(item_ids)
            elif action == "copy":
                success = self._model.copy_items(item_ids)
            elif action == "submit":
                success = self._model.submit_items(item_ids)
            elif action == "export":
                success = self._model.export_items(item_ids)
            
            if success:
                self.operation_completed.emit(f"批量{action}", True)
                self.load_data(self.current_page)  # 重新加载数据
            else:
                self.operation_completed.emit(f"批量{action}", False)
                
        except Exception as e:
            self.error_occurred.emit(f"批量操作失败: {str(e)}")
            
    def refresh_data(self) -> None:
        """刷新数据"""
        self.load_data(self.current_page)
        
    def export_data(self, format_type: str = "excel") -> bool:
        """导出数据"""
        if not self._model:
            return False
            
        try:
            success = self._model.export_items(
                filter_type=self.current_filter,
                search_text=self.current_search,
                format_type=format_type
            )
            
            if success:
                self.operation_completed.emit("导出", True)
            else:
                self.operation_completed.emit("导出", False)
                
            return success
            
        except Exception as e:
            self.error_occurred.emit(f"导出失败: {str(e)}")
            return False
            
    def import_data(self, file_path: str) -> bool:
        """导入数据"""
        if not self._model:
            return False
            
        try:
            success = self._model.import_items(file_path)
            
            if success:
                self.operation_completed.emit("导入", True)
                self.load_data(self.current_page)  # 重新加载数据
            else:
                self.operation_completed.emit("导入", False)
                
            return success
            
        except Exception as e:
            self.error_occurred.emit(f"导入失败: {str(e)}")
            return False
            
    # 模型事件处理
    def on_data_changed(self) -> None:
        """模型数据变化时的处理"""
        self.load_data(self.current_page)
        
    def on_operation_finished(self, operation: str, success: bool, message: str = "") -> None:
        """模型操作完成时的处理"""
        self.operation_completed.emit(operation, success)
        if not success and message:
            self.error_occurred.emit(message)
            
    def on_model_error(self, error_message: str) -> None:
        """模型错误时的处理"""
        self.error_occurred.emit(error_message)
        
    def get_current_filter_info(self) -> Dict[str, Any]:
        """获取当前过滤信息"""
        return {
            'filter_type': self.current_filter,
            'search_text': self.current_search,
            'page': self.current_page,
            'page_size': self.page_size
        }
        
    def set_page_size(self, page_size: int) -> None:
        """设置页面大小"""
        self.page_size = page_size
        self.current_page = 1  # 重置到第一页
        self.load_data(self.current_page)