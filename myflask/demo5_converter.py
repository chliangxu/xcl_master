from flask import Flask, request

# 1.创建Flask项目的应用对象
# __name__作用：当前py文件所在的目录是Flask项目目录，会在项目目录下寻找静态文件夹[图片 css]，模板文件夹[html]
app = Flask(__name__)


"""
flask提供的默认的转换器字典
DEFAULT_CONVERTERS = {
    "default": UnicodeConverter,
    "string": UnicodeConverter,
    "any": AnyConverter,
    "path": PathConverter,
    "int": IntegerConverter,
    "float": FloatConverter,
    "uuid": UUIDConverter,

}

flask提供的转换器类型有限，必要的时候可以自定义转换器
"""
# BaseConverter:所有转换器的基类
from werkzeug.routing import BaseConverter

# 需求：127.0.0.1:8000/user_id/666  提取路径上的参数
# 语法：<变量名称>  == <string:变量名称> == <default:变量名称>
# 细节：提取的变量名称必须和视图函数的形参名称保存一致
@app.route('/user_id/<id>')
def helloworld(id):
    print(type(id))
    return f"hello world {id}"


# 需求：127.0.0.1:8000/user_int/666  提取路径上的参数要求参数类型必须是int类型
# 完整语法：<转换器名称:变量名称>
# int转换器：<int:变量名称>
@app.route("/user_int/<int:user_id>")
def get_uesr(user_id):
    # 整型
    print(type(user_id))
    return f"get user_id {user_id}"

# 3.运行Flask项目
if __name__ == '__main__':
    # debug=True 开启调试模式
    # 1.定位bug  2.修改代码[保存]自动重启服务
    # control + p 参数提示快捷键
    # host 指定ip地址
    # port 指定端口号
    app.run(host="0.0.0.0", port=8000, debug=True)
