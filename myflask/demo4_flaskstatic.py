from flask import Flask, request

# 1.创建Flask项目的应用对象
# __name__作用：当前py文件所在的目录是Flask项目目录，会在项目目录下寻找静态文件夹[图片 css]，模板文件夹[html]
# static_folder="static" 静态文件存取的文件夹名称 默认值：static
# 访问静态文件的路由规则：<Rule '/static/<filename>' (GET, OPTIONS, HEAD) -> static>
# static_url_path 静态文件路由访问前缀， 默认值：/static
# static_url_path=None :  127.0.0.1：5000/static/kobe1.png
# static_url_path='/img'  127.0.0.1：5000/img/kobe1.png
# template_folder="templates" 模板文件夹名称 默认值：templates
app = Flask(__name__, static_folder="static", static_url_path="/img")


# 2.定义视图函数，绑定路由信息
# http://127.0.0.1:5000
# 默认支持：GET HEAD OPTIONS
@app.route('/')
def helloworld():
    # flask会将返回的字符串包装成响应对象
    # a = 1/0
    return "hello world 6666"


# 3.运行Flask项目
if __name__ == '__main__':
    # debug=True 开启调试模式
    # 1.定位bug  2.修改代码[保存]自动重启服务
    # control + p 参数提示快捷键
    # host 指定ip地址
    # port 指定端口号
    app.run(host="0.0.0.0", port=5000, debug=True)
