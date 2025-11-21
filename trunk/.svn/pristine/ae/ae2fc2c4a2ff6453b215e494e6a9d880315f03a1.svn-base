from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


class UserRole(Enum):
    PLANNER = "策划"
    CLIENT_PROGRAMMER = "客户端程序"
    SERVER_PROGRAMMER = "服务器程序"
    ARTIST = "美术"
    OPERATIONS = "运营"


@dataclass
class User:
    id: str
    name: str
    role: UserRole
    avatar_path: str = ""
    preferences: Dict[str, Any] = None

    def __post_init__(self):
        if self.preferences is None:
            self.preferences = {}


class UserModel:
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
        self._current_user = None
        self._users = {}

    @classmethod
    def get_instance(cls) -> "UserModel":
        return cls()

    def set_current_user(self, user: User):
        self._current_user = user

    def get_current_user(self) -> Optional[User]:
        return self._current_user

    def add_user(self, user: User):
        self._users[user.id] = user

    def get_user(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def get_all_users(self) -> List[User]:
        return list(self._users.values())

    def update_user(self, user: User):
        if user.id in self._users:
            self._users[user.id] = user
        if self._current_user and self._current_user.id == user.id:
            self._current_user = user
