# 捕获键盘事件
from tkinter import *

root = Tk()

def callback(event):
    print("敲击位置：", repr(event.char))
    return event.char

frame = Frame(root, width=200, height=200)
frame.bind("<Key>", callback)
frame.focus_set()

frame.pack()
frame.focus_set()
mainloop()

# 捕获点击鼠标的位置

root = Tk()

def callback(event):
    print("点击位置：", event.x, event.y)

frame = Frame(root, width=200, height=200)
frame.bind("<Button-1>", callback)
frame.pack()
#
mainloop()