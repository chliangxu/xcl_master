from typing import Optional


class PermissionService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._repo = None

    @classmethod
    def get_instance(cls) -> "PermissionService":
        return cls()

    def _ensure_repo(self):
        if self._repo is None:
            from src.modules.permission_manager.model.permission_models import PermissionRepository
            self._repo = PermissionRepository.get_instance()
        return self._repo

    def _get_current_user_id(self) -> Optional[str]:
        """从DataService获取当前用户ID"""
        from src.core import DataService
        user_repo = DataService.get_instance().user_repository
        if user_repo:
            current_user = user_repo.get_current_user()
            return current_user.id if current_user else None
        return None

    def has_module_permission(self, module_key: str, user_id: Optional[str] = None) -> bool:
        uid = user_id or self._get_current_user_id()
        if not uid:
            return False
        return self._ensure_repo().has_module_permission(uid, module_key)

    def check_permission(self, module_key: str, user_id: Optional[str] = None,
                         show_message: bool = True) -> bool:
        has_permission = self.has_module_permission(module_key, user_id)

        if not has_permission and show_message:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(None, "权限不足",
                                f"您没有访问 '{module_key}' 模块的权限，请联系管理员。")

        return has_permission

    def get_user_modules(self, user_id: Optional[str] = None) -> set:
        uid = user_id or self._get_current_user_id()
        if not uid:
            return set()

        permission = self._ensure_repo().get_permission(uid)
        return permission.modules if permission else set()

    def reload_user_permissions(self, user_id: Optional[str] = None):
        uid = user_id or self._get_current_user_id()
        if uid:
            repo = self._ensure_repo()
            repo.clear_permission(uid)
            repo.load_user_permissions(uid)

    def load_current_user_permissions(self):
        """加载当前用户的权限"""
        user_id = self._get_current_user_id()
        if user_id:
            self._ensure_repo().load_user_permissions(user_id)
