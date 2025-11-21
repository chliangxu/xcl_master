import urllib.request
from PyQt5.QtCore import QThread, pyqtSignal
from src.core import EventSystem, LogSystem
from src.modules.project.controller.project_events import ProjectEvents

class ProjectDownloadThread(QThread):
    def __init__(self, logic, tools_id, url, save_dir, installer_name):
        super().__init__()
        self.url = url
        self.save_dir = save_dir
        self.installer_name = installer_name
        self.save_path = save_dir + installer_name
        self._is_running = True
        self.tools_id = tools_id
        self.logic = logic

    def run(self):
        """执行下载任务"""
        try:
            # 获取文件大小
            with urllib.request.urlopen(self.url) as response:
                total_size = int(response.info().get('Content-Length', 0))
                total_mb = total_size / (1024 * 1024)

            # 开始下载
            downloaded = 0
            block_size = 1024 * 8  # 8KB

            def progress_callback(count, block_size, total_size):
                nonlocal downloaded
                downloaded = count * block_size
                percent = int(downloaded * 100 / total_size)
                downloaded_mb = downloaded / (1024 * 1024)
                self.logic.controller.get_module_view().project_install_widget.tools_download_progress.emit(self.tools_id, count, block_size, total_size)
                # progress_dict = {"count": count, "block_size": block_size, "total_size": total_size}
                # EventSystem.instance().send_event(ProjectEvents.DOWNLOAD_TOOLS_PROGRESS, progress_dict)
                LogSystem.instance().info(f"\r下载进度: {percent}% [{count * block_size / (1024 * 1024):.2f}MB/{total_size / (1024 * 1024):.2f}MB]")
                return self._is_running  # 如果返回False，下载会中断

            urllib.request.urlretrieve(
                self.url,
                self.save_path,
                reporthook=progress_callback
            )
            self.logic.controller.get_module_view().tools_download_complete.emit(self.tools_id, self.installer_name)
        except Exception as e:
            EventSystem.instance().send_event(ProjectEvents.DOWNLOAD_TOOLS_ERROR, str(e))


    def stop(self):
        """停止下载"""
        self._is_running = False