create table merchant(
    id int primary key auto_increment,
    mer_name varchar(32) not null,
    mer_pass varchar(16) not null default '000000',
    mer_id varchar(32) not null 
)default charset=utf8;    

create table jobs(
    id int primary key auto_increment,
    mer_name varchar(32) not null,
    post_date date,
    job_date text not null,
    job_add varchar(32) not null,
    job_thing text not null,
    peo_no int not null,
    re_no int not null default 0,
    salary decimal(8,2) not null,
    status enum('1','2','3','4') default 1
)default charset=utf8;

create table student(
    id int primary key auto_increment,
    stu_name varchar(32) not null,
    stu_pass varchar(16) default '000000',
    stu_id varchar(32) not null,
    stu_tel varchar(16) not null
)default charset=utf8;

create table stujob(
    stu_name varchar(32) not null,
    id int
)default charset=utf8;
