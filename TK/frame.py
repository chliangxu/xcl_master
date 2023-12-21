from tkinter import *
from tkinter import messagebox
import tkinter as tk
import time

LOG_LINE_NUM = 0

class FILE_SHOW():
    def __init__(self, init_window):
        self.init_window_name = init_window
        self.arguments = StringVar(self.init_window_name, "PSO和PGO")
        # self.other_arguments = StringVar(self.init_window_name, "其他参数")





    def set_init_window(self):
        self.init_window_name.title("GNGame构建常用工具")
        self.init_window_name.geometry("1200x530+200+200")


        self.FM1 = Frame(self.init_window_name, borderwidth=10)
        self.FM1.grid(sticky=NW)
        self.target_label = Label(self.FM1, text="流水线参数:")
        self.target_label.grid(row=0, column=0, sticky=NW)

        self.TP1 = Radiobutton(self.FM1, text="PSO和PGO", variable=self.arguments, value='PSO和PGO', command=self.print_info).grid(row=0, column=1, padx=20, sticky=NW)
        self.TP2 = Radiobutton(self.FM1, text="其他参数", variable=self.arguments, value='其他参数', command=self.print_info).grid(row=0, column=3, sticky=NW)
        # self.file_button_1 = Button(self.FM1, text="显示流水线参数列表", width=10, command=self)
        self.FM2 = Frame(self.init_window_name, borderwidth=10)
        self.FM2.grid(row=5, column=0, rowspan=10, columnspan=5, sticky=NW)
        self.log_label = Label(self.FM2, text="日志")
        self.log_label.grid(row=0, column=0, sticky=NW)
        self.log_data_Text = Text(self.FM2, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=1, column=0, columnspan=5, sticky=NW)
        self.log_data_Text.config(state="disabled")


    def print_info(self):
        print("111", self.arguments.get(), type(self.arguments))
        self.write_log_to_Text('Set arguments: ' + self.arguments.get())
        self.show_info()

    # 动态写入日志
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

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    def select_file_arguments(self):
        pass

    def show_info(self):
        str_info = "选择了" + "测试" + "您学习愉快"
        messagebox.showinfo("提示", str_info)

def login():
    init_window = tk.Tk()  # 实例化出一个父窗口
    file_list_show = FILE_SHOW(init_window)
    file_list_show.set_init_window()
    init_window.mainloop()

login()