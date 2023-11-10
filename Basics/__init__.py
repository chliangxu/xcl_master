# -*- coding: utf-8 -*-

import hashlib
import os
import time
import CookAndPakSingleBluePrint as tools
import threading
import sys
import json
import command_param


def get_lib_version(lib_name):
    import re
    version = "-1"
    list_log = os.popen("pip3 list").read().splitlines()
    for line in list_log:
        python_lib_info = re.split(r"[ ]+", line)
        if len(python_lib_info) == 2:
            lib_version = python_lib_info[1]
            name = python_lib_info[0]
            if name == lib_name:
                version = lib_version
                break
    return version


if sys.version > '3':
    from tkinter import *
    from tkinter import filedialog
    import platform

    if platform.system() == 'Windows':
        if not get_lib_version("xlrd") == "1.2.0":
            # os.system(f'libs\\windows\\Python38\\python.exe -m pip uninstall xlrd -y')
            # os.system(f'libs\\windows\\Python38\\python.exe -m pip install xlrd==1.2.0')
            os.system(f'pip uninstall xlrd -y')
            os.system(f'pip install xlrd==1.2.0')
else:
    from Tkinter import *
    import tkFileDialog as filedialog

    reload(sys)
    sys.setdefaultencoding('utf8')

LOG_LINE_NUM = 0
List_State = ['Start']


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

    # 设置窗口
    def set_init_window(self):
        title_path = os.path.abspath(os.path.join(__file__, "..", "..", "..", "..", "..", ".."))
        title_name = os.path.split(title_path)[1]
        self.init_window_name.title("GNPatchTool 分支:" + title_name)  # 窗口名
        self.init_window_name.geometry('1200x530+200+200')
        # self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        # self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高

        # window.fram1
        self.FM1 = Frame(self.init_window_name, borderwidth=10)
        self.FM1.grid(row=0, column=0, rowspan=5, columnspan=5, sticky=NW)
        self.target_label = Label(self.FM1, text="平 台:")
        self.target_label.grid(row=0, column=0, sticky=NW)
        self.TP1 = Radiobutton(self.FM1, text='Android_ASTC', variable=self.TargetPlatform, value='Android_ASTC',
                               command=self.print_info).grid(row=0, column=1, sticky=NW)
        self.TP2 = Radiobutton(self.FM1, text='iOS', variable=self.TargetPlatform, value='iOS',
                               command=self.print_info).grid(row=0, column=3, sticky=NW)
        self.TP3 = Radiobutton(self.FM1, text='WindowsNoEditor', variable=self.TargetPlatform, value='WindowsNoEditor',
                               command=self.print_info).grid(row=0, column=5, sticky=NW)
        # self.TP4 = Radiobutton(self.FM1, text = 'WindowsUGCEditor',variable = self.TargetPlatform, value = 'WindowsUGCEditor', command = self.print_info).grid(row = 0, column = 7,sticky = NW)
        self.TP5 = Radiobutton(self.FM1, text='LinuxServer', variable=self.TargetPlatform, value='LinuxServer',
                               command=self.print_info).grid(row=0, column=9, sticky=NW)

        self.version_label = Label(self.FM1, text="版本号:")
        self.version_label.grid(row=1, column=0, sticky=NW)

        # self.VT1 = Radiobutton(self.FM1, text = '不含lua版本号',variable = self.VersionType, value = '不含lua版本号', command = self.print_info_version).grid(row = 1, column = 1,sticky = NW)
        # self.VT2 = Radiobutton(self.FM1, text = '包含lua版本号',variable = self.VersionType, value = '包含lua版本号', command = self.print_info_version).grid(row = 1, column = 3,sticky = NW)

        self.version_Text = Entry(self.FM1, width=15, textvariable=self.VersionNum)
        self.version_Text.grid(row=1, column=1, sticky=NW, padx=5)

        self.clean_cooked_label = Label(self.FM1, text="清 理:")
        self.clean_cooked_label.grid(row=2, column=0, sticky=NW)
        self.CT1 = Radiobutton(self.FM1, text='删除以前cook', variable=self.CleanType, value='删除以前cook',
                               command=self.print_clean_info).grid(row=2, column=1, sticky=NW)
        self.CT2 = Radiobutton(self.FM1, text='备份以前cook', variable=self.CleanType, value='备份以前cook',
                               command=self.print_clean_info).grid(row=2, column=3, sticky=NW)
        self.CT3 = Radiobutton(self.FM1, text='使用上次cook', variable=self.CleanType, value='SkipCook',
                               command=self.print_clean_info).grid(row=2, column=5, sticky=NW)

        self.patch_index_label = Label(self.FM1, text="Pak索引号:")
        self.patch_index_label.grid(row=3, column=0, sticky=NW)
        self.patch_index_Text = Entry(self.FM1, width=15, textvariable=self.PatchIndex)
        self.patch_index_Text.grid(row=3, column=1, sticky=NW, padx=5)

        self.file_button_1 = Button(self.FM1, text="选择文件", width=10, command=self.select_files)  # 调用内部方法  加()为直接调用
        self.file_button_1.grid(row=4, column=0, rowspan=2, columnspan=2, sticky=NW)

        self.file_button_2 = Button(self.FM1, text="选择文件夹", width=10, command=self.select_dir)  # 调用内部方法  加()为直接调用
        self.file_button_2.grid(row=4, column=1, rowspan=2, columnspan=2, sticky=NW)

        self.file_button_3 = Button(self.FM1, text="导入配置Json", width=10, command=self.import_config)  # 调用内部方法  加()为直接调用
        self.file_button_3.grid(row=6, column=0, rowspan=2, columnspan=2, sticky=NW)

        self.file_button_4 = Button(self.FM1, text="导出配置Json", width=10, command=self.export_config)  # 调用内部方法  加()为直接调用
        self.file_button_4.grid(row=6, column=1, rowspan=2, columnspan=2, sticky=NW)

        self.Preload1 = Radiobutton(self.FM1, text='需要扫描preload', variable=self.PreloadInfo, value='need preload',
                                    command=self.print_info_preload).grid(row=8, column=0, sticky=NW)
        self.Preload2 = Radiobutton(self.FM1, text='不需要扫描preload，快速出包', variable=self.PreloadInfo,
                                    value='not preload，quick_mode', command=self.print_info_preload).grid(row=8,
                                                                                                          column=1,
                                                                                                          sticky=NW)

        self.tips_label = Label(self.FM1, text="说 明:")
        self.tips_label.grid(row=9, column=0, sticky=NW)
        self.tips_message = Message(self.FM1, width=500,
                                    text="1.选择平台\n2.填写版本号\n3.选择是否删除本地Saved/Cooked目录，无特殊需求不需要保留\n4.选择或输入要打包的文件路径\n5.使用Preload扫描需要python版本为3.0-3.8之间",
                                    fg='red').grid(row=10, column=0, columnspan=10, sticky=NW)

        self.target_label = Label(self.FM1, text="UnrealPak版本(日期):")
        self.target_label.grid(row=11, column=0, sticky=NW)
        self.PAK_1 = Radiobutton(self.FM1, text='当前引擎', variable=self.pak_type, value='latest',
                                 command=self.print_unreal_pak).grid(row=11, column=1, sticky=NW)
        self.PAK_2 = Radiobutton(self.FM1, text='4.27(无sig版本信息)', variable=self.pak_type, value='4.27',
                                 command=self.print_unreal_pak).grid(row=11, column=2, sticky=NW)
        self.PAK_3 = Radiobutton(self.FM1, text='3.9(无PakDirectory)', variable=self.pak_type, value='3.9',
                                 command=self.print_unreal_pak).grid(row=11, column=3, sticky=NW)

        self.shader_patch_label = Label(self.FM1, text="ShaderPatch开关")
        self.shader_patch_label.grid(row=12, column=0, sticky=NW)
        self.SP_1 = Radiobutton(self.FM1, text='打开', variable=self.shader_type, value='true',
                                command=self.print_shader_patch).grid(row=12, column=1, sticky=NW)
        self.SP_2 = Radiobutton(self.FM1, text='关闭', variable=self.shader_type, value='false',
                                command=self.print_shader_patch).grid(row=12, column=2, sticky=NW)

        self.reference_label = Label(self.FM1, text="Reference开关")
        self.reference_label.grid(row=13, column=0, sticky=NW)
        self.RP_1 = Radiobutton(self.FM1, text='打开', variable=self.need_reference, value='true',
                                command=self.print_shader_patch).grid(row=13, column=1, sticky=NW)
        self.RP_2 = Radiobutton(self.FM1, text='关闭', variable=self.need_reference, value='false',
                                command=self.print_shader_patch).grid(row=13, column=2, sticky=NW)

        self.start_button = Button(self.FM1, text="开始", width=10, command=self.call_pak)  # 调用内部方法  加()为直接调用
        self.start_button.grid(row=14, column=0, columnspan=2, sticky=NW)

        # window.fram2
        self.FM2 = Frame(self.init_window_name, borderwidth=10)
        self.FM2.grid(row=0, column=11, rowspan=6, columnspan=5, sticky=NW)
        self.result_data_label = Label(self.FM2, text="文件列表")
        self.result_data_label.grid(row=0, column=0, sticky=NW)
        self.result_data_Text = Text(self.FM2, width=70, height=30)  # 文件列表
        self.result_data_Text.grid(row=1, column=0, rowspan=5, columnspan=5, sticky=NW)

        # window.fram3
        self.FM3 = Frame(self.init_window_name, borderwidth=10)
        self.FM3.grid(row=5, column=0, rowspan=10, columnspan=5, sticky=NW)
        self.log_label = Label(self.FM3, text="日志")
        self.log_label.grid(row=0, column=0, sticky=NW)
        self.log_data_Text = Text(self.FM3, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=1, column=0, columnspan=5, sticky=NW)
        self.log_data_Text.config(state="disabled")

        command_param.set_str(sys.argv)
        patch_config_path = command_param.parse_arg(0) or ""
        if os.path.exists(patch_config_path):
            self.import_config_data(patch_config_path)
            self.call_pak()

    # 功能函数
    def select_files(self):
        files = filedialog.askopenfilenames(title='选择要打包的工程内文件',
                                            filetypes=[('Lua Ini Blueprint', '*.lua;*.ini;*.uasset;*.umap'),
                                                       ('All Files', '*')], initialdir='../../../../')
        for x in files:
            self.result_data_Text.insert(1.0, x + '\n')

    # 功能函数
    def select_dir(self):
        dir = filedialog.askdirectory(title='选择要打包的工程内文件夹', mustexist=True, initialdir='../../../../')
        for root, dirs, files in os.walk(dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                self.result_data_Text.insert(1.0, file_path + '\n')

    def import_config(self):
        # self.TargetPlatform = StringVar(self.init_window_name,"Android_ASTC")
        # self.VersionType = StringVar(self.init_window_name,"不含lua版本号")
        # self.VersionNum = StringVar(self.init_window_name,"0.0.0.0")
        # self.CleanType = StringVar(self.init_window_name,"删除以前cook")
        # self.PatchIndex = StringVar(self.init_window_name,"001")
        # self.LastStat = 'Start'
        # self.PreloadInfo = StringVar(self.init_window_name, "need preload")
        patch_config_data = {}
        patch_file = filedialog.askopenfilename(title='选择PatchConfig文件',
                                                filetypes=[('patch config file', '*.json'),
                                                           ('All Files', '*')], initialdir='../../../../')
        self.import_config_data(patch_file)

    def import_config_data(self, config_path):
        with open(config_path, "r", encoding="utf-8") as config_file_list:
            patch_config_data = json.load(config_file_list)
            for k, v in patch_config_data.items():
                print("Patch Config key : " + str(k) + " value : " + str(v))
            self.TargetPlatform.set(patch_config_data["TargetPlatform"])
            self.VersionNum.set(patch_config_data["VersionNum"])
            self.CleanType.set(patch_config_data["CleanType"])
            self.PatchIndex.set(patch_config_data["PatchIndex"])
            self.PreloadInfo.set(patch_config_data["PreloadInfo"])
            self.pak_type.set(patch_config_data["UnrealPak"])
            print(self.TargetPlatform.get())
            file_list = patch_config_data["FileList"]
            file_list_str = ""
            for file_path in file_list:
                file_list_str += file_path
                file_list_str += "\n"
            self.result_data_Text.insert(1.0, file_list_str)
        self.init_window_name.update()

    def export_config(self):
        patch_config_data = {}
        src = self.result_data_Text.get(1.0, END).strip()
        patch_config_data["FileList"] = src.split('\n')
        patch_config_data["inversiontype"] = self.VersionType.get()
        patch_config_data["VersionNum"] = self.VersionNum.get()
        patch_config_data["TargetPlatform"] = self.TargetPlatform.get()
        patch_config_data["CleanType"] = self.CleanType.get()
        patch_config_data["PatchIndex"] = self.PatchIndex.get()
        print("PreloadInfo : " + self.PreloadInfo.get())
        patch_config_data["PreloadInfo"] = self.PreloadInfo.get()
        patch_config_data["UnrealPak"] = self.pak_type.get()
        dir = filedialog.askdirectory(title='选择存放PatchConfig的文件夹', mustexist=True, initialdir='../../../../')
        config_path = os.path.join(dir, "PatchConfig.json")
        with open(config_path, "w+", encoding="utf-8") as config_file_list:
            json.dump(patch_config_data, config_file_list, indent=4, ensure_ascii=False)

    def call_pak(self):
        src = self.result_data_Text.get(1.0, END).strip()
        infilelist = src.split('\n')
        inversiontype = self.VersionType.get()
        inversion = self.VersionNum.get()
        inplatform = self.TargetPlatform.get()
        incleantype = self.CleanType.get()
        patch_index = self.PatchIndex.get()
        print("PreloadInfo : " + self.PreloadInfo.get())
        need_preload = self.PreloadInfo.get() == "need preload"
        pak_type = self.pak_type.get()
        shader_type = self.shader_type.get()
        need_reference = self.need_reference.get()
        self.write_log_to_Text('--------------------')
        self.write_log_to_Text('开始：' + inversion + ', ' + inplatform + ', ' + incleantype)
        self.write_log_to_Text('文件列表：' + ','.join(infilelist))
        # thread.start_new_thread(tools.Call_From_UI,(infilelist,inversiontype,inversion,inplatform,incleantype,List_State,))
        self.thread = threading.Thread(target=tools.Call_From_UI, args=(
        infilelist, inversiontype, inversion, inplatform, incleantype, List_State, patch_index, need_preload, pak_type,
        shader_type, need_reference))
        self.start_button.config(state="disabled")
        self.init_window_name.config(cursor="wait")
        self.init_window_name.update()

        self.thread.start()
        self.init_window_name.after(50, self.check_completed)
        # self.write_log_to_Text('完成')

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # 日志动态打印
    def write_log_to_Text(self, logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        self.log_data_Text.config(state="normal")
        if LOG_LINE_NUM <= 20:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0, 2.0)
            self.log_data_Text.insert(END, logmsg_in)
        self.log_data_Text.config(state="disabled")

    def print_info(self):
        self.write_log_to_Text('Set TargetPlatform: ' + self.TargetPlatform.get())

    def print_unreal_pak(self):
        self.write_log_to_Text('Set UnrealPak.exe: ' + self.pak_type.get())

    def print_shader_patch(self):
        self.write_log_to_Text('Set shader patch: ' + self.shader_type.get())

    def print_patch_reference(self):
        self.write_log_to_Text('Set patch reference: ' + self.need_reference.get())

    def print_info_version(self):
        self.write_log_to_Text('Set Version: ' + self.VersionType.get() + self.VersionNum.get())

    def print_info_preload(self):
        self.write_log_to_Text('Set preload: ' + self.PreloadInfo.get())

    def print_clean_info(self):
        self.write_log_to_Text('Set TargetPlatform: ' + self.CleanType.get())

    def check_completed(self):
        if self.thread.is_alive():
            if not self.LastStat == List_State[0]:
                self.LastStat = List_State[0]
                self.write_log_to_Text('正在' + self.LastStat + '...')
                self.init_window_name.update()
            self.init_window_name.after(50, self.check_completed)
        else:
            self.start_button.config(state="normal")
            self.init_window_name.config(cursor="")
            self.write_log_to_Text('完成')
            self.write_log_to_Text('--------------------\n')
            self.init_window_name.update()
            List_State[0] = 'Start'
            self.LastStat = 'Start'


def gui_start():
    # cook
    # import os
    # CookerExe = os.path.abspath("./../../../../trunk/Engine/Binaries/Win64/UE4Editor-Cmd.exe")
    # print(CookerExe)

    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    command_param.set_str(sys.argv)
    patch_config_path = command_param.parse_arg(0) or ""
    if not os.path.exists(patch_config_path):
        init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()