from src.common.base import BaseController
from src.common.utils import ThreadManager
from src.core.event import EventSystem
from src.modules.permission_manager.view.permission_module_view import PermissionModuleView
from src.modules.permission_manager.model.permission_models import PermissionRepository
from src.core import DataService
from .permission_events import PermissionEvents
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl


class PermissionManagerController(BaseController):
    MODULE_KEY = "PermissionManager"

    def __init__(self):
        super().__init__()
        self._permission_repo = PermissionRepository.get_instance()
        self._module_view = None
        self._current_group_id = None
        self._thread_manager = ThreadManager()
        self._register_events()

    def _get_current_user_id(self):
        user_repo = DataService.get_instance().user_repository
        if user_repo:
            current_user = user_repo.get_current_user()
            return current_user.id if current_user else None
        return None

    def get_module_view(self):
        if not self._module_view:
            self._module_view = PermissionModuleView()
            self._module_view.show_loading()
            self._thread_manager.run_in_thread(
                self._async_load_initial_data,
                on_finished=self._on_initial_data_loaded
            )
        return self._module_view

    def _async_load_initial_data(self):
        self._load_current_user_permissions()
        self._load_all_groups()
        return None

    def _on_initial_data_loaded(self, result):
        if self._module_view:
            self._module_view.hide_loading()

    def _register_events(self):
        event_system = EventSystem.instance()
        event_system.register_event(PermissionEvents.PERMISSION_CHANGED, self._load_current_user_permissions)
        event_system.register_event(PermissionEvents.GROUP_SELECTED, self._on_group_selected)
        event_system.register_event(PermissionEvents.GROUP_CREATE_REQUESTED, self._on_create_group)
        event_system.register_event(PermissionEvents.USER_ADD_TO_GROUP_REQUESTED, self._on_add_user_button_clicked)
        event_system.register_event(PermissionEvents.USER_ADDED_TO_GROUP, self._on_add_user_to_group)
        event_system.register_event(PermissionEvents.USER_REMOVE_FROM_GROUP_REQUESTED, self._on_remove_user_from_group)
        event_system.register_event(PermissionEvents.GROUP_PERMISSION_UPDATE_REQUESTED,
                                    self._on_update_group_permissions)
        event_system.register_event(PermissionEvents.THIRD_PARTY_URL_OPEN_REQUESTED, self._on_open_third_party_url)

    def _load_current_user_permissions(self, data=None):
        self._thread_manager.run_in_thread(
            self._async_load_current_user_permissions,
            on_finished=self._on_current_user_permissions_loaded
        )

    def _async_load_current_user_permissions(self):
        user_id = self._get_current_user_id()
        if not user_id:
            return None

        user_groups = self._permission_repo.get_user_groups(user_id)
        permission = self._permission_repo.get_permission(user_id)
        if not permission:
            permission = self._permission_repo.load_user_permissions(user_id)
        user_permissions = permission.modules if permission else set()
        all_modules = self._permission_repo.get_all_modules()

        return {
            'user_id': user_id,
            'groups': [g.group_name for g in user_groups],
            'permissions': user_permissions,
            'all_modules': all_modules
        }

    def _on_current_user_permissions_loaded(self, result):
        if result and self._module_view:
            self._module_view.display_user_info(result['user_id'], result['groups'])
            self._module_view.display_permissions(result['all_modules'], result['permissions'])

    def _load_all_groups(self):
        self._thread_manager.run_in_thread(
            self._async_load_all_groups,
            on_finished=self._on_all_groups_loaded
        )

    def _async_load_all_groups(self):
        groups = self._permission_repo.get_all_user_groups()
        return [{
            'id': g.id,
            'name': g.group_name,
            'description': g.description,
            'user_count': g.user_count,
            'permission_count': len(g.module_permissions)
        } for g in groups]

    def _on_all_groups_loaded(self, groups):
        if groups and self._module_view:
            self._module_view.display_groups(groups)

    def _on_group_selected(self, group_id):
        self._current_group_id = group_id
        if self._module_view:
            self._module_view.set_current_group_id(group_id)
            self._module_view.show_detail_loading()

        self._thread_manager.run_in_thread(
            lambda: self._async_load_group_detail(group_id),
            on_finished=self._on_group_detail_loaded
        )

    def _async_load_group_detail(self, group_id):
        groups = self._permission_repo.get_all_user_groups()
        group = next((g for g in groups if g.id == group_id), None)
        users = self._permission_repo.get_group_users(group_id)
        all_modules = self._permission_repo.get_all_modules()

        return {
            'group_id': group_id,
            'group_name': group.group_name if group else '',
            'users': [{'user_id': u} for u in users],
            'all_modules': all_modules,
            'module_permissions': group.module_permissions if group else set()
        }

    def _on_group_detail_loaded(self, result):
        if result and self._module_view:
            self._module_view.display_group_detail(result['group_name'])
            self._module_view.display_group_users(result['users'])
            self._module_view.render_group_permissions(result['all_modules'], result['module_permissions'])
            self._module_view.hide_detail_loading()

    def _on_create_group(self, data):
        name = data.get('name')
        description = data.get('description', '')
        self._thread_manager.run_in_thread(
            lambda: self._async_create_group(name, description),
            on_finished=self._on_group_created
        )

    def _async_create_group(self, name, description):
        success = self._permission_repo.create_user_group(name, description)
        return {'success': success, 'group_name': name}

    def _on_group_created(self, result):
        if self._module_view:
            msg_func = QMessageBox.information if result['success'] else QMessageBox.critical
            msg_text = "创建成功" if result['success'] else "创建失败"
            msg_func(self._module_view, "成功" if result['success'] else "错误",
                     f"用户组 '{result['group_name']}' {msg_text}")
            if result['success']:
                self._load_all_groups()

    def _on_add_user_button_clicked(self, group_id):
        self._thread_manager.run_in_thread(
            lambda: self._async_get_available_users(group_id),
            on_finished=self._on_available_users_loaded
        )

    def _async_get_available_users(self, group_id):
        all_users = self._permission_repo.get_all_users()
        group_users = self._permission_repo.get_group_users(group_id)
        available = [u for u in all_users if u not in group_users]
        return available

    def _on_available_users_loaded(self, available_users):
        if self._module_view:
            if not available_users:
                QMessageBox.information(self._module_view, "提示", "没有可添加的用户")
                return
            self._module_view.show_user_selection_dialog(available_users)

    def _on_add_user_to_group(self, data):
        user_id = data.get('user_id')
        group_id = data.get('group_id')
        self._thread_manager.run_in_thread(
            lambda: self._async_add_user_to_group(user_id, group_id),
            on_finished=lambda result: self._on_user_added(result, user_id)
        )

    def _async_add_user_to_group(self, user_id, group_id):
        return self._permission_repo.add_user_to_group(user_id, group_id)

    def _on_user_added(self, success, user_id):
        if self._module_view:
            msg_func = QMessageBox.information if success else QMessageBox.critical
            msg_text = "添加成功" if success else "添加失败"
            msg_func(self._module_view, "成功" if success else "错误",
                     f"用户 '{user_id}' {msg_text}")
            if success and self._current_group_id:
                self._thread_manager.run_in_thread(
                    lambda: self._async_refresh_group_users(self._current_group_id),
                    on_finished=lambda users: self._module_view.display_group_users(
                        users) if self._module_view else None
                )

    def _async_refresh_group_users(self, group_id):
        users = self._permission_repo.get_group_users(group_id)
        return [{'user_id': u} for u in users]

    def _on_remove_user_from_group(self, data):
        user_id = data.get('user_id')
        group_id = data.get('group_id')
        self._thread_manager.run_in_thread(
            lambda: self._async_remove_user_from_group(user_id, group_id),
            on_finished=lambda result: self._on_user_removed(result, user_id)
        )

    def _async_remove_user_from_group(self, user_id, group_id):
        return self._permission_repo.remove_user_from_group(user_id, group_id)

    def _on_user_removed(self, success, user_id):
        if self._module_view:
            msg_func = QMessageBox.information if success else QMessageBox.critical
            msg_text = "移除成功" if success else "移除失败"
            msg_func(self._module_view, "成功" if success else "错误",
                     f"用户 '{user_id}' {msg_text}")
            if success and self._current_group_id:
                self._thread_manager.run_in_thread(
                    lambda: self._async_refresh_group_users(self._current_group_id),
                    on_finished=lambda users: self._module_view.display_group_users(
                        users) if self._module_view else None
                )

    def _on_update_group_permissions(self, data):
        group_id = data.get('group_id')
        module_ids = data.get('module_ids', [])
        self._thread_manager.run_in_thread(
            lambda: self._async_update_group_permissions(group_id, module_ids),
            on_finished=self._on_group_permissions_updated
        )

    def _async_update_group_permissions(self, group_id, module_ids):
        success = self._permission_repo.update_group_permissions(group_id, module_ids)
        return {'success': success, 'group_id': group_id}

    def _on_group_permissions_updated(self, result):
        if self._module_view:
            msg_func = QMessageBox.information if result['success'] else QMessageBox.critical
            msg_text = "保存成功" if result['success'] else "保存失败"
            msg_func(self._module_view, "成功" if result['success'] else "错误",
                     f"权限配置{msg_text}")

    def _on_open_third_party_url(self, url: str):
        if not url:
            if self._module_view:
                QMessageBox.warning(self._module_view, "提示", "该权限没有设置管理链接")
            return

        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        success = QDesktopServices.openUrl(QUrl(url))
        if not success and self._module_view:
            QMessageBox.warning(self._module_view, "错误", f"无法打开链接: {url}")
