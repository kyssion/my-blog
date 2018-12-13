## mysql数据库开启远程登入权限

注释掉在/etc/mysql/mysql.conf.d/mysqld.cnf（使用apt安装后的配置文件）里面的bind-address = 127.0.0.1s

```shell
kys@kys-CW23S ~ $ xed /etc/mysql/mysql.conf.d/mysqld.cnf 
```

登入的mysql数据库，给需要的用户添加权限

```shell
mysql -uroot -p
use mysql;
Grant all on *.* to 'root'@'%' identified by 'root用户的密码' with grant option;
#给root用户添加%（表示所有的url地址都能进行访问）
flush privileges;#刷新
```