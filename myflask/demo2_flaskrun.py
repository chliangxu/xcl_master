from flask import Flask


# 1.创建应用对象
app = Flask(__name__)


# 2.定义视图函数，绑定路由信息
# 127.0.0.1:5000/index
@app.route('/index')
def flaskrun():
    return "falsk run"

"""
flask新版本指的是1.x版本
flask新版本运行方式-命令【了解】

指定要运行的文件名
export FLASK_APP=文件名称
指定要运行的环境
export FLASK_ENV=development 或者 production
运行flask
flask run -h ip地址 -p 端口号
"""



if __name__ == '__main__':
    # 3.旧版运行方式
    # app.run()
    pass