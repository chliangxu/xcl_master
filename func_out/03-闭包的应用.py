# 需求: 根据配置信息使用闭包实现不同人的对话信息，例如对话:
#
# 张三: 到北京了吗?
# 李四: 已经到了，放心吧。

# 闭包的作用：保证函数调用完后，函数中的变量不会销毁;

def config_name(name):

    def say_info(info):
        print(name + ":" + info)

    return say_info

if __name__ == '__main__':

    zhangsan = config_name("张三")
    zhangsan("在吗？约吗?")

    lisi = config_name("李四")
    lisi("不约，学习python.")
