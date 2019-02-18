from socket import *
import getpass
import sys
import time


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
            do_shoplogin(s)#商家登录
        elif cmd == '3':
            do_sturegister(s)#学生注册
        elif cmd == '4':
            do_stulogin(s)#学生登录
        elif cmd == '5':
            return
#商家注册
def do_shopregister(s):
    while True:
        name = input("输入商家名称:")
        passwd = getpass.getpass('输入密码:')
        passwd1 = getpass.getpass('再次输入:')
        mer_id = input("请输入身份证号:")
        
        if (' ' in name) or (' ' in passwd):
            print('用户名或密码不能有空格')
            continue
        if passwd != passwd1:
            print("两次密码不一致")
            continue
        msg = "R %s %s %s"%(name,passwd,mer_id)
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

#学生注册
def do_sturegister(s):
    while True:
        stu_name = input("输入学生名称:")
        passwd = getpass.getpass('输入密码:')
        passwd1 = getpass.getpass('再次输入:')
        stu_id = input("请输入身份证号:")
        stu_tel = input("请输入手机号码：")
        if stu_name == "" or stu_tel == '':
            print("注册失败")
            return
        if (' ' in stu_name) or (' ' in passwd):
            print('用户名或密码不能有空格')
            continue
        if passwd != passwd1:
            print("两次密码不一致")
            continue
        msg = "S %s %s %s %s"%(stu_name,passwd,stu_id,stu_tel)
        #发送请求
        s.send(msg.encode())
        #等待回复
        data = s.recv(128).decode()
        if data == 'OK':
            print("注册成功")
        
        elif data == "EXISTS":
            print("用户存在")

        else:
            print("注册失败")
        return

#商家登录
def do_shoplogin(s):
    while True:
        name = input('请输入姓名：')
        passwd = getpass.getpass('请输入密码：')
        msg = "L %s %s"%(name,passwd)
        #发送请求
        s.send(msg.encode())
        #等待回复
        data = s.recv(128).decode()
        if data == "OK":
            print("登录成功")
            shoplogin(s,name)
        else:
            print(data)
        return

def shoplogin(s,name):
    while True:
        print('''
        ================================Welcome========================================
        --1.发布兼职信息 2. 查看已发布兼职信息 3.删除已完成的兼职信息 4.修改兼职为已完成或已取消 5.退出
        ===============================================================================
       ''')
        cmd = input('请输入选项：')
        if cmd not in ['1','2','3','4','5']:
            print('请输入正确选项')
            sys.stdin.flush()#清除标志输入
            continue
        
        elif cmd == '1':
            do_jobpost(s,name)#商家发布兼职信息
        elif cmd == '2':
            do_lookpost(s,name)#商家查询兼职信息
        elif cmd == '3':
            do_deletepost(s,name)#删除已完成的兼职信息
        elif cmd == '4':
            do_changestatus(s,name)#修改兼职状态为已完成或已取消
        elif cmd == '5':
            return#登录功能

#商家发布兼职信息  
def do_jobpost(s,name):
    while True:
        job_date = input('请输入工作时间（示例:2019-1-21-12:00:00）：')
        job_add = input ("请输入工作地点：")
        job_thing = input("请输入工作内容:")
        peo_no = int(input("请输入所需人数："))
        salary = float(input("请输入薪资（元）：")) 
        
        msg = "F %s %s %s %s %d %f"%(name,job_date,job_add,job_thing,peo_no,salary)
        #发送请求
        s.send(msg.encode())
        #等待回复
        data = s.recv(128).decode()
        if data == "OK":
            print("发布成功")
        else:
            print(data)
        return

#商家查询兼职信息
def do_lookpost(s,name):
    msg = 'O %s'%name
    s.send(msg.encode())
    while True: 
        try:
            data = s.recv(1024)
            if data.decode() == "##":
                return
            print(data.decode())
        except KeyboardInterrupt:
            return  

#删除已取消的兼职信息
def do_deletepost(s,name):
    while True:
        id  = int(input("请输入要删除的兼职信息的id号："))
        msg = 'D %s %d'%(name,id)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            print("删除成功")
        else:
            print(data)
        return

