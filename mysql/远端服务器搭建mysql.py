# Windows的mysql的搭建
# https://www.cnblogs.com/zhaoweixsj/p/16872784.html

# 腾讯云服务器的搭建（centos 7）
# 1.mysql的搭建
# （首先进入管理员）
# su,之后输入机器的密码

# 安装mysql的版本(centos)
# https://blog.csdn.net/Mortal3306/article/details/137372484

# 删除版本
# https://blog.51cto.com/u_16213408/8973730

# rm -rf /var/log/mysqld.log

# 查看mysql版本
# mysql -V
# 启动mysql服务
# service mysqld start
# 查看服务状态
# service mysqld status
# 获取临时密码
# grep “password” /var/log/mysqld.log
# 若进不去mysql
# vim /etc/my.cnf
# 输入skip-grant-tables

# 查看用户
# select host, user from user;
# DELETE FROM user WHERE user = 'root' AND host = '%';
# update user set host='%' where user='root';
# 让最后的root的权限调整为%


# 进入mysql
# 更改密码
# SHOW VARIABLES LIKE 'validate_password%';
# set global validate_password_policy=0;
# set global validate_password_length=1;
# set global validate_password_mixed_case_count=2;
# 然后刷新
# flush privileges;
# alter user 'root'@'localhost' identified by '满足策略的密码';
# 退出
# exit;

# 高版本不能用(8.0及以上)因为创建用户和授权分开了
# create user '用户名'@'%' identified by '密码';
# 开启远程所有IP访问
# grant all privileges on *.* to '用户名'@'%';
# 然后刷新
# flush privileges;
# 退出
# exit;

# 查看防火墙信息
# systemctl status firewalld(看到显示dead，说明没开。)
# 开启防火墙
# systemctl start firewalld
# mysql端口
# firewall-cmd --zone=public --add-port=3306/tcp --permanent
# tomcat端口
# firewall-cmd --zone=public --add-port=8080/tcp --permanent
# 防火墙配置生效
# firewall-cmd --reload
# 查看端口的开放设置
# firewall-cmd --zone=public --list-ports

# 配置文件进行修改
# vim /ect/my.cnf
# [client]
# default-character-set=utf8
#
# character-set-server=utf8
# collation-server=utf8_general_ci

# 最大的坑点：需要在服务器上的防火墙手动开启端口的访问
# 查看端口的使用情况
# netstat -an | grep 3306

# 刷新访问
# service mysqld restart
#开启访问
# service mysqld start
# 查看状态
# service mysqld status