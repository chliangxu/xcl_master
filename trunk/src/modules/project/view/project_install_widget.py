from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGridLayout

from src.common import BaseWidget
from src.common.utils import StatusUtils
from src.core import EventSystem
from src.modules.project.controller.project_events import ProjectEvents
from src.modules.project.controller.project_macros import ProjectMacros
from src.modules.project.view.project_install_item import ProjectInstallItemWidget


class ProjectInstallWidget(BaseWidget):
    install_dev_tools = pyqtSignal(int)
    tools_download_progress = pyqtSignal(int, int, int, int)
    tools_install_start = pyqtSignal(int)
    tools_install_end = pyqtSignal(int)

    def __init__(self, project_module_view):
        self.vs_code_item = None
        self.vs_item = None
        self.p4_item = None
        self.svn_item = None
        self.btn_state_dict = {}
        self.btn_name_dict = {1:"SVN", 2:"P4", 3:"Visual Studio", 4:"Visual Studio Code"}
        self.tools_info_dict = {}
        self.project_module_view = project_module_view
        super().__init__(None)
        self.setup_connections()

    def get_tools_name(self, tools_id):
        if tools_id in self.btn_name_dict:
            return self.btn_name_dict[tools_id]
        else:
            return ""

    def get_tools_state(self, tools_id):
        if tools_id in self.btn_state_dict:
            return self.btn_state_dict[tools_id]
        else:
            return 0

    def get_tools_item(self, tools_id):
        if tools_id == ProjectMacros.INSTALL_INDEX_VS:
            return self.vs_item
        if tools_id == ProjectMacros.INSTALL_INDEX_VS_CODE:
            return self.vs_code_item
        if tools_id == ProjectMacros.INSTALL_INDEX_P4:
            return self.p4_item
        if tools_id == ProjectMacros.INSTALL_INDEX_SVN:
            return self.svn_item
        return None

    def setup_connections(self):
        self.install_dev_tools.connect(
            lambda tools_id: EventSystem.instance().send_event(ProjectEvents.TOOLS_INSTALL_CLICK, tools_id))
        EventSystem.instance().register_event(ProjectEvents.CHECK_TOOLS_VERSION_END, self._on_check_tools_version_end)
        EventSystem.instance().register_event(ProjectEvents.DOWNLOAD_TOOLS_START, self._on_download_tools_start)
        # EventSystem.instance().register_event(ProjectEvents.INSTALL_TOOLS_START, self._on_install_tools_start)
        EventSystem.instance().register_event(ProjectEvents.INSTALL_TOOLS_FINISH, self._on_install_tools_finish)
        self.project_module_view.tools_download_complete.connect(self._on_tools_download_complete)
        self.tools_download_progress.connect(self._on_tools_download_progress)
        self.tools_install_start.connect(self._on_install_tools_start)

    def init_ui(self):
        # 创建网格布局
        grid = QGridLayout(self)

        # 设置布局参数 - 这是关键优化部分
        grid.setSpacing(20)  # 增加间距，让卡片之间有适当空隙但不要太分散
        grid.setContentsMargins(30, 30, 30, 30)  # 设置边距，让内容不贴边

        # 设置列宽比例，让列均匀分布
        grid.setColumnStretch(0, 1)  # 第0列可拉伸
        grid.setColumnStretch(1, 1)  # 第1列可拉伸
        grid.setColumnStretch(2, 1)  # 第2列可拉伸

        # 设置行高比例
        grid.setRowStretch(0, 1)  # 第0行可拉伸
        grid.setRowStretch(1, 1)  # 第1行可拉伸

        self.svn_item = ProjectInstallItemWidget(ProjectMacros.INSTALL_INDEX_SVN, self.get_tools_name(ProjectMacros.INSTALL_INDEX_SVN))
        self.p4_item = ProjectInstallItemWidget(ProjectMacros.INSTALL_INDEX_P4, self.get_tools_name(ProjectMacros.INSTALL_INDEX_P4))
        self.vs_item = ProjectInstallItemWidget(ProjectMacros.INSTALL_INDEX_VS, self.get_tools_name(ProjectMacros.INSTALL_INDEX_VS))
        self.vs_code_item = ProjectInstallItemWidget(ProjectMacros.INSTALL_INDEX_VS_CODE, self.get_tools_name(ProjectMacros.INSTALL_INDEX_VS_CODE))

        # 将卡片添加到网格布局中 - 2行3列的布局
        # 第一行：SVN, P4, Visual Studio
        grid.addWidget(self.svn_item, 0, 0)  # 第0行，第0列
        grid.addWidget(self.p4_item, 0, 1)  # 第0行，第1列
        grid.addWidget(self.vs_item, 0, 2)  # 第0行，第2列

        # 第二行：VS Code 放在中间位置，空出两边
        grid.addWidget(self.vs_code_item, 1, 0)  # 第1行，第1列（中间位置）

    def _on_check_tools_version_end(self, tools_info_dict):

        self.tools_info_dict = tools_info_dict

        vs_found = tools_info_dict["vs_found"]
        vs_version = tools_info_dict["vs_version"]
        self.update_tools_btn_label(ProjectMacros.INSTALL_INDEX_VS, vs_found, vs_version)

        vs_code_found = tools_info_dict["vs_code_found"]
        vs_code_version = tools_info_dict["vs_code_version"]
        self.update_tools_btn_label(ProjectMacros.INSTALL_INDEX_VS_CODE, vs_code_found, vs_code_version)

        p4_found = tools_info_dict["p4_found"]
        p4_version = tools_info_dict["p4_version"]
        self.update_tools_btn_label(ProjectMacros.INSTALL_INDEX_P4, p4_found, p4_version)

        svn_found = tools_info_dict["svn_found"]
        svn_version = tools_info_dict["svn_version"]
        self.update_tools_btn_label(ProjectMacros.INSTALL_INDEX_SVN, svn_found, svn_version)

    def update_tools_btn_label(self, tools_id, found, version):
        item = self.get_tools_item(tools_id)

        tools_name = self.get_tools_name(tools_id)
        if found:
            item.set_label_text(f"已安装版本：{version}")
            item.set_tools_state(ProjectMacros.TOOLS_STATE_ALREADY_INSTALL)
            self.btn_state_dict[tools_id] = ProjectMacros.TOOLS_STATE_ALREADY_INSTALL
            item.set_btn_text("已安装")
        else:
            item.set_label_text("", "")
            self.btn_state_dict[tools_id] = ProjectMacros.TOOLS_STATE_NEED_INSTALL
            item.set_btn_text("安装")

    def _on_download_tools_start(self, tools_id):
        item = self.get_tools_item(tools_id)
        if item is not None:
            item.set_tools_state(ProjectMacros.TOOLS_STATE_DOWNLOADING)
            self.btn_state_dict[tools_id] = ProjectMacros.TOOLS_STATE_DOWNLOADING
            item.set_btn_text("下载中……")

    def _on_install_tools_start(self, tools_id):
        item = self.get_tools_item(tools_id)
        if item is not None:
            item.set_btn_text("安装中……")
            item.set_tools_state(ProjectMacros.TOOLS_STATE_INSTALLING)
            self.btn_state_dict[tools_id] = ProjectMacros.TOOLS_STATE_INSTALLING

    def _on_install_tools_finish(self, tools_id):
        item = self.get_tools_item(tools_id)
        if item is not None:
            item.set_tools_state(ProjectMacros.TOOLS_STATE_ALREADY_INSTALL)
            self.btn_state_dict[tools_id] = ProjectMacros.TOOLS_STATE_ALREADY_INSTALL
            item.set_btn_text("已安装")

    def _on_tools_download_complete(self, tools_id, installer_name):
        item = self.get_tools_item(tools_id)
        if item is not None:
            item.set_tools_state(ProjectMacros.TOOLS_STATE_DOWNLOADED)
            self.btn_state_dict[tools_id] = ProjectMacros.TOOLS_STATE_DOWNLOADED
            item.set_btn_text("下载完成")

    def _on_tools_download_progress(self, tools_id, count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        tools_name = self.get_tools_name(tools_id)
        StatusUtils.show(f"{tools_name} 下载进度: {percent}% [{count * block_size / (1024 * 1024):.2f}MB/{total_size / (1024 * 1024):.2f}MB]")