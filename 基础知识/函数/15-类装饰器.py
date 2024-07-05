
# def func_out(fn):
#
#     def func_inner(*args, **kwargs):
#
#         print("请先登录....")
#         result = fn(*args, **kwargs)
#         return result
#
#     return func_inner

class func_out(object):

    def __init__(self, fn):
        self.__fn = fn      # self.__fn=0x11

    # 对象() --> 自动调用__call__ 这个方法
    def __call__(self, *args, **kwargs):
        print("请先登录....")
        self.__fn()


@func_out       # comment = func_out(comment)
def comment():  # 0x11
    print("发表评论....")


if __name__ == '__main__':
    comment()   # 对象() --> __call__() --> fn --> comment()