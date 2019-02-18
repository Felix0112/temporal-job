from socket import *
import sys
import getpass
import time 
def main():
    #设置地址
    addr = ('127.1.1.1',1111)
    #创建套接字
    s = socket()
    try:
        s.connect(addr)
    except Exception as e:
        print(e)
        return

    #进入一级界面
    while True:
        print('''
        ==========Welcome=========
        --1.注册 2.登录  3.退出-----
        ==========================
        ''')
