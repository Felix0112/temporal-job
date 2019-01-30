create table merchant(
    id int primary key auto_increment,
    mer_name varchar(32) not null,
    mer_pass varchar(16) not null default '000000',
    mer_num varchar(32) not null 
)default charset=utf8;
