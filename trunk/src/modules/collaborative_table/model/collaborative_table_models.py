"""
协同表格模型 - MVC架构中的模型层
负责数据管理和业务逻辑
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from PyQt5.QtCore import pyqtSignal

from src.common.base import BaseModel


class CollaborativeTableModel(BaseModel):
    """协同表格模型类"""
    
    # 定义信号
    data_changed = pyqtSignal()  # 数据变化
    operation_finished = pyqtSignal(str, bool, str)  # 操作完成 (操作名, 是否成功, 消息)
    error_occurred = pyqtSignal(str)  # 错误发生
    
    def __init__(self):
        super().__init__()
        self.items = []  # 存储所有项目数据
        self.locked_items = set()  # 存储锁定的项目ID
        self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 初始化测试数据
        self.init_test_data()
        
    def init_test_data(self):
        """初始化测试数据"""
        self.items = [
            {
                'id': '1011',
                'name': 'JPNZ-摩托车',
                'type': '载具',
                'owner': '张云龙',
                'modified_time': '2025-11-10 09:25',
                'status': 'normal',
                'locked': False
            },
            {
                'id': '1012',
                'name': 'JPNZ-摩托车',
                'type': '载具',
                'owner': '张云龙',
                'modified_time': '2025-11-10 09:25',
                'status': 'normal',
                'locked': False
            },
            {
                'id': '1013',
                'name': 'JPNZ-摩托车',
                'type': '载具',
                'owner': '张云龙',
                'modified_time': '2025-11-10 09:25',
                'status': 'error',
                'locked': False
            },
            {
                'id': '1014',
                'name': 'JPNZ-摩托车',
                'type': '载具',
                'owner': '张云龙',
                'modified_time': '2025-11-10 09:25',
                'status': 'warning',
                'locked': False
            },
            {
                'id': '1015',
                'name': 'JPNZ-摩托车',
                'type': '载具',
                'owner': '张云龙',
                'modified_time': '2025-11-10 09:25',
                'status': 'success',
                'locked': False
            },
        ]
        
    def get_items(self, filter_type: str = "", search_text: str = "", 
                  page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """获取项目列表
        
        Args:
            filter_type: 过滤类型
            search_text: 搜索文本
            page: 页码
            page_size: 页面大小
            
        Returns:
            包含items, total, last_update的字典
        """
        try:
            # 过滤数据
            filtered_items = self.items.copy()
            
            # 按类型过滤
            if filter_type and filter_type != "类型":
                filtered_items = [item for item in filtered_items 
                                if item['type'] == filter_type]
            
            # 按搜索文本过滤
            if search_text:
                search_text = search_text.lower()
                filtered_items = [item for item in filtered_items 
                                if search_text in item['name'].lower() or 
                                   search_text in item['id'].lower() or
                                   search_text in item['owner'].lower()]
            
            total = len(filtered_items)
            
            # 分页
            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            page_items = filtered_items[start_index:end_index]
            
            return {
                'items': page_items,
                'total': total,
                'last_update': self.last_update
            }
            
        except Exception as e:
            self.error_occurred.emit(f"获取数据失败: {str(e)}")
            return {'items': [], 'total': 0, 'last_update': self.last_update}
            
    def get_item_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取单个项目"""
        for item in self.items:
            if item['id'] == item_id:
                return item
        return None
        
    def add_item(self, item_data: Dict[str, Any]) -> bool:
        """添加新项目"""
        try:
            # 检查ID是否已存在
            if self.get_item_by_id(item_data['id']):
                self.error_occurred.emit("项目ID已存在")
                return False
                
            # 设置默认值
            item_data.setdefault('status', 'normal')
            item_data.setdefault('locked', False)
            item_data.setdefault('modified_time', 
                               datetime.now().strftime("%Y-%m-%d %H:%M"))
            
            self.items.append(item_data)
            self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.data_changed.emit()
            self.operation_finished.emit("添加", True, "项目添加成功")
            return True
            
        except Exception as e:
            self.error_occurred.emit(f"添加项目失败: {str(e)}")
            self.operation_finished.emit("添加", False, str(e))
            return False
            
    def update_item(self, item_id: str, item_data: Dict[str, Any]) -> bool:
        """更新项目"""
        try:
            for i, item in enumerate(self.items):
                if item['id'] == item_id:
                    # 检查是否被锁定
                    if item.get('locked', False):
                        self.error_occurred.emit("项目已被锁定，无法修改")
                        return False
                        
                    # 更新数据
                    self.items[i].update(item_data)
                    self.items[i]['modified_time'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    
                    self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M")
                    self.data_changed.emit()
                    self.operation_finished.emit("更新", True, "项目更新成功")
                    return True
                    
            self.error_occurred.emit("未找到指定项目")
            return False
            
        except Exception as e:
            self.error_occurred.emit(f"更新项目失败: {str(e)}")
            self.operation_finished.emit("更新", False, str(e))
            return False
            
    def delete_item(self, item_id: str) -> bool:
        """删除单个项目"""
        try:
            for i, item in enumerate(self.items):
                if item['id'] == item_id:
                    # 检查是否被锁定
                    if item.get('locked', False):
                        self.error_occurred.emit("项目已被锁定，无法删除")
                        return False
                        
                    self.items.pop(i)
                    self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M")
                    self.data_changed.emit()
                    self.operation_finished.emit("删除", True, "项目删除成功")
                    return True
                    
            self.error_occurred.emit("未找到指定项目")
            return False
            
        except Exception as e:
            self.error_occurred.emit(f"删除项目失败: {str(e)}")
            self.operation_finished.emit("删除", False, str(e))
            return False
            
    def delete_items(self, item_ids: List[str]) -> bool:
        """批量删除项目"""
        try:
            deleted_count = 0
            locked_items = []
            
            for item_id in item_ids:
                for i, item in enumerate(self.items):
                    if item['id'] == item_id:
                        if item.get('locked', False):
                            locked_items.append(item_id)
                        else:
                            self.items.pop(i)
                            deleted_count += 1
                        break
                        
            if locked_items:
                self.error_occurred.emit(f"以下项目已被锁定，无法删除: {', '.join(locked_items)}")
                
            if deleted_count > 0:
                self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.data_changed.emit()
                self.operation_finished.emit("批量删除", True, f"成功删除 {deleted_count} 个项目")
                return True
            else:
                self.operation_finished.emit("批量删除", False, "没有项目被删除")
                return False
                
        except Exception as e:
            self.error_occurred.emit(f"批量删除失败: {str(e)}")
            self.operation_finished.emit("批量删除", False, str(e))
            return False
            
    def lock_item(self, item_id: str) -> bool:
        """锁定单个项目"""
        try:
            for item in self.items:
                if item['id'] == item_id:
                    item['locked'] = True
                    self.locked_items.add(item_id)
                    self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M")
                    self.data_changed.emit()
                    self.operation_finished.emit("锁定", True, "项目锁定成功")
                    return True
                    
            self.error_occurred.emit("未找到指定项目")
            return False
            
        except Exception as e:
            self.error_occurred.emit(f"锁定项目失败: {str(e)}")
            self.operation_finished.emit("锁定", False, str(e))
            return False
            
    def lock_items(self, item_ids: List[str]) -> bool:
        """批量锁定项目"""
        try:
            locked_count = 0
            
            for item_id in item_ids:
                for item in self.items:
                    if item['id'] == item_id:
                        item['locked'] = True
                        self.locked_items.add(item_id)
                        locked_count += 1
                        break
                        
            if locked_count > 0:
                self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.data_changed.emit()
                self.operation_finished.emit("批量锁定", True, f"成功锁定 {locked_count} 个项目")
                return True
            else:
                self.operation_finished.emit("批量锁定", False, "没有项目被锁定")
                return False
                
        except Exception as e:
            self.error_occurred.emit(f"批量锁定失败: {str(e)}")
            self.operation_finished.emit("批量锁定", False, str(e))
            return False
            
    def unlock_item(self, item_id: str) -> bool:
        """解锁单个项目"""
        try:
            for item in self.items:
                if item['id'] == item_id:
                    item['locked'] = False
                    self.locked_items.discard(item_id)
                    self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M")
                    self.data_changed.emit()
                    self.operation_finished.emit("解锁", True, "项目解锁成功")
                    return True
                    
            self.error_occurred.emit("未找到指定项目")
            return False
            
        except Exception as e:
            self.error_occurred.emit(f"解锁项目失败: {str(e)}")
            self.operation_finished.emit("解锁", False, str(e))
            return False
            
    def copy_item(self, item_id: str) -> bool:
        """复制单个项目"""
        try:
            source_item = self.get_item_by_id(item_id)
            if not source_item:
                self.error_occurred.emit("未找到源项目")
                return False
                
            # 创建副本
            new_item = source_item.copy()
            new_item['id'] = f"{item_id}_copy_{len(self.items) + 1}"
            new_item['name'] = f"{source_item['name']}_副本"
            new_item['locked'] = False
            new_item['modified_time'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            self.items.append(new_item)
            self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.data_changed.emit()
            self.operation_finished.emit("复制", True, "项目复制成功")
            return True
            
        except Exception as e:
            self.error_occurred.emit(f"复制项目失败: {str(e)}")
            self.operation_finished.emit("复制", False, str(e))
            return False
            
    def copy_items(self, item_ids: List[str]) -> bool:
        """批量复制项目"""
        try:
            copied_count = 0
            
            for item_id in item_ids:
                if self.copy_item(item_id):
                    copied_count += 1
                    
            if copied_count > 0:
                self.operation_finished.emit("批量复制", True, f"成功复制 {copied_count} 个项目")
                return True
            else:
                self.operation_finished.emit("批量复制", False, "没有项目被复制")
                return False
                
        except Exception as e:
            self.error_occurred.emit(f"批量复制失败: {str(e)}")
            self.operation_finished.emit("批量复制", False, str(e))
            return False
            
    def submit_items(self, item_ids: List[str]) -> bool:
        """提交项目"""
        try:
            submitted_count = 0
            locked_items = []
            
            for item_id in item_ids:
                for item in self.items:
                    if item['id'] == item_id:
                        if item.get('locked', False):
                            locked_items.append(item_id)
                        else:
                            # 标记为已提交状态
                            item['status'] = 'submitted'
                            item['modified_time'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                            submitted_count += 1
                        break
                        
            if locked_items:
                self.error_occurred.emit(f"以下项目已被锁定，无法提交: {', '.join(locked_items)}")
                
            if submitted_count > 0:
                self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.data_changed.emit()
                self.operation_finished.emit("提交", True, f"成功提交 {submitted_count} 个项目")
                return True
            else:
                self.operation_finished.emit("提交", False, "没有项目被提交")
                return False
                
        except Exception as e:
            self.error_occurred.emit(f"提交失败: {str(e)}")
            self.operation_finished.emit("提交", False, str(e))
            return False
    
    def view_item(self, item_id: str):
        """查看项目详情"""
        # 这里可以触发打开详情页面的信号
        item = self.get_item_by_id(item_id)
        if item:
            # 可以发送信号给控制器，让其打开详情页面
            print(f"查看项目详情: {item}")
        else:
            self.error_occurred.emit("未找到指定项目")
            
    def export_items(self, filter_type: str = "", search_text: str = "", 
                    format_type: str = "excel") -> bool:
        """导出项目数据"""
        try:
            # 获取过滤后的数据
            data = self.get_items(filter_type, search_text, 1, 9999)  # 获取所有数据
            items = data['items']
            
            if not items:
                self.error_occurred.emit("没有数据可导出")
                return False
                
            # 这里可以实现具体的导出逻辑
            # 比如导出到Excel、CSV等格式
            print(f"导出 {len(items)} 个项目到 {format_type} 格式")
            
            self.operation_finished.emit("导出", True, f"成功导出 {len(items)} 个项目")
            return True
            
        except Exception as e:
            self.error_occurred.emit(f"导出失败: {str(e)}")
            self.operation_finished.emit("导出", False, str(e))
            return False
            
    def import_items(self, file_path: str) -> bool:
        """导入项目数据"""
        try:
            # 这里可以实现具体的导入逻辑
            # 比如从Excel、CSV等格式导入
            print(f"从 {file_path} 导入数据")
            
            # 示例：添加一些测试数据
            imported_count = 0
            # 这里应该解析文件并添加数据
            
            if imported_count > 0:
                self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.data_changed.emit()
                self.operation_finished.emit("导入", True, f"成功导入 {imported_count} 个项目")
                return True
            else:
                self.operation_finished.emit("导入", False, "没有数据被导入")
                return False
                
        except Exception as e:
            self.error_occurred.emit(f"导入失败: {str(e)}")
            self.operation_finished.emit("导入", False, str(e))
            return False
            
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        try:
            total = len(self.items)
            locked = len(self.locked_items)
            
            # 按状态统计
            status_count = {}
            type_count = {}
            
            for item in self.items:
                status = item.get('status', 'normal')
                item_type = item.get('type', '未知')
                
                status_count[status] = status_count.get(status, 0) + 1
                type_count[item_type] = type_count.get(item_type, 0) + 1
                
            return {
                'total': total,
                'locked': locked,
                'status_count': status_count,
                'type_count': type_count,
                'last_update': self.last_update
            }
            
        except Exception as e:
            self.error_occurred.emit(f"获取统计信息失败: {str(e)}")
            return {}
            
    def update_data(self, data: List[Dict[str, Any]]) -> bool:
        """更新所有数据"""
        try:
            self.items = data.copy()
            self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.data_changed.emit()
            print(f"✅ 更新数据成功: {len(data)} 条记录")
            return True
        except Exception as e:
            error_msg = f"更新数据失败: {str(e)}"
            print(f"❌ {error_msg}")
            self.error_occurred.emit(error_msg)
            return False
            
    def get_all_data(self) -> List[Dict[str, Any]]:
        """获取所有数据"""
        return self.items.copy()
        
    def search_items(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索项目"""
        if not keyword:
            return []
            
        results = []
        keyword_lower = keyword.lower()
        
        for item in self.items:
            # 在名称、类型、拥有者中搜索
            if (keyword_lower in item.get('name', '').lower() or
                keyword_lower in item.get('type', '').lower() or
                keyword_lower in item.get('owner', '').lower() or
                keyword_lower in item.get('id', '').lower()):
                results.append(item)
                
        return results