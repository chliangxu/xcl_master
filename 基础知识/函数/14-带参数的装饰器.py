
# 带参数的装饰器: 在装饰器 外层 套一层函数，实现闭包。使用闭包接收参数


def logging(flag):  # flag="+"   flag="-"

    def func_out(fn):   # fn=0x11

        def func_inner(*args, **kwargs):    # 0x22
            if flag == "+":
                print("做加法运算功能....")
            elif flag == "-":
                print("做减法运算功能....")
            result = fn(*args, **kwargs)    # 0x11
            return result

        return func_inner


    return func_out


@logging("+")       # 执行顺序: 1. logging("+") 2. @func_out -> add=func_out(add) -> add=0x22
def add(a, b):      # 0x11
    result = a + b
    return result


@logging("-")       # 执行顺序: 1. logging("-") 2. @func_out -> sub=func_out(sub) -> sub=0x22
def sub(a, b):
    result = a - b
    return result


if __name__ == '__main__':

    result = add(10, 20)    # 0x22(10, 20)
    print(result)


    result = sub(100, 50)
    print(result)