#修改兼职状态为已完成或已取消
def do_changestatus(s,name):
    while True:
        id  = int(input("请输输入要修改状态的兼职信息的id号："))
        cmd = input("请选择对兼职状态的操作：1.设置为已完成，2.设置为已取消")
        if cmd == '1':
            cmd = '3'
            msg = 'C %s %d %s'%(name,id,cmd)
            s.send(msg.encode())
        else:
            cmd = '4'
            msg = 'C %s %d %s'%(name,id,cmd)
            s.send(msg.encode())
        
        data = s.recv(128).decode()
        if data == "OK":
            print("操作已完成")
        else:
            print(data)
        return

#学生登录
def do_stulogin(s):
    while True:
        name = input('请输入姓名：')
        passwd = getpass.getpass('请输入密码：')
        msg = "T %s %s"%(name,passwd)
        #发送请求
        s.send(msg.encode())
        #等待回复
        data = s.recv(128).decode()
        if data == "OK":
            print("登录成功")
            stulogin(s,name)
        else:
            print(data)
        return

#
def stulogin(s,name):
    while True:
        print('''
        ===================Welcome==========================
        --1.查看已发布兼职信息 2.报名兼职及取消  3.查看自己报名的兼职 4.退出         --
        ====================================================
       ''')
        cmd = input('请输入选项：')
        if cmd not in ['1','2','3','4']:
            print('请输入正确选项')
            sys.stdin.flush()#清除标志输入
            continue
        elif cmd == '1':
            do_searchjob(s,name)#查询已发布兼职信息
        elif cmd == '2':
            do_signjob(s,name)#报名兼职及取消
        elif cmd == "3":
            do_lookstujob(s,name)#查看自己报名的兼职
        elif cmd == '4':
            return#登录功能

def do_searchjob(s,name):
    while True:
        print('''
        ==========================Welcome=======================================
        --1.查询所有报名中的工作 2.查询某个商家 3.根据工作内容查询 4.根据工资查询 5.根据工作时间查询 6.返回
        ========================================================================
        ''')
        cmd = input("请输入选项：")
        if cmd not in ['1','2','3','4','5','6']:
            print('请输入正确选项')
            sys.stdin.flush()#清除标志输入
            continue
        elif cmd == '1':
            msg = 'A %s'%cmd
            s.send(msg.encode()) 
        elif cmd == "2":
            mer_name = input("请输入商家名:")
            msg = "A %s %s"%(cmd,mer_name)
            s.send(msg.encode())
        elif cmd == "3":
            job_thing = input("请输入工作内容:")
            msg = "A %s %s"%(cmd,job_thing)
            s.send(msg.encode())
        elif cmd == "4":
            salary = float(input("请输入您的目标工资:"))
            msg = "A %s %2f"%(cmd,salary)
            s.send(msg.encode())
        elif cmd == "5":
            job_date = input("请输入工作时间（示例:2019-1-21-12:00:00）:")
            msg = "A %s %s"%(cmd,job_date)
            s.send(msg.encode())
        elif cmd == "6":
            return
        while True:
            try:
                data = s.recv(1024)
                if data.decode() == "##":
                    return
                print(data.decode())
            except KeyboardInterrupt:
                return  

#报名兼职及取消
def do_signjob(s,name):
    while True:
        print('''
        ===========Welcome===========
        --1.报名兼职   2.取消兼职     --
        =============================
        ''')
        cmd = input("请输入选项:")
        if cmd not in ['1','2']:
            print('请输入正确选项')
            sys.stdin.flush()#清除标志输入
            continue
        elif cmd == "1":
            id = int(input("请输入兼职id号:"))
            msg = "I %s %s %d"%(cmd,name,id)
            s.send(msg.encode())
        elif cmd == "2":
            id = int(input("请输入兼职id号:"))
            msg = "I %s %s %d"%(cmd,name,id)
            s.send(msg.encode())
        data = s.recv(128).decode()
        if data == "OK":
            print("操作成功")
        else:
            print(data)
        return

#查看报名的兼职
def do_lookstujob(s,name):
    msg = "K %s"%name
    s.send(msg.encode())
    while True:
        try:
            data = s.recv(1024)
            if data.decode() == "##":
                return
            print(data.decode())
        except KeyboardInterrupt:
            return

  






main()