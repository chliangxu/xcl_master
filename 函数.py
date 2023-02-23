import os

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


# Func().new_func()


def get_work_path():
    working_dir = os.getcwd()
    work_path = os.path.join(working_dir, "stiff")
    if not os.path.exists(work_path):
        os.mkdir(work_path)
        print("old_work_path", type(work_path), work_path)
    return work_path
    # return work_path

def get_path():
    print(get_work_path())
    work_path = os.path.join(get_work_path(), "new")
    print("111", work_path)

print(get_path())