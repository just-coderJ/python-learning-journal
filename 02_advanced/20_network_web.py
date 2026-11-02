"""
=========================================================
📚 模块: 20 网络与 Web 开发
💡 核心对比：
1. Socket：TCP 三次握手与 HTTP 报文拼接（类似 Java Socket 编程）。
2. WSGI：Python Web 服务器与应用的统一接口规范（对应 Java Servlet 规范）。
=========================================================
"""
import socket
from wsgiref.simple_server import make_server

print("--- 1. TCP Socket 发送 HTTP 请求 ---")
# 任务 1：用 socket.socket(AF_INET, SOCK_STREAM) 连接 www.sina.com.cn:80。
# 任务 2：手动发送 GET / HTTP/1.1 请求头，接收响应并按 \r\n\r\n 分离 Header 与 HTML 内容。

host = "www.baidu.com"
port = 80
request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

try:
    # 1. 创建 TCP Socket (AF_INET 表示 IPv4, SOCK_STREAM 表示 TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)

    # 2. 连接服务器
    s.connect((host, port))

    s.send(request.encode('utf-8'))

    # 3. 接收数据：因为网页数据通常很大，需要循环接收
    response_data = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        response_data += chunk
    s.close()

    # 4.分离Header和HTML内容
    # HTTP协议中，Header和Body之间用 \r\n\r\n 分隔
    header_data, html_data = response_data.split(b"\r\n\r\n", 1)

    print("[响应头 Header]:")
    # 解码并打印前 200 个字符，免得刷屏
    print(header_data.decode('utf-8', errors='ignore')[:200] + "\n...")

    print("【网页内容 HTML】(前 100 个字符):")
    print(html_data.decode('utf-8', errors='ignore')[:100])

except Exception as e:
    print(f"Socket 请求失败: {e}")


print("\n--- 2. 定义 WSGI 接口 ---")
# 任务 3：实现 application(environ, start_response)，根据 PATH_INFO 返回不同 HTML。
# 任务 4：用 wsgiref.simple_server 监听 8000 端口运行该应用。

def application(environ, start_response):
    # 获取请求的路径
    path = environ.get('PATH_INFO', '/')

    if path == '/':
        # 如果访问根路径，返回 200 OK
        status = '200 OK'
        headers = [('Content-Type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        # WSGI 规范要求返回一个可迭代对象（通常是列表），里面装 bytes 数据
        return [
            b"<h1>Hello, WSGI! \xe6\xac\xa2\xe8\xbf\x8e\xe6\x9d\xa5\xe5\x88\xb0 Python \xe7\x9a\x84\xe4\xb8\x96\xe7\x95\x8c!</h1>"]
    else:
        # 其他路径，返回 404 Not Found
        status = '404 Not Found'
        headers = [('Content-Type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return [b"<h1>404 Not Found - \xe9\xa1\xb5\xe9\x9d\xa2\xe6\x89\xbe\xe4\xb8\x8d\xe5\x88\xb0</h1>"]


if __name__ == '__main__':
    print("正在启动 WSGI 服务器，监听 8000 端口...")
    print("请在浏览器中访问: http://localhost:8000")
    print("（注意：服务器会一直运行，需要点击控制台的红色 Stop 按钮才能停止）")

    # 创建服务器，绑定 0.0.0.0（允许外部访问）和 8000 端口
    httpd = make_server('0.0.0.0', 8080, application)
    # 开始监听请求（这会阻塞当前进程）
    httpd.serve_forever()

# 总结:
# socket.AF_INET