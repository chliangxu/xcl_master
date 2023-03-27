
def func_out(fn):   # fn=foo=0x11

    def func_inner(*args, **kwargs):    # 0x22
        print("新增功能....")
        result = fn(*args, **kwargs)     # 0x11(*args, **kwargs)
        return result

    return func_inner


@func_out       # foo=func_out(foo)  --> foo = func_inner = 0x22
def foo(a, b):  # 0x11
    result = a + b
    return result


if __name__ == '__main__':

    result = foo(10, 20)    # foo(10, 20) --> 0x22(10, 20)
    print("result: ", result)

