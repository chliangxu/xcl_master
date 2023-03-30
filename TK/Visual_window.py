import tkinter as tk

root=tk.Tk()
root.geometry('300x240')
txt = tk.StringVar()
T=tk.Text(root,font=('宋体',12),width=50,height=3)
var2='Tkinter'
var1 = "12345"
T.insert('1.0',var2)
T.insert('end',var1)
T.place(x=175,y=180)

root.mainloop()