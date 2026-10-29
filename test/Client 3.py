from socket import *
import time
# 确定客户端传输协议（服务端和客户端服务协议一样才能进行有效的通信）
client = socket(AF_INET, SOCK_STREAM)  # 这里的SOCK_STREAM代表的就是流式协议TCP，如果是SOCK_DGRAM就代表UDP协议
# 开始连接服务端IP和PORT,建立双向链接
client.connect(('127.0.0.1', 8888))  # 通过服务端IP和PORT进行连接
#返回连接套接字的远程地址，类型通常是元组 (ipaddr,port)
print(client.getpeername())
# 返回套接字自己的地址，通常是一个元组 (ipaddr,port)
print(client.getsockname())
# 走到这一步就已经建立连接完毕，接下来开始数据通信：
while True:
    client.send('hello，python'.encode('utf-8'))    # 将发送的信息转码成Bytes类型数据
    data = client.recv(1024)  # 每次最大收数据大小为1024字节（1kb）
    print('客户端接收响应数据：' + data.decode('utf-8')) # 将b类型数据转换成字符串格式
    time.sleep(1)
    # 一次传输完毕
client.close()    # 关闭客户端连接
