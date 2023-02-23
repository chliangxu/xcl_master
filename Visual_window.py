# 可视化窗口的代码

from tkinter import *
from tkinter import messagebox

def func():
    print("我是黄同学")

# 创建窗口：实例化一个窗口对象
win = Tk()

# 窗口大小
win.geometry("600x450")

#  窗口标题
win.title("我的个性签名设计")


# 添加标签控件
label = Label(win, text="签名", font=("宋体",25),fg="red")

# 定位
label.grid()
"""
label.grid()等价于label.grid(row=0,column=0)
"""

"""
text参数用于指定显示的文本；
font参数用于指定字体大小和字体样式；
fg参数用于指定字体颜色；
"""


# 添加输入框
entry = Entry(win, text="签名", font=("宋体",25),fg="red")
entry.grid(row=0,column=1)
"""
row=0,column=1表示我们将输入框控件，放在第1行第2列的位置；
python语言中，这个下标是从0开始的。
"""

# 添加点击按钮
button = Button(win,text="签名设计",font=("宋体",25),fg="blue", command=func)
button.grid(row=1,column=1)

# 显示窗口
win.mainloop()