from tkinter import Tk, StringVar, Label
import time




class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        self.TargetPlatform = StringVar(self.init_window_name, "Android_ASTC")
        self.VersionType = StringVar(self.init_window_name, "不含lua版本号")
        self.VersionNum = StringVar(self.init_window_name, "0.0.0.0")
        self.CleanType = StringVar(self.init_window_name, "删除以前cook")
        self.PatchIndex = StringVar(self.init_window_name, "001")
        self.LastStat = 'Start'
        self.PreloadInfo = StringVar(self.init_window_name, "need preload")
        self.pak_type = StringVar(self.init_window_name, "latest")
        self.shader_type = StringVar(self.init_window_name, "false")
        self.need_reference = StringVar(self.init_window_name, "false")


























def gui_start():
    # cook
    # import os
    # CookerExe = os.path.abspath("./../../../../trunk/Engine/Binaries/Win64/UE4Editor-Cmd.exe")
    # print(CookerExe)

    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    # ZMJ_PORTAL.set_init_window()
    # command_param.set_str(sys.argv)
    # patch_config_path = command_param.parse_arg(0) or ""
    # if not os.path.exists(patch_config_path):
    #     init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()