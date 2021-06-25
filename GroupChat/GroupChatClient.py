# -*- coding:utf-8 -*-
# 客户端

from colorama import init
import socket
import threading


def recv(sock, addr):
    sock.sendto(name.encode('utf-8'), addr)
    while True:
        data = sock.recv(1024)
        print(data.decode('utf-8'))


# 发送数据方法（scoket对象， ip+端口）
def send(sock, addr):
    while True:
        string = input()
        message = '\n\033[0;36m'+name+'\033[0m' + ' : ' + string
        data = message.encode('utf-8')
        sock.sendto(data, addr)
        if string.lower() == 'EXIT'.lower():
            break


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = (ip, 9999)
    tr = threading.Thread(target=recv, args=(s, server), daemon=True)
    ts = threading.Thread(target=send, args=(s, server))
    tr.start()
    ts.start()
    ts.join()
    s.close()


if __name__ == '__main__':
    init(autoreset=True)
    print("\033[0;36m-----欢迎来到聊天室,退出聊天室请输入'EXIT(不分大小写)'-----\033[0m")
    ip = input('\033[0;36m输入Server ip(例如：127.0.0.1):\033[0m').split()[0]
    name = input('\033[0;36m请输入你的名称:\033[0m')
    print('\033[0;36m-----------------%s------------------\033[0m' % name)
    main()