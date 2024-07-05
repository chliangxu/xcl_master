#!/usr/bin/python

from wsgiref.simple_server import make_server
import json

#输出回复时，通过string.encode()指定输出的文字编码方式，string.encode('gb2312')、string.encode('utf-8')、string.encode('gbk')
connStr ='''
{ 
	"code" : 0, 
	"msg" : "SUCCESS 成功"
}
'''

heartbeatStr ='''
{ 
	"code" : 0, 
	"msg" : "SUCCESS 成功"
}
'''

heartbeatErrStr ='''
{ 
	"code" : -1, 
	"msg" : "FAILED 无效"
}
'''

infoGetStr ='''
{ 
	"code" : 0, 
	"msg" : "GET 成功"
}
'''

infoPostStr ='''
{ 
	"code" : 0, 
	"msg" : "POST 成功"
}
'''

errStr ='''
{ 
	"code" : -1, 
	"msg" : "not support"
}
'''

def RunServer(environ, start_response):

    #添加回复内容的HTTP头部信息，支持多个
    headers = {'Content-Type': 'application/json', 'Custom-head1': 'Custom-info1'}

    # environ 包含当前环境信息与请求信息，为字符串类型的键值对
    current_url = environ['PATH_INFO']
    current_content_type = environ['CONTENT_TYPE']
    current_content_length = environ['CONTENT_LENGTH']
    current_request_method = environ['REQUEST_METHOD']
    current_remote_address = environ['REMOTE_ADDR']
    current_encode_type = environ['PYTHONIOENCODING']        #获取当前文字编码格式，默认为UTF-8
    '''
    HTTP客户端请求的其他头部信息（Host、Connection、Accept等），对应environ内容为“HTTP_XXX”，
    例如：请求头部为"custom-header: value1",想获取custom-header的值使用如下方式：
    '''
    #current_custom_header = environ['HTTP_CUSTOM_HEADER']

    #获取 body JSON内容转换为python对象
    current_req_body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH']))
    current_req_json = json.loads(current_req_body)

    #打印请求信息
    #print("environ:", environ)
    print("REQUEST remote ip:", current_remote_address)
    print("REQUEST method:", current_request_method)
    print("REQUEST URL:", current_url)
    print("REQUEST Content-Type:", current_content_type)
    #print("REQUEST Custom-header:", current_custom_header)
    print("REQUEST body:", current_req_json)

    #根据不同URL回复不同内容
    if current_url == "/connect":
        start_response("200 OK", list(headers.items()))
        return [connStr.encode("utf-8"), ]

    elif current_url == "/keepalive":
        # 根据 body JSON内容，回复不同内容
        '''
        判断JSON请求的内容是否合法,假设请求内容如下：判断 cmd 等于 keepalive, interval 大于30
        {
            "cmd": "keepalive",
            "data":
            {
                "interval": 30
            }
        }
        '''
        if current_req_json['cmd'] == 'keepalive':
            if current_req_json['data']['interval'] >= 30:
                start_response("200 OK", list(headers.items()))
                return [heartbeatStr.encode("utf-8"), ]
            else:
                start_response("410 err", list(headers.items()))
                return [heartbeatErrStr.encode("utf-8"), ]
        else:
            start_response("410 err", list(headers.items()))
            return [heartbeatErrStr.encode("utf-8"), ]

    elif current_url == "/info":
        # 根据不同请求方法回复不同内容
        if current_request_method == 'GET':
            start_response("200 OK", list(headers.items()))
            return [infoGetStr.encode("utf-8"), ]

        elif current_request_method == 'POST':
            start_response("200 OK", list(headers.items()))
            return [infoPostStr.encode("utf-8"), ]

        else:
            start_response("404 not found", list(headers.items()))
            return [errStr.encode("utf-8"), ]

    else:
        start_response("404 not found", list(headers.items()))
        return [errStr.encode("utf-8"), ]

if __name__ == "__main__":
    #10000为HTTP服务监听端口，自行修改
    httpd = make_server('', 10000, RunServer)
    host, port = httpd.socket.getsockname()
    print('Serving running', host, 'port', port)
    httpd.serve_forever()
