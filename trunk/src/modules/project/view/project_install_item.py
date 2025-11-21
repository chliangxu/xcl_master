import sys
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QMessageBox, QToolButton

from src.common import BaseWidget
from src.common.utils import ResourceUtils
from src.core import EventSystem, LogSystem
from src.modules.project.controller.project_events import ProjectEvents
from src.modules.project.controller.project_macros import ProjectMacros


class ProjectInstallItemWidget(BaseWidget):
    def __init__(self, tools_id, tools_name):
        self.icon_button = None
        self.tools_state = 0
        self.version_suggest_label = None
        self.version_label = None
        self.install_btn = None
        self.name_label = None
        self.tools_id = tools_id
        self.tools_name = tools_name
        self.tools_icon_dict = {1: "svn.png", 2: "p4.png", 3: "vs.png", 4: "vs_code.png"}
        self.tools_suggest_version_dict = {1: "1.15.3", 2: "2024.2", 3: "17.14.36628.8", 4: "1.106.1"}
        super().__init__(None)

    def init_ui(self):
        uic.loadUi(ResourceUtils.get_ui_path(__file__, "project_install_item.ui"), self)

        self.name_label = self.findChild(QLabel, "softwareoneLabel")
        self.name_label.setText(self.tools_name)

        self.install_btn = self.findChild(QPushButton, "installoneButton")
        self.install_btn.setText("安装")

        self.version_label = self.findChild(QLabel, "versiononeLabel")
        self.version_label.setText("")

        self.version_suggest_label = self.findChild(QLabel, "versionsuggestLabel")
        self.version_suggest_label.setText("")

        self.install_btn.clicked.connect(self._on_tools_clicked)

        self.icon_button = self.findChild(QToolButton, "icononeButton")
        self.set_tools_icon()

        self.set_tools_suggest_version()

    def set_tools_suggest_version(self):
        if self.tools_id in self.tools_suggest_version_dict:
            self.version_suggest_label.setText(f"建议安装版本：{self.tools_suggest_version_dict[self.tools_id]}")

    def _on_tools_clicked(self):
        if self.tools_state == ProjectMacros.TOOLS_STATE_ALREADY_INSTALL:
            message_box_reply = QMessageBox.question(None, '安装确认', "%s 本地已安装，确认要重新安装吗？" % self.tools_name,
                                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if message_box_reply == QMessageBox.Yes:
                EventSystem.instance().send_event(ProjectEvents.TOOLS_INSTALL_CLICK, self.tools_id)
            else:
                LogSystem.instance().info("[project] TOOLS_STATE_ALREADY_INSTALL %s安装已取消" % self.tools_name)
        elif self.tools_state == ProjectMacros.TOOLS_STATE_DOWNLOADING:
            QMessageBox.warning(None, '提示', "%s 正在下载中，请稍等" % self.tools_name)
        elif self.tools_state == ProjectMacros.TOOLS_STATE_NEED_INSTALL or self.tools_state == ProjectMacros.TOOLS_STATE_DOWNLOADED:
            EventSystem.instance().send_event(ProjectEvents.TOOLS_INSTALL_CLICK, self.tools_id)
        elif self.tools_state == ProjectMacros.TOOLS_STATE_INSTALLING:
            message_box_reply = QMessageBox.question(None, '安装确认',
                                                     "%s 上次安装未结束，确认要重新安装吗？" % self.tools_name,
                                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if message_box_reply == QMessageBox.Yes:
                EventSystem.instance().send_event(ProjectEvents.TOOLS_INSTALL_CLICK, self.tools_id)
            else:
                LogSystem.instance().info("[project] TOOLS_STATE_INSTALLING %s安装已取消" % self.tools_name)
        else:
            EventSystem.instance().send_event(ProjectEvents.TOOLS_INSTALL_CLICK, self.tools_id)


    def set_label_text(self, installed_version):
        self.version_label.setText(installed_version)

    def set_tools_state(self, tools_state):
        self.tools_state = tools_state

    def set_btn_text(self, text):
        self.install_btn.setText(text)

    def get_tools_icon_path(self):
        icon_name = "default.png"
        if self.tools_id in self.tools_icon_dict:
            icon_name = self.tools_icon_dict[self.tools_id]
        icon_path = self._get_icon_dir() / icon_name
        return icon_path

    def set_tools_icon(self):
        icon_path = self.get_tools_icon_path()
        if icon_path.exists():
            self.icon_button.setIcon(QIcon(str(icon_path)))
            self.icon_button.setIconSize(QSize(150, 150))
        else:
            LogSystem.instance().info(f"[project] set_tools_icon failed path[{str(icon_path)}] not found")

    @staticmethod
    def _get_icon_dir() -> Path:
        if getattr(sys, 'frozen', False):
            base_path = Path(sys.executable).parent
        else:
            base_path = Path(__file__).parent.parent.parent.parent.parent
        return base_path / 'assets' / 'icon' / 'project'