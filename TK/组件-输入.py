# Entry 控件是 Tkinter GUI 编程中的基础控件之一，它的作用就是允许用户输入内容。

# 常用语法：Entry( master, option)
# exportselection	默认情况下，如果在输入框中选中文本会复制到粘贴板，如果要忽略这个功能，可以设置为 exportselection=0
# selectbackground	选中文字时的背景颜色
# selectforeground	选中文字时的前景色
# show	指定文本框内容以何种样式的字符显示，比如密码可以将值设为 show=“*”
# textvariable	输入框内值，也称动态字符串，使用 StringVar() 对象来设置，而 text 为静态字符串对象
# xscrollcommand	设置输入框内容滚动条，当输入的内容大于输入框的宽度时使用户

# from tkinter import Tk, StringVar, Label
# import time
#
# win = Tk()
# win.title("Python自学")
# win.geometry('720x480+100+100')
# win.resizable(0, 0)
# win.title('数字的时钟')
#
#
# # 获取时间的函数
# def gettime():
#     # 获取当前时间
#     dstr.set(time.strftime("%H:%M:%S"))
#     # 每隔 1s 调用一次 gettime()函数来获取时间
#     win.after(1000, gettime)
#     win.update()
#
#
# # 生成动态字符串
# dstr = StringVar()
# # 利用 textvariable 来实现文本变化
# lb = Label(win, textvariable=dstr, fg='green', font=("微软雅黑", 85))
# lb.pack()
# # 调用生成时间的函数
# gettime()
# # 显示窗口
# win.mainloop()

# Entry 常用方法 -

# 名称	说明
# delete()	根据索引值删除输入框内的值
# get()	获取输入框内的是
# set()	设置输入框内的值
# insert()	在指定的位置插入字符串
# index()	返回指定的索引值
# select_clear()	取消选中状态
# select_adujst()	确保输入框中选中的范围包含 index 参数所指定的字符，选中指定索引和光标所在位置之前的字符
# select_from (index)	设置一个新的选中范围，通过索引值 index 来设置
# select_present()	返回输入框是否有处于选中状态的文本，如果有则返回 true，否则返回 false。
# select_to()	选中指定索引与光标之间的所有值
# select_range()	选中指定索引与光标之间的所有值，参数值为 start,end，要求 start 必须小于 end。