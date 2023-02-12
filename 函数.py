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

    def two_func(self):
        pass


Func().new_func()
