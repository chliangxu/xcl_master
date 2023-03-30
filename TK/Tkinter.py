# java -jar E:\GNGame\buglySymbolAndroidV2.jar -i D:\install\包\lingshi\Android\libUE4.so -u -id ceba63c445 -key 38a91667-0d01-4beb-bc30-167584487923 -url https://crashsight.qq.com/openapi/file/upload/symbol
from tkinter import *
import hashlib
import time
import os


# class MY_BUGLY():
#
#     def __init__(self,init_window_name):
#         self.init_window_name = init_window_name
#
#     # 设置窗口
#     def set_init_window(self):
#         root = self.init_window_name.title("bugly上传工具")
#         self.init_window_name.geometry('1068x681+10+10')
#
#         # 标签
#         self.init_window_name.Entry(root, show= "*").pack()
#
#         self.init_window_name = Button(root, text = "insert point", width = 15, hight = 2, command=insert_point)
#
#     def insert_point(self):
#
#
# def gui_start():
#     init_window = Tk()              #实例化出一个父窗口
#     ZMJ_PORTAL = MY_BUGLY(init_window)
#     # 设置根窗口默认属性
#     ZMJ_PORTAL.set_init_window()
#
#     init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
#
#
# gui_start()


# coding=utf-8
import tkinter as tk

# 主窗口
win = tk.Tk()
win.geometry("300x200+400+200")
win.title("Tkinter Entry 用法")


# 创建验证子程序
def test():
    if e1.get() == "test":
        print("正确！")
        return True
    else:
        print("错误！")
        e1.delete(0, "end")
        return False


v = tk.StringVar()
# 第一行
l1 = tk.Label(text="验证码：").grid(row=0, column=0)
e1 = tk.Entry(win, textvariable=v, validate="focusout", validatecommand=test)
e1.grid(row=0, column=1)
# 第二行
l2 = tk.Label(text="验证结果").grid(row=1, column=0)
e2 = tk.Entry(win).grid(row=1, column=1)

# 开始窗口的事件循环
win.mainloop()