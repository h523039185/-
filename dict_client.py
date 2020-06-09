"""
dict 客户端

收集请求，发送请求，获取结果，展示
"""
from socket import *

# 服务器地址
SERVER_ADDR = ("127.0.0.1",8888)

# 单词查询
def do_query(sockfd,name):
    while True:
        word = input("Word:")
        if word == '##':
            break
        msg = "Q %s %s"%(name,word)
        sockfd.send(msg.encode())
        # 如果查到了就返回单词解释，如果没有查到则返回 Not Found
        data = sockfd.recv(4096).decode()
        print(word,":",data)

# 查询历史记录
def do_hist(sockfd,name):
    msg = "H "+name
    sockfd.send(msg.encode()) # 发送请求
    # 不能确定接收几个历史记录
    while True:
        # 每次接收一个历史记录
        data = sockfd.recv(1024).decode()
        if data == '##':
            break
        print(data) # 打印历史记录

# 二级界面方法
def login_page(sockfd,name):
    while True:
        print("=============查询界面=============")
        print(" 1.查单词    2.历史记录     3.注销")
        print("=================================")
        cmd = input("输入命令:")
        # sockfd.send(cmd.encode())
        if cmd == '1':
            do_query(sockfd,name)
        elif cmd == '2':
            do_hist(sockfd,name)
        elif cmd == '3':
            return # 回到一级界面
        else:
            print("请输入正确序号")

# 注册用户
def do_register(sockfd):
    name = input("User:")
    passwd = input("Password:")
    msg = "R %s %s"%(name,passwd)
    sockfd.send(msg.encode()) # 发送请求
    result = sockfd.recv(128).decode() # 得到反馈
    if result == 'OK':
        print("注册成功")
    else:
        print("注册失败")

# 请求登录
def do_login(sockfd):
    name = input("User:")
    passwd = input("Password:")
    msg = "L %s %s" % (name, passwd)
    sockfd.send(msg.encode())  # 发送请求
    result = sockfd.recv(128).decode()  # 得到反馈
    if result == 'OK':
        print("登录成功")
        login_page(sockfd,name)
    else:
        print("登录失败")

# 搭建服务链接
def main():
    # 创建套接字链接服务端
    sockfd = socket()
    sockfd.connect(SERVER_ADDR)

    # 一级界面
    while True:
        print("=========登录界面===========")
        print(" 1.注册    2.登录     3.退出")
        print("===========================")
        cmd = input("输入命令:")
        # sockfd.send(cmd.encode())
        if cmd == '1':
            do_register(sockfd)
        elif cmd == '2':
            do_login(sockfd)
        elif cmd == '3':
            sockfd.send(b"E") # 告知服务端退出
            return
        else:
            print("请输入正确序号")

if __name__ == '__main__':
    main()