from django.shortcuts import render
from django.http import HttpResponse
"""
 django.http模块中定义了HttpResponse 对象的API
 作用：不需要调用模板直接返回数据
 HttpResponse属性：
    content: 返回内容,字符串类型
    charset: 响应的编码字符集
    status_code: HTTP响应的状态码
"""

"""
hello 为一个视图函数，每个视图函数必须第一个参数为request。哪怕用不到request。
request是django.http.HttpRequest的一个实例
"""
def hello(request):
    return HttpResponse('Hello World')

"""
request	HttpRequest实例	是	包含用户请求信息的实例
template_name	str	是	模板的名称（可以带路径）
context	dict	否	向模板传递的上下文变量（可以为空）
content_type	str	否	返回的响应类型（MIME type），默认情况下为’text/html’
status	int	否	HTTP响应状态码，默认为200
using	str	否	使用的Django数据库别名（当使用多个数据库时）
"""
def test(request):
    context = {"msg":"测试视图传递给模板"}
    return render(request, "index.html", context=context)
