# 装饰器是一个特殊的闭包函数, 外层函数有且只有一个参数，并且这参数是函数类型


# 装饰器的的定义
def func_out(fn):       # fn=0x11

    def func_inner():   # 0x22
        print("请先登录.....")
        fn()

    return func_inner   # return 0x22

# 装饰器使用方法2：语法糖方式 （写在待装饰函数的上面)
@func_out       # 解释器再加载执行模块时，自动转换成这个代码comment = func_out(comment)，并调用。
def comment():      # 0x11
    print("发表评论....")


if __name__ == '__main__':
    # 装饰器使用方法1：闭包方式调用
    # comment = func_out(comment)     # comment = 0x22

    comment()       # 0x22()



