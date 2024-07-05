import multiprocessing
from multiprocessing import Process, Pool, Queue, Pipe
import os, time, random
"""
【Python】Python多进程详解:https://zhuanlan.zhihu.com/p/493699150， https://www.cnblogs.com/lj-C/p/14893317.html
多进程
作用：多进程可以充分利用多核CPU的计算能力，实现真正的并行计算。
定义：进程是操作系统分配资源的基本单位。每个进程都有自己的内存空间，这意味着进程之间的变量是隔离的，一个进程无法访问另一个进程的变量。
使用场景：
1.多任务处理 -> 在处理多个任务时，可以使用进程来实现并发执行。比如，在一个 Web 服务器中，可以使用进程来处理多个客户端的请求。每个客户端连接到服务器时，服务器可以创建一个进程来处理该客户端的请求，从而实现并发处理多个客户端的请求。
2.计算密集型任务 -> 在进行计算密集型任务时，可以使用进程来充分利用多核 CPU 的性能。比如，在进行图像处理、数据分析等任务时，可以将任务分成多个子任务，并使用进程来并发执行这些子任务，从而加速任务的执行。
3.资源隔离 -> 在进行一些需要资源隔离的任务时，可以使用进程来隔离不同的资源。比如，在进行网络爬虫时，可以将每个网站的爬虫放在一个进程中，从而避免不同的爬虫之间互相干扰。
进程与线程的选择：
在选择进程或线程时，需要根据具体的场景来进行选择。一般来说，进程适合处理 CPU 密集型任务，线程适合处理 I/O 密集型任务。
1.如果需要充分利用多核CPU的性能，可以选择使用进程来实现任务的并发执行。
2.如果需要处理大量的 I/O 操作，可以选择使用线程来实现任务的并发执行。
3.如果需要处理大量的 I/O 操作，可以选择使用线程来实现任务的并发执行。
4.如果需要共享数据，可以选择使用线程来实现数据的共享和同步。
"""

"""
multiprocessing的基本方法：
1.start:进程启动
2.join:join()方法就是让主进程进入阻塞状态，等对应的子进程执行完毕再执行下一行，主要用于进程同步。
3.pool:如果想一次性创建多个进程，可以用Pool方法（注意Pool是一个方法，不是类）
4.进程间的通信:现在设想你需要两个进程，一个进程（接收进程）产生数据（比如从网站上爬虫，或者从websocket接收数据等），另一个进程（转发进程）对产生的数据进行处理并转发（比如计算并处理之后上传数据库，或者发送给websocket等）
方法：Queue和Pipe
"""

# 1.start, join
def run_a_sub_proc(name):
    print(f'子进程：{name}（{os.getpid()}）开始...')
    for i in range(3):
        print(f'子进程：{name}（{os.getpid()}）运行中...')
        time.sleep(1)

# if __name__ == '__main__':
#     print(f'主进程（{os.getpid()}）开始...')
#     p1 = multiprocessing.Process(target=run_a_sub_proc, args=('进程-1', ))
#     p2 = multiprocessing.Process(target=run_a_sub_proc, args=('进程-2', ))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()

# 2.pool
"""
Pool的默认大小是你所用的电脑CPU的核数，CPU核数可通过os.cpu_count()获得。

p.join()的意思是等Pool中所有的子进程全部执行完毕再进行下一步，在调用p.join()之前需要先调用p.close()。
"""
def run_a_sub_proc(name):
    print(f'子进程：{name}（{os.getpid()}）开始！')
    for i in range(2):
        print(f'子进程：{name}（{os.getpid()}）运行中...')
        time.sleep(1)
    print(f'子进程：{name}（{os.getpid()}）结束！')

# if __name__ == '__main__':
#     print(f'主进程（{os.getpid()}）开始...')
#     p = Pool(3)
#     for i in range(1, 5):
#         p.apply_async(run_a_sub_proc, args=(f"进程-{i}",))
#     p.close()
#     p.join()

# 3.进程通信（Queue和Pipe）
"""
Queue可以被多个进程调用，而Pipe只能被两个进程调用；
Queue是基于Pipe实现的，因此Pipe速度比Queue快很多
"""
def recv(q):
    print(f'子进程：接收进程（{os.getpid()}）开始！')
    while True:
        # 用产生随机数的方法模拟数据的接收
        data = random.randint(1, 100)
        print(f'子进程：接收进程接收到数据{data}！')
        q.put(data)
        sleep_time = random.randint(1, 3)
        time.sleep(sleep_time)

def send(q):
    print(f'子进程：转发进程（{os.getpid()}）开始！')
    while True:
        # 注意：如果q里面没有数据，get()方法就会等待，直到获得一个数据并赋值给data
        data = q.get()
        print(f'子进程：转发进程接收到数据{data}并开始处理、转发！')
        time.sleep(1)

# if __name__ == '__main__':
#     print(f'主进程（{os.getpid()}）开始...')
#     q = Queue()
#     p1 = Process(target=recv, args=(q,))
#     p2 = Process(target=send, args=(q,))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()

def sub_process(name, p):
    print(f'子进程：{name}（{os.getpid()}）开始！')
    while True:
        data_s = random.randint(1, 100)
        p.send(data_s)
        print(f'子进程：{name}发送数据：{data_s}！')
        data_r = p.recv()
        print(f'子进程：{name}接收到数据：{data_r}！')
        time.sleep(1)

# if __name__ == '__main__':
    # print(f'主进程（{os.getpid()}）开始...')
    # conn_1, conn_2 = Pipe()
    # p1 = Process(target=sub_process, args=("进程-1", conn_1,))
    # p2 = Process(target=sub_process, args=("进程-2", conn_2,))
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()

import multiprocessing
import os.path as osp
import shutil

def copy_file(file_path, out_path):
    shutil.copyfile(file_path, osp.join(out_path, osp.basename(file_path)))

def copy_folder(src_folder, out_folder):
    # 在目标文件夹中创建一个与源文件夹相同的文件结构
    dst_folder = osp.join(out_folder, osp.basename(src_folder))
    if not osp.exists(dst_folder):
        shutil.copytree(src_folder, dst_folder)

    # 使用进程池递归复制文件
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        for root, _, files in os.walk(src_folder):
            for file in files:
                file_path = osp.join(root, file)
                pool.apply_async(copy_file, args=(file_path, dst_folder))
                print("11111")
        pool.close()  # 关闭进程池
        pool.join()  # 等待进程池中的所有进程完成

    print(f'Folder {src_folder} copied to {dst_folder} successful!')

if __name__ == '__main__':
    copy_folder(r'E:\C++配套资源', r'E:\\xcl')





