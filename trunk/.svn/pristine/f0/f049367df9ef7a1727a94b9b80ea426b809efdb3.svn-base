from PyQt5.QtWidgets import QVBoxLayout

from src.common import BaseWidget
from src.modules.project.view.project_config_p4_item import ProjectConfigP4Item
from src.modules.project.view.project_config_svn_item import ProjectConfigSvnItem


class ProjectConfigWidget(BaseWidget):

    def __init__(self, parent=None):
        self.project_config_svn_item = None
        self.project_config_p4_item = None
        super().__init__(parent)

    def init_ui(self):
        self.project_config_p4_item = ProjectConfigP4Item(self)
        self.project_config_svn_item = ProjectConfigSvnItem(self)

        form_layout = QVBoxLayout(self)
        form_layout.addWidget(self.project_config_p4_item)
        form_layout.addWidget(self.project_config_svn_item)