import time

def time_master(func):
    def call_func():
        print("计时器开始：函数开始调用：")
        start_time = time.time()
        func()
        end_time = time.time()
        print('计时器结束，函数调用完成')
        return print(f'计时器结果返回：函数调用耗时{end_time-start_time:.2f}')
    return call_func

@time_master
def move_file():
    import shutil
    import os
    from_file_path = input("输入你需要移动文件的路径")
    to_file_path = input("输入你移动之后的文件路径")
    filelist = os.listdir(from_file_path)  # 列出该目录下的所有文件,listdir返回的文件列表是不包含路径的。
    for file in filelist:
        src = os.path.join(from_file_path, file)
        dst = os.path.join(to_file_path, file)
        print('src:', src)
        print('dst:', dst)
        shutil.move(src, dst)


if __name__ == '__main__':
    move_file()