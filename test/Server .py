import threading
import socket
import time


numDict = {}
num = 0
def func(cnn):
    global numDict
    global num

    while True:

        try:
            request = cnn.recv(1024)
            if len(request) == 0:
                cnn.close()
                break
            print(
                '%s接收到来自客户端%s的信息，信息内容为：%s' % (time.strftime("%D %H:%M:%S"), cnn.getpeername(), request.decode('utf-8')))
            if request.decode('utf-8') == "连接":
                a = str(num)
                client = {cnn.getpeername()[1]: a}
                numDict = dict()
                numDict.update(client)
                num = num + 1
                print('编号为 ' + numDict.get(cnn.getpeername()[1]) + ' 灯柱已连接')

            if request.decode('utf-8') == "报警":
                print('收到编号为 ' + numDict.get(cnn.getpeername()[1]) + '灯柱的报警请求！')
                cnn.send(b'%s' % "已联系附近公安！".encode('utf-8'))




        except ConnectionResetError:
            pass


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 8888))
    s.listen(5)
    print("服务器已启动...")

    while True:
        cnn, addr = s.accept()
        th = threading.Thread(target=func, args=(cnn,), daemon=True)
        th.start()
