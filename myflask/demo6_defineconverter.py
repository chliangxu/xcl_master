from flask import Flask, request

# 1.创建Flask项目的应用对象
# __name__作用：当前py文件所在的目录是Flask项目目录，会在项目目录下寻找静态文件夹[图片 css]，模板文件夹[html]
app = Flask(__name__)
"""
DEFAULT_CONVERTERS = {
    "default": UnicodeConverter,
    "string": UnicodeConverter,
    "any": AnyConverter,
    "path": PathConverter,
    "int": IntegerConverter,
    "float": FloatConverter,
    "uuid": UUIDConverter,
    # 自定义一个键值对
    "mobile": PhoneConverter,
}
"""

from werkzeug.routing import BaseConverter

# 1.自定义转换器类继承于BaseConverter
class PhoneConverter(BaseConverter):
    # 2.重写父类的regex属性，将正则表达式给予其赋值
    # 注意点：不能加^匹配开头
    regex = "1[3-9]\d{9}$"

# 3.将自定义的转换器类注册到默认的转换器字典中
app.url_map.converters["mobile"] = PhoneConverter

@app.route('/mobile/<mobile:phone>')
def helloworld(phone):
    return "hello world {}".format(phone)


# 3.运行Flask项目
if __name__ == '__main__':
    # debug=True 开启调试模式
    # 1.定位bug  2.修改代码[保存]自动重启服务
    # control + p 参数提示快捷键
    # host 指定ip地址
    # port 指定端口号
    app.run(host="0.0.0.0", port=8000, debug=True)
