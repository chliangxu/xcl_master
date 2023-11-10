# python的序列化，反序列化和异常处理 https://blog.csdn.net/weixin_62623950/article/details/128483266
# 序列化和反序列化的意义
# 1.通过文件操作，我们可以将字符串写入到一个本地文件中，但是如果是一个对象（列表，字典，元组）的话，就无法写入到文件里，需要将这个文件进行序列化
#   然后才能写入到文件里。设计一套协议，按照某种规则，将内存中的数据转换成字节序列，保存到文件，这就是序列化，反之就是将文件中的字节序列恢复到内
#   存中，这就是反序列化。
#   JSON和PICKLE两个模块用来实现数据的序列化和反序列化

# 2.json本质上就是字符串，区别在于json里要是使用双引号表示字符串。json用于不同平台来传送数据
# 序列化和反序列化的两个办法
# 序列化：dumps(将python中的数据转换成二进制)，dump(将python中的数据转换成二进制，同时保存大指定文件)
# 反序列化：loads(将二进制加载成python数据)，load(读取文件，并将文件的二进制内容加载成python数据)
import json
names = ["zhangsan", "lisi", "jack", "peter"]
x = json.dumps(names)

file = open("name.txt", "w", encoding="utf-8")
file.write(x)
file.close()

json.dump(names, file)
file.close()