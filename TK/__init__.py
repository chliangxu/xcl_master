import tkinter as tk
root=tk.Tk()
root.geometry('300x240')
# a.控件Entry
# 1.设置背景颜色
bg = "red" # bg = background
b1=tk.Entry(root,bg='red',width=20)

# 2. 设置文字的颜色
fg = "red" # fg = foreground
b1=tk.Entry(root,width=20,fg='red')

# 3. 设置输入文字的字体。
# 3.1.side='left'：将输入框放在当前界面的左边居中

# 3.2.side='right' ：将输入框放在当前界面的右边居中

# 3.3.side='top'：将输入框放在当前界面的顶部居中

# 3.4.side='bottom'：将输入框放在当前界面的底部居中

txt = tk.StringVar() # 关联的tkinter变量，一般是StringVar类型。如果该变量改变，则输入控件中的内容也会更新。接收一个字符串
E=tk.Entry(root,textvariable=txt,font=('宋体',12),bg='white',fg='black',width=20)
E.pack(side='left')
E.place(x=100,y=100) # x表示到界面最左边的距离，y表示到界面最右边的距离

# 4.在文本框中插入一个字符串, 'end'表示在当前文本框里最后的位置继续插入 , '1.0'表示在当前文本框前面的位置插入
var2='Tkinter'
var1 = "12345"
E.insert('1.0',var2)
E.insert('end',var1)