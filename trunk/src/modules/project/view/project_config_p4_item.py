from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QFrame, QMessageBox
from src.common.base import BaseWidget
from src.common.utils import ResourceUtils
from src.core import LogSystem


class ProjectConfigP4Item(BaseWidget):

    def __init__(self, project_config_widget):
        self.confirm_btn = None
        self.connect_btn = None
        self.browser_btn = None
        self.create_dir_btn = None
        self.workspace_input = None
        self.account_input = None
        self.server_combo_box = None
        self.dir_input = None
        self.project_config_widget = project_config_widget
        super().__init__(None)


    def setup_connections(self):
        pass

    def init_ui(self):
        uic.loadUi(ResourceUtils.get_ui_path(__file__, "project_config_p4.ui"), self)
        self.dir_input = self.findChild(QLineEdit, "p4catalogueEdit")
        self.server_combo_box = self.findChild(QComboBox, "p4serverBox")
        self.account_input = self.findChild(QLineEdit, "accountEdit")
        self.workspace_input = self.findChild(QLineEdit, "workspaceEdit")

        self.create_dir_btn = self.findChild(QPushButton, "p4newButton")
        self.browser_btn = self.findChild(QPushButton, "p4browserButton")
        self.connect_btn = self.findChild(QPushButton, "p4connectButton")
        self.confirm_btn = self.findChild(QPushButton, "p4confirmButton")

        self.dir_input.setText("E:\\CJGame\\trunk")
        self.account_input.setText("jackningli")
        self.workspace_input.setText("JackDiskE")
        self.server_combo_box.addItem("devproxy.ied.com:9666")  # 添加第一个选项
        self.server_combo_box.addItem("cgproxy.ied.com:9666")  # 添加第二个选项[2](@ref)
