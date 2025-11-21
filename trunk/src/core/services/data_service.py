from typing import Optional, Dict, Any


class DataService:
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
        self._repositories: Dict[str, Any] = {}
        self._global_data: Dict[str, Any] = {}

    @classmethod
    def get_instance(cls) -> "DataService":
        return cls()

    def register_repository(self, name: str, repository: Any):
        self._repositories[name] = repository

    def get_repository(self, name: str) -> Optional[Any]:
        return self._repositories.get(name)

    def unregister_repository(self, name: str):
        if name in self._repositories:
            del self._repositories[name]

    def set_global_data(self, key: str, value: Any):
        self._global_data[key] = value

    def get_global_data(self, key: str, default=None) -> Any:
        return self._global_data.get(key, default)

    def clear_global_data(self):
        self._global_data.clear()

    def get_all_repositories(self) -> Dict[str, Any]:
        return self._repositories.copy()

    @property
    def tool_repository(self):
        return self.get_repository('tool')

    @property
    def user_repository(self):
        return self.get_repository('user')

    @property
    def project_repository(self):
        return self.get_repository('project')

    @property
    def permission_repository(self):
        return self.get_repository('permission')
