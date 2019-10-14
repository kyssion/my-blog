## postgresql学习记录（一）

### 一.初探postgresql

PostgreSQL是一个功能强大的开源对象关系数据库管理系统(ORDBMS)。 用于安全地存储数据; 支持最佳做法，并允许在处理请求时检索它们。PostgreSQL(也称为Post-gress-Q-L)由PostgreSQL全球开发集团(全球志愿者团队)开发。 它不受任何公司或其他私人实体控制。 它是开源的，其源代码是免费提供的。

### 二.踩坑postgresql的安装
单纯的安装postgresql是非常容易的打开官网按照教程就可以很容易的安装上去

1. 在 /etc/apt/sources.list.d/pgdg.list 文件中添加如下的语句
注意要选择适合自己系统的版本,具体要求看postgresql的官方网站

``` 
deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main
```

2. 运行命令开始安装
```
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \sudo apt-key add -
sudo apt-get update
```

``` 
sudo apt-get install postgresql-9.6
```

### 三.为postgresql添加新的用户并且开启远程登入的权限
postgresql和mysql有一些差别,要想开启远程登入权限需要修改两个文件

1. 输入 vi postgresql.conf 修改pistgresql.conf文件

``` 
vi postgresql.conf
```

![](blogimg/postgresql/4.png)

编辑其中的listen_addresses 字段 将原来的listen_addresses = ‘localhost’修改为listen_addresses = ‘*’

``` 
vi pg_hba.conf
```

![](blogimg/postgresql/5.png)

修改整个文件变成如上的样子:说明一下,local 表示本地登入的权限使用peer认证(本机使用unix socket认证:注意在这种模式下,linux系统必须切换到相应的用户中才行,这样就不需要使用密码进行登入了),host外网使用的是md5认证(增加安全权限)具体为什么要看一下其他的东西:http://hi-kys.me/?p=361

2. 针对安全性为postgresql添加一个新的用户
在上面的过程中我们已将使用了peer认证方法声明了所有的用户,也就是说只要linux系统中拥有和postgresql相同名称的用户,那么将linux切换到这个用户中将可以不使用密码进行登入数据的操作
第一次使用postgresql首先切换linux用户

```
su postgresql
```

直接登入到数据库中

``` 
psql
```

以上两步可以使用一个命令解决

```
sudo -u postgres psql
```

![](blogimg/postgresql/6.png)

创建新的用户并设置密码

``` 
CREATE USER dbuser WITH PASSWORD '*****';
```

或者使用这个命令

```
CREATE ROLE name LOGIN PASSWORD '123456‘;
```

引申:user和role的区别就是role没有登入权限而user拥有登入权限
创建一个数据库并关联到当前的用户上

```
create database xxx owner username
```

付给这个新用户全部的权限(这里只是做开发不考虑进行权限管理)

```
grant ALL on DATABASE database_name TO user_name
```

使用\du命令查看一下 \q退出

![](/blogimg/postgresql/7.png)

3. 测试一下
使用命令

``` 
psql -U user_name -d database_name -h xxx.xxx.xxx.xxx -p5432
```

- 或者使用图形工具进行连接登入成功证明配置正确
