# 1.基本用法
# import tkinter as tk
#
# root = tk.Tk()
# root.title("标签示例")
#
# label = tk.Label(root, text="这是一个标签")
# label.pack()
#
# root.mainloop()

# 2.标签的属性
# text：标签中显示的文本。
# width：标签的宽度。
# height：标签的高度。
# bg：标签的背景颜色。
# fg：文本的颜色（前景颜色）。
# font：文本的字体。
# image：标签中显示的图像。
# compound：图像和文本的位置关系。

import tkinter as tk
#
# root = tk.Tk()
# root.title("自定义标签")
#
# label1 = tk.Label(root, text="红色文本", fg="red", bg="white")
# label1.pack()
#
# label2 = tk.Label(root, text="宋体字体", font=("宋体", 16))
# label2.pack()
#
# label3 = tk.Label(root, text="宽高", width=20, height=5, bg="yellow")
# label3.pack()
#
# photo = tk.PhotoImage(file="python.gif")
# label4 = tk.Label(root, image=photo, compound="center")
# label4.pack()
#
# root.mainloop()

# 绑定事件
import tkinter as tk

def click(event):
    print("鼠标单击了标签")

root = tk.Tk()
root.title("绑定事件")

label = tk.Label(root, text="单击这里", fg="red", bg="white")
label.pack()

label.bind("<Button-1>", click)

root.mainloop()
