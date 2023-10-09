'''
用tkinter制作一个图形化定时器
'''
from tkinter import *
from tkinter import messagebox
import io
import threading
import win32gui, winsound
import argparse


class Timer:
    def __init__(self, Minutes, Seconds):
        self.state = {'isStop': False, 'minutes': Minutes, 'seconds': Seconds}
        self.createContainer()

    # 创建容器
    def createContainer(self):
        # 创建窗口实例
        self.window = Tk()
        self.window.title('Timer')
        # 禁止全屏
        self.window.resizable(False, False)

        self.addWidgets()
        # 开启定时
        self.startTimer()
        # 修改主窗口退出协议
        self.window.protocol('WM_DELETE_WINDOW', self.closeWindow)

        # 返回屏幕的宽高
        # win_w = self.tk.winfo_screenwidth()
        # win_h = self.tk.winfo_screenheight()
        # 返回需要的宽高
        x = self.window.winfo_reqwidth()
        y = self.window.winfo_reqheight()
        # 设置初始位置
        self.window.geometry("%dx%d+%d+%d" % (400, 200, 20, 20))
        # 修改图标(对启动速度有点影响)
        # self.window.iconbitmap('title.ico')
        # 主事件循环
        self.window.mainloop()

    # 添加组件
    def addWidgets(self):
        self.Minutes = IntVar()
        self.Minutes.set(self.state['minutes'])
        self.Seconds = IntVar()
        self.Seconds.set(self.state['seconds'])
        # relief :设置3D效果
        self.e_minutes = Entry(self.window, relief=RAISED, justify=RIGHT, font='Helvetica 34 bold', state='readonly',
                               width=2, textvariable=self.Minutes)
        self.e_seconds = Entry(self.window, relief=RAISED, justify=RIGHT, font='Helvetica 34 bold', state='readonly',
                               width=2, textvariable=self.Seconds)
        self.btn_stop_start = Button(self.window, text='Start', font='Helvetica 10', width=10, command=self.changeTimer)
        self.btn_reset = Button(self.window, text='Reset', font='Helvetica 10', width=10, command=self.resetTime)

        # 组件布局
        self.e_minutes.grid(row=0, column=0, rowspan=2)
        Label(self.window, font='Helvetica 25 bold', text=':').grid(row=0, column=1, rowspan=2)  # 装饰作用
        self.e_seconds.grid(row=0, column=2, rowspan=2)
        self.btn_stop_start.grid(row=0, column=3, sticky='e')
        self.btn_reset.grid(row=1, column=3, sticky='e')

    # 更新时间
    def updateTime(self):
        # 避免按下暂停，线程还在执行
        if self.state['isStop'] == True:
            return
        if self.Seconds.get() > 0:
            self.Seconds.set(self.Seconds.get() - 1)
            self.window.update()
        elif self.Seconds.get() == 0 and self.Minutes.get() > 0:
            self.Seconds.set(59)
            self.Minutes.set(self.Minutes.get() - 1)
            self.window.update()

        elif self.Seconds.get() == 0 and self.Minutes.get() == 0:  # 没时间了，发声提示
            self.Seconds.set(0)
            self.window.update()
            self.state['isStop'] = True  # 用于停止刷新时间
            self.alert()
        self.startCicle()

        # 关闭窗口

    def closeWindow(self):
        if self.state['isStop'] == False:
            if messagebox.askyesno('It`s not time.', 'Are you sure stop?'):
                self.state['isStop'] = True
                self.window.quit()
        else:
            self.window.quit()

    # 重置时间
    def resetTime(self):
        self.Minutes.set(self.state['minutes'])
        self.Seconds.set(self.state['seconds'])

    # 更改定时状态
    def changeTimer(self):
        if self.state['isStop'] == True:
            self.state['isStop'] = False
            self.startTimer()
        else:
            self.state['isStop'] = True
            self.stopTimer()

    # 开启循环
    def startCicle(self):
        if self.state['isStop'] == True:
            return
        threading.Timer(1, self.updateTime).start()

    # 开始定时
    def startTimer(self):
        # 在时间停止时，可以修改定时时间
        self.state['minutes'] = self.Minutes.get()
        self.state['seconds'] = self.Seconds.get()
        self.e_minutes['state'] = 'readonly'
        self.e_seconds['state'] = 'readonly'
        self.btn_stop_start['text'] = 'Stop'
        self.window.update()
        self.startCicle()

    # 暂停定时
    def stopTimer(self):
        self.btn_stop_start['text'] = 'Start'
        self.e_minutes['state'] = 'normal'
        self.e_seconds['state'] = 'normal'
        self.window.update()

    # 发声提示
    def alert(self):
        winsound.Beep(600, 3000)  # 发出声音提示 默认闹3s


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=int, default=3, help='set minutes for timer')
    parser.add_argument('-s', type=int, default=0, help='*set seconds for timer')
    args = parser.parse_args()
    Timer(args.m, args.s)

