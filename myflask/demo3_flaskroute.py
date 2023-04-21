from flask import Flask

app = Flask(__name__)


# 路由必须是/开头
# methods=["get", "POST"] 指定请求方式 可以忽略大小写
# 请求方式错误：405
@app.route('/index', methods=["get", "POST"])
def hello_world():
    return 'Hello World!'

"""
Map(
        路由地址      允许的请求方式               视图函数名称
[<Rule '/index' (GET, OPTIONS, HEAD, POST) -> hello_world>,
        访问静态文件的路由                        flask底层已经实现了访问静态文件的视图函数
 <Rule '/static/<filename>' (GET, OPTIONS, HEAD) -> static>])

"""

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True, port=8000)
