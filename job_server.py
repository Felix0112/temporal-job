from socket import *
import os,sys
import pymysql
import signal
import time
from db_conf import *

#定义一些全局变量
Host = '0.0.0.0'
Port = 1111
Addr = (Host,Port)

#网络连接
def main():
    #创建数据库连接
    db = pymysql.connect(host,user,password,dbname)
    #创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(Addr)
    s.listen(5)
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            c,addr = s.accept()
            print("connect form ",addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue

        #创建子进程
        pid = os.fork()
        if pid ==0:
            s.close()
            do_child(c,db)
            sys.exit(0)
        else:
            c.close()

def do_child(c,db):
    while True:
        data = c.recv(128).decode()
        print(c.getpeername(),':',data)
        if (not data) or data[0] == 'E':
            c.close()
            sys.exit()
        elif data[0] == "R":#商家注册
            do_shopregister(c,db,data)