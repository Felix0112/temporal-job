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
    db = pymysql.connect(host,user,password,dbname,charset="utf8")
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
        data = c.recv(1024).decode()
        print(c.getpeername(),':',data)
        if (not data) or data[0] == 'E':
            c.close()
            sys.exit()
        elif data[0] == "R":#商家注册
            do_shopregister(c,db,data)
        elif data[0] == "L":#商家登录
            do_shoplogin(c,db,data)
        elif data[0] == "F":#商家发布兼职信息
            do_shoppost(c,db,data)
        elif data[0] == "O":#商家查询兼职信息
            do_lookpost(c,db,data)
        elif data[0] == 'D':#商家删除兼职信息
            do_deletepost(c,db,data)
        elif data[0] == "C":#商家改变兼职状态
            do_changestatus(c,db,data)
        elif data[0] == "S":#学生注册
            do_sturegister(c,db,data)
        elif data[0] == "T":#学生登录
            do_stulogin(c,db,data)
        elif data[0] == "A":#学生查询兼职信息
            do_searchjob(c,db,data)
        elif data[0] == "I":#学生报名或取消报名
            do_signjob(c,db,data)
        elif data[0] == "K":#学生查看自己报名的兼职
            do_lookstujob(c,db,data)

#商家注册
def do_shopregister(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    mer_id = l[3]
    cursor = db.cursor()
    sql = '''select * from merchant where mer_name = "%s"'''%name
    cursor.execute(sql)
    r = cursor.fetchone()
    if r != None:
        c.send(b"EXISTS")
        return
    
    #插入用户
    sql = "insert into merchant(mer_name,mer_pass,mer_id)values \
        ('%s','%s','%s')"%(name,passwd,mer_id)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except Exception:
        db.rollback()
        c.send(b'Fail')

#学生注册
def do_sturegister(c,db,data):
    l = data.split(' ')
    stu_name = l[1]
    passwd = l[2]
    stu_id = l[3]
    stu_tel = l[4]
    cursor = db.cursor()
    sql = '''select * from student where stu_name = "%s" or stu_tel = "%s"'''%(stu_name,stu_tel)
    cursor.execute(sql)
    r = cursor.fetchone()
    if r != None:
        c.send(b"EXISTS")
        return
    
    #插入用户
    sql = "insert into student(stu_name,stu_pass,stu_id,stu_tel)values \
        ('%s','%s','%s','%s')"%(stu_name,passwd,stu_id,stu_tel)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except Exception:
        db.rollback()
        c.send(b'Fail')

#商家登录
def do_shoplogin(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()
    sql = "select * from merchant where mer_name = '%s' and \
    mer_pass = '%s'"%(name,passwd)
    cursor.execute(sql)
    r = cursor.fetchone()
    if r == None:
        c.send(b'Not Exisit')
    else:
        c.send(b'OK')

#商家发布兼职信息
def do_shoppost(c,db,data):
    l = data.split(' ')
    mer_name = l[1]
    job_date = l[2]
    # print(job_date)
    job_add = l[3]
    job_thing = l[4]
    peo_no = int(l[5])
    salary = float(l[6])
    # print(salary)
    cursor = db.cursor()
    sql = "insert into jobs(mer_name,post_date,job_date,job_add,job_thing,peo_no,salary)values \
        ('%s',now(),'%s','%s','%s',%d,%2f)"%(mer_name,job_date,job_add,job_thing,peo_no,salary)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except Exception as e:
        print(e)
        db.rollback()
        c.send(b"Fail")
    
#商家查询兼职信息
def do_lookpost(c,db,data):
    l = data.split(" ")
    mer_name = l[1]
    cursor = db.cursor()
    sql = "select * from jobs where mer_name = '%s'"%mer_name
    cursor.execute(sql)
    r = cursor.fetchall()
    if r == None:
        c.send('没有发布兼职信息'.encode())
    for id,mer_name,post_date,job_date,job_add,job_thing,peo_no,re_no,salary,status in r:
        msg = "id:%d,商家名称：'%s',发布时间:'%s',工作时间:'%s',工作地点:'%s',工作内容:'%s',所需人数:%d,已报人数:%d,薪资:%2f,状态：%s"%(id,mer_name,post_date,job_date,job_add,job_thing,peo_no,re_no,salary,status)
        c.send(msg.encode())
        time.sleep(0.1)
    c.send(b'##')

#商家删除兼职信息
def do_deletepost(c,db,data):
    l = data.split(" ")
    mer_name = l[1]
    id = l[2]
    cursor = db.cursor()
    sql = "delete from jobs where mer_name = '%s' and id = %d and status = '4'"%(name,id)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except Exception:
        db.rollback()
        c.send(b'Fail')

#商家修改兼职状态为已完成或已取消
def do_changestatus(c,db,data):
    l = data.split(" ")
    mer_name = l[1]
    id = int(l[2])
    status = l[3]
    cursor = db.cursor()
    sql = "update jobs set status = '%s' where id = %d and mer_name = '%s'"%(status,id,mer_name)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except Exception:
        db.rollback()
        c.send(b'Fail')

#学生登录
def do_stulogin(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()
    sql = "select * from student where stu_name = '%s' and \
    stu_pass = '%s'"%(name,passwd)
    cursor.execute(sql)
    r = cursor.fetchone()
    if r == None:
        c.send(b'Not Exisit')
    else:
        c.send(b'OK')

#学生查询工作
def do_searchjob(c,db,data):
    l = data.split(" ")
    cmd = l[1]
    cursor = db.cursor()
    if cmd == '1':
        sql = "select * from jobs where status='1'"
    elif cmd == '2':
        mer_name = l[2]
        sql = "select * from jobs where mer_name = '%s' and status = '1' "%mer_name
    elif cmd == "3":
        job_thing = l[2]
        sql = "select * from jobs where job_thing = '%s' and status='1'"%job_thing
    elif cmd == "4":
        salary = float(l[2])
        sql = "select * from jobs where salary >= %2f and status='1'"%salary
    elif cmd == "5":
        job_date = l[2]
        sql = "select * from jobs where job_date = '%s' and status='1'"%job_date
    cursor.execute(sql)
    r = cursor.fetchall()
    if r == None:
        c.send('没有查询到兼职信息或您输入有误'.encode())
        time.sleep(0.1)
    for id,mer_name,post_date,job_date,job_add,job_thing,peo_no,re_no,salary,status in r:
        msg = "id:%d,商家名称：'%s',发布时间:'%s',工作时间:'%s',工作地点:'%s',工作内容:'%s',所需人数:%d,已报人数:%d,薪资:%2f,状态：%s"%(id,mer_name,post_date,job_date,job_add,job_thing,peo_no,re_no,salary,status)
        c.send(msg.encode())
        time.sleep(0.1)
    c.send(b'##')

#学生报名或取消报名兼职
def do_signjob(c,db,data):
    l = data.split(" ")
    cmd = l[1]
    stu_name = l[2]
    id = int(l[3])
    cursor = db.cursor()
    if cmd == "1":
        sql1 = "update jobs set re_no = re_no + 1 where id = %d"%id
        sql2 = "insert into stujob(stu_name,id)values('%s',%d)"%(stu_name,id)
    elif cmd == "2":
        sql1 = "update jobs set re_no = re_no - 1 where id = %d"%id
        sql2 = "delete from stujob where stu_name='%s' and id =%d"%(stu_name,id)
    try:
        cursor.execute(sql1)
        cursor.execute(sql2)
        db.commit()
        c.send(b'OK')
        #如果报名成功,就要对工作的状态进行更新,如果报名人数满了,工作状态就改为进行中(2)
        cursor = db.cursor()
        sql3 = "select peo_no,re_no from jobs where id = %d"%id
        cursor.execute(sql3)
        r = cursor.fetchall()
        peo_no = r[0][0]
        re_no = r[0][1]
        if peo_no == re_no:
            sql4 = "update jobs set status=2 where id = %d"%id
            cursor.execute(sql4)
            db.commit()
    except Exception:
        db.rollback()
        c.send(b'Fail')

#学生查看报名的兼职
def do_lookstujob(c,db,data):
    l = data.split(" ")
    stu_name = l[1]
    cursor = db.cursor()
    sql = "select id from stujob where stu_name = '%s'"%stu_name
    cursor.execute(sql)
    r = cursor.fetchall()
    if r == None:
        c.send('没有查询到兼职信息或您输入有误'.encode())
        time.sleep(0.1)
    for id in r:
        sql = "select * from jobs where id = %d"%id
        cursor.execute(sql)
        r = cursor.fetchall()
        for id,mer_name,post_date,job_date,job_add,job_thing,peo_no,re_no,salary,status in r:
            msg = "id:%d,商家名称：'%s',发布时间:'%s',工作时间:'%s',工作地点:'%s',工作内容:'%s',所需人数:%d,已报人数:%d,薪资:%2f,状态：%s"%(id,mer_name,post_date,job_date,job_add,job_thing,peo_no,re_no,salary,status)
            c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')
        

    








main()