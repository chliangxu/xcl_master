import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel,QHeaderView
from PyQt5 import uic
from src.common.utils import ResourceUtils


class VersionInfoModuleView(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(ResourceUtils.get_ui_path(__file__, "recommend_version.ui"), self)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)




if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建QApplication实例
    window = VersionInfoModuleView()  # 实例化主窗口
    window.show()  # 显示窗口
    sys.exit(app.exec_())  # 进入事件循环