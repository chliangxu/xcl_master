# 1.创建窗口实例
# http://m.biancheng.net/view/jlwcjve.html

from tkinter import *
from tkinter import messagebox
import tkinter as tk
root = tk.Tk()
root.geometry("400x150")

txt = IntVar()
txt.set(0)

rado_list = ["python中文网", "CSDN平台"]

def show_info():
    str_info = "选择了" + rado_list[txt.get()] + "祝您学习愉快"
    messagebox.showinfo("提示", str_info)

for i,item in enumerate(rado_list):
    Radiobutton(root, text=item, variable=txt, value=i, command=show_info).pack(anchor="w")

root.mainloop()