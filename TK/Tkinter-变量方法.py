# x = IntVar()：整型变量，默认是0
# x = DoubleVar()：浮点型变量，默认是0.0
# x = StringVar()：字符串变量，默认是""
# x = BooleanVar()：布尔型变量，True是1，False是0

# import tkinter
#
# def click():
#     if x.get() == "":
#         x.set("Python!!!")
#     else:
#         x.set("")
#
# root = tkinter.Tk()
# x = tkinter.StringVar()
# # textvariable 是可变的，会跟随字符串变而自动变内容
# label = tkinter.Label(root, textvariable=x, bg="lightyellow", fg="red", font="Verdana 18 bold", width=15, height=2)
# label.pack()
#
# button = tkinter.Button(root, text="请点击", command=click)
# button.pack()
#
# root.mainloop()

# 追踪trace() 使用模式 w
import tkinter

# 这里必须要加入*args，具体下面细说
# def show(*args):
#     print("数据：", string.get())
#
# root = tkinter.Tk()
# string = tkinter.StringVar()
# entry = tkinter.Entry(root, textvariable=string)
# entry.pack(padx=5, pady=10)
# string.trace("w", show)
#
# root.mainloop()

import tkinter

def show(*args):
    Tr.set(Tw.get())

def getting(*args):
    print("警告！！正在被读取数据")

def hit():
    print("数据为：", Tw.get())

root = tkinter.Tk()
Tw = tkinter.StringVar()
entry = tkinter.Entry(root, textvariable=Tw)
entry.pack(padx=5, pady=10)
Tw.trace("w", show)
Tw.trace("r", getting)

Tr = tkinter.StringVar()
label = tkinter.Label(root, textvariable=Tr)
Tr.set("同步显示")
label.pack(padx=5, pady=10)

button = tkinter.Button(root, text="点击读取", command=hit)
button.pack(padx=5, pady=10)

root.mainloop()
