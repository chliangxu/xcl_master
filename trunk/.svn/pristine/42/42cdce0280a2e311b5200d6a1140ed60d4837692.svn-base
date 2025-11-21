from PyQt5 import uic
from PyQt5.QtWidgets import QLineEdit, QComboBox, QPushButton

from src.common import BaseWidget
from src.common.utils import ResourceUtils


class ProjectConfigSvnItem(BaseWidget):

    def __init__(self, project_config_widget):
        self.confirm_btn = None
        self.server_combo_box = None
        self.dir_input = None
        self.project_config_widget = project_config_widget
        super().__init__(None)


    def setup_connections(self):
        pass

    def init_ui(self):
        uic.loadUi(ResourceUtils.get_ui_path(__file__, "project_config_svn.ui"), self)
        self.dir_input = self.findChild(QLineEdit, "svncatalogueEdit")
        self.server_combo_box = self.findChild(QComboBox, "svnserverBox")
        self.server_combo_box.addItem("http://tc-svn.tencent.com/PanGu/TomorrowClient_proj/branches/CJGame/trunk/Survive")  # 添加第一个选项
        self.server_combo_box.addItem("http://tc-svn.tencent.com/PanGu/TomorrowClient_proj/branches/CJGame/trunk/UE4181/Source")  # 添加第二个选项[2](@ref)
        self.confirm_btn = self.findChild(QPushButton, "svnconfirmButton")

        self.dir_input.setText("E:\\CJGame\\trunk")

#http://tc-svn.tencent.com/PanGu/TomorrowClient_proj/branches/CJGame/trunk