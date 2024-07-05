
def func_out(fn):   # fn=foo=0x11

    def func_inner(*args, **kwargs):    # 0x22
        print("新增功能....")
        result = fn(*args, **kwargs)     # 0x11(*args, **kwargs)
        return result

    return func_inner

@func_out
def foo():
    print("发表评论")

@func_out
def foo1(a, b):
    result = a + b
    print("foo1: ", result)

@func_out
def foo2(a, b, c, d):
    result = a + b + c + d
    print("foo2: ", result)

@func_out
def foo3(a, b, c):
    result = a + b + c
    return result

if __name__ == '__main__':

    foo()
    foo1(10, 20)
    foo2(1,2,3,4)
    result = foo3(100,200,300)
    print(result)


