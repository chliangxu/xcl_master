from typing import Dict, List, Callable, Any


class EventSystem:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.initialize()

    @classmethod
    def instance(cls):
        return cls()

    def initialize(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def register_event(self, event_name: str, callback: Callable):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        if callback not in self._listeners[event_name]:
            self._listeners[event_name].append(callback)

    def unregister_event(self, event_name: str, callback: Callable):
        if event_name in self._listeners:
            if callback in self._listeners[event_name]:
                self._listeners[event_name].remove(callback)
            if not self._listeners[event_name]:
                del self._listeners[event_name]

    def send_event(self, event_name: str, data: Any = None):
        if event_name in self._listeners:
            for callback in self._listeners[event_name][:]:
                try:
                    callback(data) if data is not None else callback()
                except Exception as e:
                    from src.core.log import LogSystem
                    LogSystem.instance().error(f"Event callback error [{event_name}]: {e}")

    def clear_event(self, event_name: str = None):
        if event_name:
            if event_name in self._listeners:
                del self._listeners[event_name]
        else:
            self._listeners.clear()

    def has_listeners(self, event_name: str) -> bool:
        return event_name in self._listeners and len(self._listeners[event_name]) > 0

    def get_listener_count(self, event_name: str) -> int:
        return len(self._listeners.get(event_name, []))
