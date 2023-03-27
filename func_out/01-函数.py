# python中一切皆对象;
#   函数名就是function对象

#   函数名(): 跳转到函数的入口地址，执行代码;



def foo():
    print("foo函数")

def foo2():
    print("foo2函数")

if __name__ == '__main__':
    foo()

    print(foo)

    f = foo

    print(f)

    f()

    foo()

    foo=foo2

    foo()

