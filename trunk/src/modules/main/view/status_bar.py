from PyQt5.QtWidgets import QStatusBar, QLabel
from PyQt5.QtCore import QTimer


class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()

        self.message_label = QLabel()
        self.addWidget(self.message_label, 1)

        self.setStyleSheet("""
            QStatusBar {
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
                padding: 2px 8px;
            }
            QLabel {
                color: #495057;
                padding: 0 5px;
            }
        """)

    def show_message(self, message: str, timeout: int = 0):
        self.message_label.setText(message)
        if timeout > 0:
            QTimer.singleShot(timeout, lambda: self.message_label.setText(""))

    def clear(self):
        self.message_label.setText("")
