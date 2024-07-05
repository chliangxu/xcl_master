

def func_out(fn):   # fn=foo=0x11

    def func_inner(a, b):   # 0x22

        print("新增的功能 ....")
        fn(a, b)

    return func_inner



@func_out       # foo=func_out(foo) --> foo=0x22
def foo(a, b):  # 0x11
    result = a + b
    print("结果:", result)

if __name__ == '__main__':
    foo(1, 2)   # 0x22(1,2)

