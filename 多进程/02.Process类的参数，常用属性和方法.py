

class Processid:

    """
    参数的意义：
    group：该参数未进行实现， 不需要传参
    target：为新建进程指定执行任务，也就是指定一个函数；
    name：为新建进程设置名称；
    args：为 target 参数指定的参数传递非关键字参数；
    kwargs：为 target 参数指定的参数传递关键字参数。
    """

    def __init__(self,group=None,target=None,name=None,args=(),kwargs={}):
        pass

"""
Process类常用属性和方法:
run()：第 2 种创建进程的方式需要用到，继承类中需要对方法进行重写，该方法中包含的是新进程要执行的代码。
start()：和启动子线程一样，新创建的进程也需要手动启动，该方法的功能就是启动新创建的线程。
join([timeout])：在多进程执行过程，其他进程必须等到调用 join() 方法的进程执行完毕（或者执行规定的 timeout 时间）后，才能继续执行；
"""