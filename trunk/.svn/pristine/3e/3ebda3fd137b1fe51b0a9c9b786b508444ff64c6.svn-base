from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from src.common.base.base_widget import BaseWidget


class BaseCardWidget(BaseWidget):
    clicked = pyqtSignal()
    hover_changed = pyqtSignal(bool)

    def __init__(self, parent=None):
        self._is_hovered = False
        self._is_clickable = True
        super().__init__(parent)

    def setup_ui(self):
        self.setFixedHeight(120)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(8)

    def apply_styles(self):
        self.setStyleSheet(f"""
            BaseCardWidget {{
                background-color: {self.get_color('surface')};
                border: 1px solid {self.get_color('border')};
                border-radius: 8px;
            }}
            BaseCardWidget:hover {{
                background-color: {self.get_color('surface_hover')};
                border-color: {self.get_color('primary')};
            }}
        """)

    def set_clickable(self, clickable: bool) -> None:
        self._is_clickable = clickable
        if clickable:
            self.setCursor(QCursor(Qt.PointingHandCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))

    def mousePressEvent(self, event):
        if self._is_clickable and event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self._is_hovered = True
        self.hover_changed.emit(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._is_hovered = False
        self.hover_changed.emit(False)
        super().leaveEvent(event)

    def is_hovered(self) -> bool:
        return self._is_hovered

    def create_title_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet(f"""
            QLabel {{
                color: {self.get_color('text')};
                font-size: 14px;
                font-weight: bold;
            }}
        """)
        return label

    def create_description_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet(f"""
            QLabel {{
                color: {self.get_color('text_secondary')};
                font-size: 12px;
            }}
        """)
        return label

    def create_badge_label(self, text: str, color: str = None) -> QLabel:
        if color is None:
            color = self.get_color('primary')

        label = QLabel(text)
        label.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                padding: 2px 8px;
                border-radius: 10px;
                font-size: 11px;
            }}
        """)
        return label
