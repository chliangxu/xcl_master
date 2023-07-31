import os
import string
import random

class Func:

    def new_func(self):
        # 1.匿名函数
        if not Func.first_func(self):
            return False

        return True

    def first_func(self):
        ret = lambda a,b:a+b
        print(ret(2,3))
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
        need_str = [ random.choice(all_chs) for i in range(n)]
        finally_str = "".join(need_str)
        print(f"类型是{type(finally_str)}\n"
              f"输出的内容{finally_str}")
        return finally_str



Func().two_func(9)

