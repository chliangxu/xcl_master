# mysql的windows安装
# https://www.cnblogs.com/zhaoweixsj/p/16872784.html

# 一些常用的mysql命令
# 常见命令
# show databases; 查看所有数据库
# use 数据库名；使用该数据库库
# select database(); 查看当前数据库的名称
# create database 数据库名；创建数据库
# 1.连接数据库
# 1.1.连接自己的机器上的mysq
# mysql -u root -p
# 1.2.连接其他数据库上的mysql
# mysql -h 所连接机器的ip -u root -p

# 2.查询
# 2.1.select database(); 查看当前数据库的名称
# 2.2.use 数据库名；使用该数据库库
# 2.3.show tables; 查看该数据库中的所有表格
# 2.4.desc 表名；查看表的结构类型




# 2.4的详解

# 2.4.1
# 表结构的类型分类
# https://blog.csdn.net/Lizzy_Fly/article/details/130012796

# 2.4.2
# 约束分类

# a.根据约束的作用范围
# 列级约束：将此约束声明放在对应字段的后面
# 表级约束：在表中所有字段声明完，在所有字段的后面声明约束

# b.根据约束起的作用
# I: NOT NULL: 非空约束，规定某个字段不能为空
# 关键字；NOT NULL
# 默认。所有的类型的值都可以是NULL,包括INT,FLOAT等数据类型
# 非空约束只能出现在表对象的列上，只能某个列单独限定非空，不能组合非空
# 一个表可以很多列都分别限定了非空
# 空字符串“不等于NULL, 0也不能等于NULL"
"""
添加非空约束
ALTER TABLE test1
MODIFY salary DECIMAL(10,2) NOT NULL
删除非空约束
ALTER TABLE test1
MODIFY salary DECIMAL(10,2);
"""""

# II: UNIQUE: 唯一约束，规定某个字段在整个列表中是唯一的
# 关键字：UNIQUE
# 同一个表可以有多个唯一约束
# 唯一约束可以是某一个列的值唯一，也可以多个列组合的值唯一。
# 唯一性约束允许列值为空
# 在创建唯一约束的时候，如果不给唯一约束命名，就默认和列名相同。
# MySQL会给唯一约束的列上默认创建一个唯一索引。
"""
CREATE TABLE test2(
id INT UNIQUE, #列约束
last_name VARCHAR(15) ,
email VARCHAR(25) ,
salary DECIMAL(10,2),
#表约束
CONSTRAINT uk_test2_email UNIQUE(email)
)
"""
# 复合约束
"""
CREATE TABLE `USER`(
id INT,
name VARCHAR(15),
password varchar(25),
#表约束实现多行约束
CONSTRAINT uk_user_name_pwd UNIQUE(name,password)
);
"""
# 删除唯一约束
"""
ALTER TABLE USER
DROP INDEX uk_user_name_pwd;
"""

# III: PRIMARY KEY: 主键（非空且唯一）约束
# 关键字：primary key
# 主键约束相当于唯一约束 + 非空约束的组合， 主键约束不允许重复，也不允许出现空值
# 一个表最多只能有一个主键约束，建立主键约束可以在列级别创建，也可以在表级别上创建
# 主键约束对应着表中的一列或者多列（复合主键）
# 如果是多列组合的复合主键约束，那么这些列都不允许为空值，并且组合的值不允许重复
# 需要注意的一点是，不要修改主键字段的值。因为主键是数据记录的唯一标识，如果修改了主键的值，就有可能会破坏数据的完整性

# 添加主键约束
"""
CREATE TABLE test3(
id INT PRIMARY KEY, #列级约束
last_name VARCHAR(15),
salary DECIMAL(10,2),
email VARCHAR(25)
);
"""
"""
CREATE TABLE test4(
id INT , 
last_name VARCHAR(15),
salary DECIMAL(10,2),
email VARCHAR(25),
#表约束，没有必要取别名
CONSTRAINT pk_test5_id PRIMARY KEY(id)
);
"""
# 复合主键约束
"""
CREATE TABLE test5(
id INT , 
last_name VARCHAR(15),
salary DECIMAL(10,2),
email VARCHAR(25),
#表约束
PRIMARY KEY(id,last_name)
);
"""
# 删除主键约束(在开发中根本不会用到)
"""
ALTER TABLE test6
DROP PRIMARY KEY;
"""

# IV: AUTO_INCREMENT: 自增列
# 关键字:auto_increment
# 一个表最多只能有一个自增长列
# 当需要产生唯一标识符或顺序值时，可设置自增长
# 自增长列约束的列必须是键列（主键列，唯一键列）
# 自增约束的列的数据类型必须是整数类型
# 如果自增列指定了0和NULL，会在当前最大值的基础上自增，如果自增列手动指定了具体值，直接赋值为具体值
# 当向主键（含AUTO_INCREMENT）的字符上添加0或null时，实际上会自动的往上添加指定字段的数值
# 添加自增约束
# 开发中，一旦主键作用的字段声明有AUTO_INCREMENT,则我们在添加数据时，就不要给主键赋值了
"""
CREATE TABLE test7(
id INT PRIMARY KEY AUTO_INCREMENT, 
last_name VARCHAR(15),
salary DECIMAL(10,2),
email VARCHAR(25)
);
"""
# 删除自增约束
"""
ALTER TABLE test7
MODIFY id INT
"""

# V: DEFAULT 默认值约束
# 给某个字段/某列指定默认值，一旦设置默认值，在插入数据时，如果此字段没有显式赋值，则赋值为默认值。
# 建表时
"""
create table 表名称(
字段名 数据类型 primary key,
字段名 数据类型 unique key not null,
字段名 数据类型 unique key,
字段名 数据类型 not null default 默认值,
);
"""
# 建表后
"""
alter table 表名称 modify 字段名 数据类型 default 默认值;
#如果这个字段原来有非空约束，你还保留非空约束，那么在加默认值约束时，还得保留非空约束，否则非空约束就被删除了
#同理，在给某个字段加非空约束也一样，如果这个字段原来有默认值约束，你想保留，也要在modify语句中保留默认值约束，否则就删除了
alter table 表名称 modify 字段名 数据类型 default 默认值 not null;
"""
# 删除默认值
"""
alter table 表名称 modify 字段名 数据类型; #删除默认值约束，也不保留非空约束
alter table 表名称 modify 字段名 数据类型 not null; #删除默认值约束，保留非空约束
"""

# V: POREIGN KEY: 外键约束
# CHECK 检查约束
# https://www.jb51.net/article/276841.htm
# 添加约束/删除约束
# CREATE TABLE时添加约束
# ALTER TABLE时增加约束，删除约束
