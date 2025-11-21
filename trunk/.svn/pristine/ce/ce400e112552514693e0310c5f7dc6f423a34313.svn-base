from src.core import ModuleManager


def register_all_modules():
    from src.modules.login.controller.login_controller import LoginController
    from src.modules.project.controller.project_controller import ProjectController
    from src.modules.tools.controller.tools_controller import ToolsController
    from src.modules.permission_manager.controller.permission_manager_controller import PermissionManagerController
    from src.modules.task.controller.task_controller import TaskController
    from src.modules.notification.controller.notification_controller import NotificationController
    from src.modules.version_info.controller.version_info_controller import VersionInfoController
    from src.modules.collaborative_table.controller.collaborative_table_main_controller import CollaborativeTableMainController

    modules = [
        {
            "module_key": "Login",
            "name": "登录模块",
            "icon": "🔑",
            "controller_class": LoginController,
            "order": 0,
            "visible": False
        },
        {
            "module_key": "Project",
            "name": "工程模块",
            "icon": "📁",
            "controller_class": ProjectController,
            "order": 1
        },
        {
            "module_key": "Tools",
            "name": "工具模块",
            "icon": "🔧",
            "controller_class": ToolsController,
            "order": 2
        },
        {
            "module_key": "PermissionManager",
            "name": "权限管理",
            "icon": "🔐",
            "controller_class": PermissionManagerController,
            "order": 3
        },
        {
            "module_key": "Task",
            "name": "任务模块",
            "icon": "📋",
            "controller_class": TaskController,
            "order": 4
        },
        {
            "module_key": "Notification",
            "name": "通知模块",
            "icon": "🔔",
            "controller_class": NotificationController,
            "order": 5
        },
        {
            "module_key": "VersionInfo",
            "name": "版本信息",
            "icon": "ℹ️",
            "controller_class": VersionInfoController,
            "order": 6
        },
        {
            "module_key": "CollaborativeSheet",
            "name": "协同表格",
            "icon": "📊",
            "controller_class": CollaborativeTableMainController,
            "order": 7
        },
    ]

    for module in modules:
        ModuleManager.register(**module)
