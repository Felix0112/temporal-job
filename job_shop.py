from socket import *


def main():
    
    s = socket()
    try:
        s.connect(('0.0.0.0',1111))
    except Exception as e:
        print(e)
        return

    #进入一级界面
    while True:

        print("=======================登录注册================")
        print("|1.商家注册 2.商家登录 3.学生注册 4.学生登录 5.退出|")
        print("==============================================")
        cmd = input("请输入选项")
        if cmd not in ['1','2','3','4','5']:
            print("请输入正确选项")
            sys.stdin.flush()#清除标志输入
            continue
        elif cmd == '1':
            do_shopregister(s)#商家注册
        elif cmd == '2':
            pass
        elif cmd == '3':
            pass
        elif cmd == '4':
            pass
        elif cmd == '5':
            return

def do_shopregister(s):
    while True:
        name = input("merchant:")
        passwd = getpass.getpass('passwd')
        passwd1 = getpass.getpass('again:')
        mer_num = input("请输入身份证号")
        
        if (' ' in name) or (' ' in passwd):
            print('用户名或密码不能有空格')
            continue
        if passwd != passwd1:
            print("两次密码不一致")
            continue
        msg = "R %s %s %s"%(name,passwd,mer_num)
        #发送请求
        s.send(msg.encode())
        #等待回复
        data = s.recv(128).decode()
        if data == 'OK':
            print("注册成功")
        
        elif data == "EXISTS":
            print("用户存在")

        elif data == "身份证验证失败":
            print("身份证号验证失败")
        else:
            print("注册失败")
        return




main()