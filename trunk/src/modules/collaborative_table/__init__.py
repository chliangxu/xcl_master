"""
协同表格模块 - MVC架构实现

包含以下组件：
- CollaborativeTableView: 主视图类（继承自BaseWidget）
- CollaborativeTableMainView: 主界面视图类（继承自BaseWidget）
- CollaborativeTableController: 控制器类（继承自BaseController）
- CollaborativeTableMainController: 主控制器类（继承自BaseController，同时作为模块入口）
- CollaborativeTableModel: 模型类（继承自BaseModel）
- CollaborativeTableMainModel: 主模型类

使用方法：
```python
from src.modules.collaborative_table import CollaborativeTableMain

# 创建主入口（实际是主控制器）
main_system = CollaborativeTableMain()

# 初始化系统
main_system.initialize()

# 获取主视图用于嵌入到其他窗口
main_view = main_system.get_main_view()
```
"""

from .model import CollaborativeTableModel, CollaborativeTableMainModel
from .controller import CollaborativeTableController, CollaborativeTableMainController
from .view import CollaborativeTableView, CollaborativeTableMainView

# 使用控制器作为主入口
CollaborativeTableMain = CollaborativeTableMainController

__all__ = [
    'CollaborativeTableModel',
    'CollaborativeTableMainModel',
    'CollaborativeTableController',
    'CollaborativeTableMainController',
    'CollaborativeTableView',
    'CollaborativeTableMainView',
]