"""
协同表格主模型 - 管理多个Tab的数据模型
"""

from PyQt5.QtCore import QObject, pyqtSignal
from typing import Dict, List, Optional, Any
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from src.common.base import BaseModel
from .collaborative_table_models import CollaborativeTableModel


@dataclass
class TabConfig:
    """Tab配置信息"""
    tab_key: str
    tab_title: str
    tab_type: str = "default"  # default, custom, archive
    created_time: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    data_count: int = 0
    last_updated: datetime = field(default_factory=datetime.now)


class CollaborativeTableMainModel(BaseModel):
    """协同表格主模型类 - 管理多个Tab页面的数据"""
    
    # 定义信号
    tab_config_changed = pyqtSignal(str, dict)  # Tab配置变化 (tab_key, config)
    tab_data_updated = pyqtSignal(str, list)    # Tab数据更新 (tab_key, data)
    tabs_reordered = pyqtSignal(list)           # Tab重新排序 (new_order)
    
    def __init__(self):
        super().__init__()
        self.tab_configs: Dict[str, TabConfig] = {}
        self.tab_models: Dict[str, CollaborativeTableModel] = {}
        self.tab_order: List[str] = []
        
        # 初始化默认Tab配置
        self._init_default_tabs()
        
    def _init_default_tabs(self):
        """初始化默认Tab配置"""
        default_tabs = [
            {"key": "item", "title": "物品表", "type": "default"},
        ]
        
        for tab_info in default_tabs:
            self.add_tab_config(
                tab_info["key"], 
                tab_info["title"], 
                tab_info["type"]
            )
            
    def add_tab_config(self, tab_key: str, tab_title: str, tab_type: str = "default") -> bool:
        """添加Tab配置"""
        if tab_key in self.tab_configs:
            print(f"⚠️ Tab键 '{tab_key}' 已存在")
            return False
            
        # 创建Tab配置
        config = TabConfig(
            tab_key=tab_key,
            tab_title=tab_title,
            tab_type=tab_type
        )
        
        # 创建对应的数据模型
        tab_model = CollaborativeTableModel()
        
        # 存储配置和模型
        self.tab_configs[tab_key] = config
        self.tab_models[tab_key] = tab_model
        self.tab_order.append(tab_key)
        
        # 连接Tab模型信号
        tab_model.data_changed.connect(
            lambda: self._on_tab_data_changed(tab_key, tab_model.get_all_data())
        )
        
        print(f"✅ 添加Tab配置: '{tab_title}' (键: {tab_key})")
        self.tab_config_changed.emit(tab_key, config.__dict__)
        
        return True
        
    def remove_tab_config(self, tab_key: str) -> bool:
        """移除Tab配置"""
        if tab_key not in self.tab_configs:
            print(f"❌ Tab键 '{tab_key}' 不存在")
            return False
            
        # 移除配置和模型
        config = self.tab_configs.pop(tab_key)
        self.tab_models.pop(tab_key)
        
        # 从排序列表中移除
        if tab_key in self.tab_order:
            self.tab_order.remove(tab_key)
            
        print(f"✅ 移除Tab配置: '{config.tab_title}' (键: {tab_key})")
        self.tabs_reordered.emit(self.tab_order.copy())
        
        return True
        
    def get_tab_config(self, tab_key: str) -> Optional[TabConfig]:
        """获取Tab配置"""
        return self.tab_configs.get(tab_key)
        
    def get_tab_model(self, tab_key: str) -> Optional[CollaborativeTableModel]:
        """获取Tab数据模型"""
        return self.tab_models.get(tab_key)
        
    def get_all_tab_configs(self) -> Dict[str, TabConfig]:
        """获取所有Tab配置"""
        return self.tab_configs.copy()
        
    def get_tab_order(self) -> List[str]:
        """获取Tab顺序"""
        return self.tab_order.copy()
        
    def reorder_tabs(self, new_order: List[str]) -> bool:
        """重新排序Tab"""
        # 验证新顺序包含所有现有Tab
        if set(new_order) != set(self.tab_order):
            print("❌ 新顺序包含无效的Tab键")
            return False
            
        self.tab_order = new_order.copy()
        print(f"✅ Tab重新排序: {new_order}")
        self.tabs_reordered.emit(self.tab_order.copy())
        
        return True
        
    def update_tab_title(self, tab_key: str, new_title: str) -> bool:
        """更新Tab标题"""
        if tab_key not in self.tab_configs:
            return False
            
        config = self.tab_configs[tab_key]
        old_title = config.tab_title
        config.tab_title = new_title
        config.last_updated = datetime.now()
        
        print(f"✅ 更新Tab标题: '{old_title}' -> '{new_title}'")
        self.tab_config_changed.emit(tab_key, config.__dict__)
        
        return True
        
    def set_tab_active(self, tab_key: str, active: bool) -> bool:
        """设置Tab激活状态"""
        if tab_key not in self.tab_configs:
            return False
            
        config = self.tab_configs[tab_key]
        config.is_active = active
        config.last_updated = datetime.now()
        
        print(f"✅ 设置Tab状态: '{config.tab_title}' -> {'激活' if active else '禁用'}")
        self.tab_config_changed.emit(tab_key, config.__dict__)
        
        return True
        
    def update_tab_data(self, tab_key: str, data: List[Dict[str, Any]]) -> bool:
        """更新Tab数据"""
        if tab_key not in self.tab_models:
            return False
            
        tab_model = self.tab_models[tab_key]
        tab_model.update_data(data)
        
        # 更新配置中的数据计数
        if tab_key in self.tab_configs:
            config = self.tab_configs[tab_key]
            config.data_count = len(data)
            config.last_updated = datetime.now()
            self.tab_config_changed.emit(tab_key, config.__dict__)
            
        return True
        
    def get_tab_data(self, tab_key: str) -> List[Dict[str, Any]]:
        """获取Tab数据"""
        if tab_key not in self.tab_models:
            return []
            
        tab_model = self.tab_models[tab_key]
        return tab_model.get_all_data()
        
    def get_tab_statistics(self) -> Dict[str, Any]:
        """获取Tab统计信息"""
        stats = {
            "total_tabs": len(self.tab_configs),
            "active_tabs": sum(1 for config in self.tab_configs.values() if config.is_active),
            "total_records": sum(config.data_count for config in self.tab_configs.values()),
            "tab_types": {}
        }
        
        # 统计Tab类型
        for config in self.tab_configs.values():
            tab_type = config.tab_type
            if tab_type not in stats["tab_types"]:
                stats["tab_types"][tab_type] = 0
            stats["tab_types"][tab_type] += 1
            
        return stats
        
    def search_across_tabs(self, keyword: str) -> Dict[str, List[Dict[str, Any]]]:
        """跨Tab搜索"""
        results = {}
        
        for tab_key, tab_model in self.tab_models.items():
            if hasattr(tab_model, 'search_items'):
                tab_results = tab_model.search_items(keyword)
                if tab_results:
                    results[tab_key] = tab_results
                    
        return results
        
    def _on_tab_data_changed(self, tab_key: str, data: List[Dict[str, Any]]):
        """Tab数据变化处理"""
        # 更新配置中的数据计数
        if tab_key in self.tab_configs:
            config = self.tab_configs[tab_key]
            config.data_count = len(data)
            config.last_updated = datetime.now()
            
        # 发出信号
        self.tab_data_updated.emit(tab_key, data)
        
    def clear_all_tabs(self):
        """清空所有Tab"""
        self.tab_configs.clear()
        self.tab_models.clear()
        self.tab_order.clear()
        
        print("✅ 清空所有Tab配置")
        self.tabs_reordered.emit([])
        
    def load_sample_data_for_tab(self, tab_key: str):
        """为指定Tab加载示例数据"""
        if tab_key not in self.tab_models:
            return False
            
        # 根据Tab类型生成不同的示例数据
        config = self.tab_configs[tab_key]
        sample_data = []
        
        if config.tab_type == "default":
            sample_data = [
                {"id": f"{tab_key}_001", "name": f"{config.tab_title}项目1", "type": "载具", "owner": "张三", "status": "进行中"},
                {"id": f"{tab_key}_002", "name": f"{config.tab_title}项目2", "type": "武器", "owner": "李四", "status": "已完成"},
                {"id": f"{tab_key}_003", "name": f"{config.tab_title}项目3", "type": "道具", "owner": "王五", "status": "待开始"},
            ]
        elif config.tab_type == "archive":
            sample_data = [
                {"id": f"{tab_key}_arc_001", "name": f"归档项目1", "type": "载具", "owner": "赵六", "status": "已归档"},
                {"id": f"{tab_key}_arc_002", "name": f"归档项目2", "type": "材料", "owner": "孙七", "status": "已归档"},
            ]
        else:
            sample_data = [
                {"id": f"{tab_key}_custom_001", "name": f"自定义项目1", "type": "其他", "owner": "用户A", "status": "自定义"},
            ]
            
        return self.update_tab_data(tab_key, sample_data)