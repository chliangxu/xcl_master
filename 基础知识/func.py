import os
import string
import random
import time
import json

# 创建一个迭代器类
class MyIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        value = self.data[self.index]
        self.index += 1
        return value


class Func:

    def new_func(self):
        # 1.匿名函数
        if not Func.first_func(self):
            return False

        return True

    def first_func(self):
        ret = lambda a, b: a + b
        print(ret(2, 3))
        li = [1, 2, 3, 4, 5]
        new_ret = map(lambda a: a + 10, li)
        print(list(new_ret))

    # 随机生成字母和数字
    def two_func(self, n):
        """
        ascii_lowercase:小写的字母（a-z）
        ascii_lowercase:大写的字母（A-Z）
        ascii_letters:所有的字母（a-z和A-Z）
        :return: 随机的产生字母数（n）
        """
        all_chs = string.ascii_letters + string.digits
        need_str = [random.choice(all_chs) for i in range(n)]
        finally_str = "".join(need_str)
        print(f"类型是{type(finally_str)}\n"
              f"输出的内容{finally_str}")
        return finally_str

    # 生成器
    """ 按块读取 """
    def read_file_by_chunk(self, file, chunk_size=512):
        with open(file, mode='r', encoding='utf-8') as f:
            while True:
                chunk = f.readline()
                if not chunk:
                    return
                yield chunk


# start_time = time.time()
# chunks = Func().read_file_by_chunk(r"E:\xcl\xcl_master\AC_output.ips")
# # chunks = Func().read_file_by_chunk(r"E:\xcl\xcl_master\197_anr_trace_output_Release.txt")
# lis = []
# for chunk in chunks:
#     print("/////////////////", type(chunk), chunk, end='',)
#
#     if "uuid" in chunk or "path" in chunk:
#         lis.append(chunk)
# # print(lis)
# # print(len(lis))
# for index, i in enumerate(lis):
#     print(index, i)
#     if "/AClient.app\/AClient" in i:
#         print(index, i)
#         print(lis[index - 1])
#         break

    # if "/lib/arm64/libUE4.so" in chunk:
    #     old_str = "("
    #     new_str = " "
    #     tw_str = ")"
    #     finally_str = chunk.replace(old_str, new_str).replace(tw_str, new_str)
    #     str_split = finally_str.split(" ")
    #     print(str_split)
    #     if str_split[-3] == "BuildId:":
    #         lis.append(str_split[-2])

