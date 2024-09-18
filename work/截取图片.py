import pyautogui
import time
import pygetwindow as gw
import webbrowser
import numpy as np
from PIL import ImageGrab

import webbrowser

# 打开默认浏览器并访问指定 URL
url = "https://s.bkdevops.qq.com/1PvAxW0Q"
webbrowser.open(url)

# 延时，等待网页加载完成
time.sleep(3)

# 获取浏览器窗口
browser_window = gw.getWindowsWithTitle('蓝盾DevOps平台')
for window in browser_window:
    print(window)

print(pyautogui.size())
#
# # # 将光标移动到浏览器窗口，确保下一步的截图是对的
pyautogui.moveTo(pyautogui.size()[0]/2, pyautogui.size()[1]/2)

# 指定截图区域，这里的坐标要根据实际情况进行调整
region = (1150, 370, 1400, 600)

# 截图
screenshot = ImageGrab.grab(region)
screenshot.show()

# 或者保存图片
screenshot.save('screenshot.png')