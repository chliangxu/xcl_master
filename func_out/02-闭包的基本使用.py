# 1.存在函数嵌套定义
# 2.内层函数需要调用外层函数的变量(使得外层函数的变量的引用计数不为0，这个变量不会销毁)
# 3.外层函数返回内层函数名

# 闭包：使用外层函数变量的这个内层函数就是闭包

# 闭包作用：保证外层函数调用完后，函数中的变量不会销毁。

def func_out(num1): # num1=1

    def func_inner(num2):   # num2=3

        result = num1 + num2
        print("result: ", result)

    return func_inner


if __name__ == '__main__':

    f = func_out(1)     # f = func_inner

    f(2)                # f(2) --> func_inner(2)
    f(3)                # f(3) --> func_inner(3)

