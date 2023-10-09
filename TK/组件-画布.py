# 1.创建Canvas对象和添加绘图对象
import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=800, height=800)
canvas.pack()

# rectangle = canvas.create_rectangle(50, 50, 150, 150, fill='red')
# oval = canvas.create_oval(100, 100, 200, 200, fill='blue')
#
# # 修改矩形的颜色
# canvas.itemconfig(rectangle, fill='green')
#
# # 删除椭圆
# canvas.delete(oval)

# 前两个参数表示图像的中心坐标
# 绘制文本
text = canvas.create_text(150, 50, text='Hello, world!', font=('Arial', 16))

# 绘制图像
image = tk.PhotoImage(file='python.gif')
canvas.create_image(350, 350, image=image)

root.mainloop()
