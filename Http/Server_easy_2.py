import socket
from threading import Thread


def request_handler(new_client_socket, ip_port):
    """接收信息，并且做出响应"""

    # 接收客户端浏览器发送的请求协议
    request_data = new_client_socket.recv(1024)  # 接收请求报文
    print(request_data)

    # 判断协议是否为空
    if not request_data:
        print("%s客户端已下线！" % str(ip_port))
        new_client_socket.close()
    else:
        # 响应行
        response_line = "HTTP/1.1 200 OK\r\n"

        # 响应头
        response_header = "Server:Python20WS/2.1\r\n"

        # 响应空行
        response_blank = "\r\n"

        # 响应主体
        # 返回字符串内容
        # response_body = "Hello World"

        # 返回固定页面
        with open(r"E:\xcl\xcl_master\Html\test.html", "rb") as file:
            response_body = file.read()

        # 拼接响应报文
        response_data = (response_line + response_header + response_blank).encode() + response_body

        # 发送响应报文
        new_client_socket.send((response_data))

        # 关闭连接
        new_client_socket.close()


def main():
    """主函数"""

    # 创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 设置地址重用  SOL_SOCKET表示当前套接字，SO_REUSEADDR表示设置地址重用
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    # 绑定端口
    tcp_server_socket.bind(("", 8080))

    # 设置监听，让套接字由主动变为被动接收
    tcp_server_socket.listen(128)

    while True:
        # 接收客户端连接  定义函数
        new_client_socket, ip_port = tcp_server_socket.accept()
        print("新的客户端%s已连接！" % str(ip_port))

        # 接收请求并作出响应
        t1 = Thread(target=request_handler, args=(new_client_socket, ip_port))
        t1.start()


if __name__ == '__main__':
    main()