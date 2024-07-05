# 装饰器的内层函数原型 应该 跟待装饰的函数的原型一致

def func_out(fn):   # fn=foo=0x11

    def func_inner(*args, **kwargs):   # 0x22

        print("新增功能....")
        # print(args, kwargs)
        fn(*args, **kwargs)

    return func_inner


@func_out       # foo=func_out(foo)   --> foo = 0x22
def foo(*args, **kwargs):   # 0x11
    print(args)
    print(kwargs)
    a, b = args
    c = kwargs['c']
    result = a + b + c
    print("结果: ", result)


if __name__ == '__main__':
    foo(1, 2, c=100)        # 0x22(1, 2, c=100)

