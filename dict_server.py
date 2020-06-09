"""
author : Levi
email: lvze@tedu.cn

dict 服务端模型 （多进程tcp并发处理模型）
接收请求，做逻辑处理，将结果发送给客户端
"""
from socket import *
from multiprocessing import Process
from signal import *
from dict_db import Database # 数据处理模块
from time import sleep

# 全局变量
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)
db = Database(database='dict')

# 处理注册
def do_register(connfd,name,passwd):
    # 是否能够注册，由register返回的数据确定
    if db.register(name,passwd):
        connfd.send(b"OK")
    else:
        connfd.send(b"Fail")

# 处理登录
def do_login(connfd,name,passwd):
    # 是否能够登录
    if db.login(name,passwd):
        connfd.send(b"OK")
    else:
        connfd.send(b"Fail")

# 查询单词
def do_query(connfd,name,word):
    db.insert_hist(name,word) # 插入历史记录
    mean = db.query(word)  # 查询单词
    connfd.send(mean.encode()) # 将解释发送给客户端

# 历史记录
def do_hist(connfd,name):
    # data --> ((word,time),(),())
    data = db.history(name)
    for i in data:
        # i --> (word,time)
        msg = "%s  %s  %s"%(name,i[0],i[1])
        connfd.send(msg.encode())
        sleep(0.1) # 处理粘包
    connfd.send(b'##')

# 处理客户端请求
def handle(connfd):
    db.cursor() # 在每个进程中生成各自游标
    # 循环接收请求，分情况处理
    while True:
        data = connfd.recv(1024).decode()
        tmp = data.split(' ')
        if not data or tmp[0] == 'E':
            connfd.close()
            db.cur.close()
            return # 函数退出，子进程退出
        elif tmp[0] == 'R':
            # tmp --> [R name passwd]
            do_register(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'L':
            # tmp --> [L name passwd]
            do_login(connfd, tmp[1], tmp[2])
        elif tmp[0] == 'Q':
            # tmp --> [Q name word]
            do_query(connfd, tmp[1],tmp[2])
        elif tmp[0] == 'H':
            # tmp --> [H name]
            do_hist(connfd, tmp[1])

# 结构搭建，启动整个服务
def main():
    # 创建tcp套接字
    sockfd = socket()
    sockfd.bind(ADDR)
    sockfd.listen(5)

    signal(SIGCHLD, SIG_IGN)  # 交给操作系统处理僵尸进程
    print("Listen the port %d" % PORT)
    # 循环处理客户端链接
    while True:
        try:
            connfd, addr = sockfd.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            print("服务结束")
            break

        # 为客户端创建进程
        p = Process(target=handle, args=(connfd,))
        p.daemon = True  # 子进程随父进程退出
        p.start()
    db.close()
    sockfd.close()


if __name__ == '__main__':
    main()