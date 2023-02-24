import time
import os,sys
import requests
import shutil

def move_file():
    import shutil
    import os
    from_file_path = input("输入你需要移动文件的路径")
    to_file_path = input("输入你移动之后的文件路径")
    if os.path.exists(from_file_path):
        file_num = len(os.listdir(from_file_path))
        # shutil.move(from_file_path, to_file_path)
    else:
        print("文件夹不存在，不能执行移动文件夹操作")


def progress_bar(file_num):
    start = time.perf_counter()
    for i in range(1, file_num + 1):
        finsh = "▓" * i
        need_do = "-" * (t - i)
        progress = (i / t) * 100
        print("progress", progress)
        dur = time.perf_counter() - start
        print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(progress, finsh, need_do, dur), end="")
        time.sleep(0.05)

def finally_file():
    pass
if __name__ == '__main__':
#     # move_file()
    from_file_path = input("路径")
    progress_bar(from_file_path)
# t = 100
# start = time.perf_counter()
# for i in range(t + 1):
#     print(i)
#     finsh = "▓" * i
#     need_do = "-" * (t - i)
#     progress = (i / t) * 100
#     print("progress", progress)
#     dur = time.perf_counter() - start
#     print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(progress, finsh, need_do, dur), end="")
#     time.sleep(0.05)