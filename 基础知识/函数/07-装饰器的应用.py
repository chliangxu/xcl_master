
# 函数执行时间的统计


import time


def func_out(fn):       # fn=0x11

    def func_inner():   # 0x22
        start = time.time()
        fn()            # 0x11()
        end = time.time()
        print("函数共花费时间: %f " % (end-start))

    return func_inner   # return 0x22


@func_out       # foo=func_out(foo)  ---> foo = 0x22
def foo():      # 0x11

    for i in range(100000):
        print(i)



if __name__ == '__main__':
    foo()       # 0x22()




