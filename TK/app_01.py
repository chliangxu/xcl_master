from tkinter import *
import tkinter as tk
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

    def set_init_window(self):
        self.init_window_name.title("GNGame")
        self.init_window_name.geometry('1200x530+200+200')

        self.FM1 = Frame(self.init_window_name, borderwidth=10)
        """
        Frame的用法及介绍
        0.Frame组件是容器组件，用于复杂布局中将其他的组件分组，所谓的容器组件，就是可以收纳其他组件，可以做其他组件的父组件的组件
        1.属性
        bg或background：Frame组件的背景颜色
        bd或borderwidth：Frame组件的边框宽度，默认值为0
        width：Frame组件的宽度 | height：Frame组件的高度 | padx：Frame的X方向的内边距 | pady：Frame的Y方向的内边距 | relieff：Frame的样式
        """
        self.FM1.grid(row=0, column=0, rowspan=5, columnspan=5, sticky=NW)
        """
        Grid布局的常用属性
        row：组件所在的行号 | column：组件所在列号 | rowspan：组件所使用的行数 | columnspan：组件所使用的列数
        padx：组件与单元格边缘的水平距离 | pady：组件与单元格边缘的垂直距离 | ipadx：组件内部的水平填充 | ipady：组件内部的垂直填充
        sticky：指定了元素在单元格中的对齐方式，可以取值为N（上），S（下），W（左），E（右），NW（左上），NE（右上），SW（左下），SE（右下）
        以及他们的组合
        """
        self.target_label = Label(self.FM1, text="平台:")
        self.target_label.grid(row=0, column=0, sticky=NW)

        # self.TP1 = RADIOBUTTON(self.FM1, Text=)



def gui_start():
    # cook
    # import os
    # CookerExe = os.path.abspath("./../../../../trunk/Engine/Binaries/Win64/UE4Editor-Cmd.exe")
    # print(CookerExe)

    init_window = tk.Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()

    # 设置根窗口默认属性
    # ZMJ_PORTAL.set_init_window()
    # command_param.set_str(sys.argv)
    # patch_config_path = command_param.parse_arg(0) or ""
    # if not os.path.exists(patch_config_path):
    #     init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()
