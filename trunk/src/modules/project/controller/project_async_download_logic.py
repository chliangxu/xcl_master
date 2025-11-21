import os
import subprocess

from PyQt5.QtCore import QTimer, pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox

from src.core import LogSystem, EventSystem
from src.modules.project.controller.project_download_thread import ProjectDownloadThread
from src.modules.project.controller.project_events import ProjectEvents
from src.modules.project.controller.project_macros import ProjectMacros


class ProjectAsyncDownloadLogic(QObject):


    def __init__(self, controller):
        super().__init__()
        self.install_downloaded_name = None
        self.install_tools_id = None
        self.download_thread = None
        self.controller = controller
        self.save_dir = "C:\\DevTools\\"

    def start_download(self, tools_id, download_url, save_dir, installer_name):
        EventSystem.instance().send_event(ProjectEvents.DOWNLOAD_TOOLS_START, tools_id)
        self.download_thread = ProjectDownloadThread(self, tools_id, download_url, save_dir, installer_name)
        self.download_thread.start()

    def download_and_install_by_tools_id(self, tools_id):
        if tools_id == ProjectMacros.INSTALL_INDEX_SVN:
            self.download_and_install_svn(tools_id)
        elif tools_id == ProjectMacros.INSTALL_INDEX_VS:
            self.download_and_install_vs(tools_id)
        elif tools_id == ProjectMacros.INSTALL_INDEX_VS_CODE:
            self.download_and_install_vs_code(tools_id)
        elif tools_id == ProjectMacros.INSTALL_INDEX_P4:
            self.download_and_install_p4(tools_id)

    def download_and_install_p4(self, tools_id):
        download_url = "https://filehost.perforce.com/perforce/r25.3/bin.ntx64/p4vinst64.exe"
        installer_name = "p4vinst64.exe"
        self.download_and_install(tools_id, download_url, installer_name)

    def download_and_install_svn(self, tools_id):
        download_url = "https://git.tencent.com/SVN/TortoiseSVN/Preview/TortoiseSVN-Preview-x64.msi"
        installer_name = "TortoiseSVN-Preview-x64.msi"
        self.download_and_install(tools_id, download_url, installer_name)

    def download_and_install_vs_code(self, tools_id):
        download_url = "https://vscode.download.prss.microsoft.com/dbazure/download/stable/cb1933bbc38d329b3595673a600fab5c7368f0a7/VSCodeUserSetup-x64-1.106.1.exe"
        installer_name = "VSCodeUserSetup-x64-1.106.1.exe"
        self.download_and_install(tools_id, download_url, installer_name)

    def download_and_install_vs(self, tools_id):
        download_url = "https://aka.ms/vs/17/release/vs_professional.exe"
        installer_name = "vs_professional.exe"
        self.download_and_install(tools_id, download_url, installer_name)

    def download_and_install(self, tools_id, download_url, installer_name):
        installer_path = os.path.join(self.save_dir, installer_name)
        downloaded_name = "downloaded_" + installer_name
        downloaded_path = os.path.join(self.save_dir, downloaded_name)

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        if not os.path.exists(downloaded_path):
            LogSystem.instance().info("[project] 文件%s不存在，将直接尝试下载，链接是%s" % (installer_path, download_url))
            self.start_download(tools_id, download_url, self.save_dir, installer_name)
        else:
            LogSystem.instance().info("[project] 文件%s已存在，将直接尝试安装" % installer_path)
            self.show_install_confirm(tools_id, installer_name)

    def show_install_confirm(self, tools_id, installer_name):
        downloaded_name = "downloaded_" + installer_name
        if not os.path.exists(self.save_dir + downloaded_name):
            print(f"❌ 安装文件不存在: {self.save_dir + downloaded_name}")
            return

        message_box_reply = QMessageBox.question(None, '安装确认', "%s已下载完成，现在安装吗？" % installer_name,
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message_box_reply == QMessageBox.Yes:
            self.install(tools_id, self.save_dir + downloaded_name)
        else:
            LogSystem.instance().info("[project] 安装已取消")  # 用户选择取消

    def install(self, tools_id, installer_path):
        """根据文件类型调用相应的安装函数"""
        file_extension = os.path.splitext(installer_path)[1].lower()
        EventSystem.instance().send_event(ProjectEvents.INSTALL_TOOLS_START, tools_id)
        if file_extension == '.msi':
            return self.install_msi(tools_id, installer_path)
        elif file_extension == '.exe':
            return self.install_exe(tools_id, installer_path)
        else:
            print(f"❌ 不支持的安装文件格式: {file_extension}")
            return False

    @staticmethod
    def install_msi(tools_id, installer_path):
        """安装MSI文件[1,9](@ref)"""
        try:
            LogSystem.instance().info("\n开始安装 MSI 包...")
            LogSystem.instance().info("正在进行静默安装，请稍候...")
            command = ['msiexec', '/i', installer_path]

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            LogSystem.instance().info("安装进行中...")
            # 等待安装完成
            stdout, stderr = process.communicate(timeout=1800)  # 30分钟超时

            if process.returncode == 0:
                EventSystem.instance().send_event(ProjectEvents.INSTALL_TOOLS_FINISH, tools_id)
                LogSystem.instance().info("\n✅ MSI 安装成功!")
                return True
            else:
                LogSystem.instance().info(f"\n❌ MSI 安装失败，返回码: {process.returncode}")
                if stderr:
                    LogSystem.instance().info(f"错误信息: {stderr}")
                EventSystem.instance().send_event(ProjectEvents.INSTALL_TOOLS_FINISH, tools_id)
                return False

        except subprocess.TimeoutExpired:
            print("\n⚠️ 安装超时，但可能仍在后台进行中...")
            return True
        except Exception as e:
            print(f"\n❌ 安装过程中发生错误: {e}")
            return False

    # 安装程序函数
    @staticmethod
    def install_exe(tools_id, installer_path):
        try:
            LogSystem.instance().info("\n开始安装 Visual Studio...")
            LogSystem.instance().info("这可能需要较长时间，请耐心等待...")
            command = [
                installer_path
            ]

            # 启动安装程序
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # 实时显示安装进度
            print("安装进度:")
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())

            # 等待安装完成
            process.wait()

            if process.returncode == 0:
                LogSystem.instance().info("\nVisual Studio 安装成功!")
                EventSystem.instance().send_event(ProjectEvents.INSTALL_TOOLS_FINISH, tools_id)
                return True
            else:
                EventSystem.instance().send_event(ProjectEvents.INSTALL_TOOLS_FINISH, tools_id)
                LogSystem.instance().info(f"\n安装失败，错误代码: {process.returncode}")
                return False
        except Exception as e:
            LogSystem.instance().info(f"安装过程中发生错误: {e}")
            return False

    def download_finish(self, tools_id, installer_name):
        if os.path.exists(self.save_dir + installer_name):
            downloaded_install_name = "downloaded_" + installer_name
            os.rename(self.save_dir + installer_name, self.save_dir + downloaded_install_name)
            self.show_install_confirm(tools_id, installer_name)
        else:
            LogSystem.instance().info(f"[project] 更新结束后，文件不存在 installer_name[%s]" % installer_name)

    def on_tools_download_complete(self, tools_id, installer_name ):
        LogSystem.instance().info("[Project] 下载完成 installer_name[%s] " % installer_name)
        self.download_finish(tools_id, installer_name)

    def on_install_dev_tools(self, tool_id: int):
        LogSystem.instance().info("[Project] 开始安装 tools_id: " + str(tool_id))
        self.download_and_install_by_tools_id(tool_id)

    @staticmethod
    def on_download_tools_error(error_msg):
        LogSystem.instance().info("[Project] 下载失败 error_msg: " + str(error_msg))