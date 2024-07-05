num1 = 100

def func_out(num1): #num1=1

    def func_inner(num2):   # num2=1

        # 定义了一个新的num1变量，而不是修改外层函数变量
        #num1 = 10

        # 声明使用全局的num1
        # global num1

        # 声明使用外部函数的变量num1
        nonlocal num1
        num1 = 10

        result = num1 + num2
        return result


    print(num1)     # 1
    func_inner(1)   #
    print(num1)     # 10


    return func_inner

if __name__ == '__main__':

    f = func_out(1)
