from tkinter import *
# 1.按钮布局（pack）
# widget.pack(options)
# 使用 pack() 方法布局控件
# label1.pack(expand=True, fill="both", side="top", anchor="n")

# widget：表示需要布置的控件
# options -> 表示可选的参数
# expand：设置为 True 时，控件可以扩大以填充空白区域。
# fill：设置为 “x” 时，控件在水平方向上可伸展。
# fill：设置为 “y” 时，控件在垂直方向上可伸展。
# fill：设置为 “both” 时，控件在水平和垂直方向上可伸展。
# side：指定控件在容器中停靠的位置，可以是 “top”、”bottom”、”left” 或 “right”。
# anchor：控制控件在容器中的位置，可以是 “n”、”e”、”s”、”w”、”center”、”ne”、”nw”、”se” 或 “sw”。

# text：按钮上显示的文本。
# width：按钮的宽度。
# height：按钮的高度。
# bg：按钮的背景颜色。
# fg：按钮上文本的颜色（前景颜色）。
# font：按钮上文本的字体。
# command：按钮被点击时触发的函数

# 示例代码
# 创建按钮，并且给按钮添加点击事件（2-1, ）
# import tkinter as tk
# from tkinter import messagebox
# root = tk.Tk()  # 创建窗口
# root.title('演示窗口')
# root.geometry("300x100+630+80")  # (宽度x高度)+(x轴+y轴)
#
# btn1 = tk.Button(root)  # 创建按钮，并且将按钮放到窗口里面
# btn1["text"] = "点击"  # 给按钮一个名称
# btn1.pack()  # 按钮布局
#
#
# def test(e):
#     '''创建弹窗'''
#     messagebox.showinfo("窗口名称", "点击成功")
#
#
# btn1.bind("<Button-1>", test)  # 将按钮和方法进行绑定，也就是创建了一个事件
# root.mainloop()  # 让窗口一直显示，循环

count = 0

def add():
    global count
    count += 1
    lbl.config(text=str(count))

root = Tk()

lbl = Label(root, text=str(count), font=('Arial', 24))
lbl.pack()

btn = Button(root, text='点击增加', font=('Arial', 16), command=add)
btn.pack()

mainloop()










