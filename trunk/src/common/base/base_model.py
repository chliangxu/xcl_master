from PyQt5.QtCore import QObject, pyqtSignal

class BaseModel(QObject):
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._data = {}

    def get_data(self, key: str, default=None):
        return self._data.get(key, default)

    def set_data(self, key: str, value):
        self._data[key] = value
        self.data_changed.emit()

    def clear_data(self):
        self._data.clear()
        self.data_changed.emit()

    def get_all_data(self):
        return self._data.copy()
