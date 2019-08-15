# Mysql 主从复制 replication

## mysql集群方案有replication和PXC

![](/blogimg/mysql/1.webp)

![](/blogimg/mysql/2.jpg )


replication和PXC两种方案写入数据同步比较：

- replication采用异步复制，无法保证数据的一致。
- PXC采用同步复制，事务在集群的所有节点要么同时提交，要么不提交，PXC使用的是percona，percona是mysql改进版，性能挺升很大

## MySQL Replication

主从复制（也称 AB 复制）允许将来自一个MySQL数据库服务器（主服务器）的数据复制到一个或多个MySQL数据库服务器（从服务器)

> 复制是异步的 从站不需要永久连接以接收来自主站的更新。

根据配置，您可以复制数据库中的所有数据库，所选数据库甚至选定的表。

MySQL主从复制的优点包括：

- 横向扩展解决方案 - 在多个从站之间分配负载以提高性能。在此环境中，所有写入和更新都必须在主服务器上进行。但是，读取可以在一个或多个从设备上进行。该模型可以提高写入性能（因为主设备专用于更新），同时显着提高了越来越多的从设备的读取速度。
- 数据安全性 - 因为数据被复制到从站，并且从站可以暂停复制过程，所以可以在从站上运行备份服务而不会破坏相应的主数据。
- 分析 - 可以在主服务器上创建实时数据，而信息分析可以在从服务器上进行，而不会影响主服务器的性能。
- 远程数据分发 - 您可以使用复制为远程站点创建数据的本地副本，而无需永久访问主服务器。

### mysql Replication原理

![](/blogimg/mysql/2.webp)

> 前提是作为主服务器角色的数据库服务器必须开启二进制日志

过程:

1. 主服务器上面的任何修改都会通过自己的 I/O tread(I/O 线程)保存在二进制日志 Binary log 里面。
2. 从服务器上面也启动一个 I/O thread，通过配置好的用户名和密码, 连接到主服务器上面请求读取二进制日志，然后把读取到的二进制日志写到本地的一个Realy log（中继日志）里面。
3. 从服务器上面同时开启一个 SQL thread 定时检查 Realy log(这个文件也是二进制的)，如果发现有更新立即把更新的内容在本机的数据库上面执行一遍.

------

> 注意:每个从服务器都会收到主服务器二进制日志的全部内容的副本。从服务器设备负责决定应该执行二进制日志中的哪些语句。除非另行指定，否则主从二进制日志中的所有事件都在从站上执行。如果需要，您可以将从服务器配置为仅处理一些特定数据库或表的事件。

> 重要: 您无法将主服务器配置为仅记录特定事件。

------

## 一主多从配制方法

如果一主多从的话，这时主库既要负责写又要负责为几个从库提供二进制日志。此时可以稍做调整，将二进制日志只给某一从，这一从再开启二进制日志并将自己的二进制日志再发给其它从。或者是干脆这个从不记录只负责将二进制日志转发给其它从，这样架构起来性能可能要好得多，而且数据之间的延时应该也稍微要好一些。工作原理图如下：

![](/blogimg/mysql/3.webp)

## 关于二进制日志

mysqld将数字扩展名附加到二进制日志基本名称以生成二进制日志文件名。每次服务器创建新日志文件时，该数字都会增加，从而创建一系列有序的文件。每次启动或刷新日志时，服务器都会在系列中创建一个新文件。服务器还会在当前日志大小达到max_binlog_size参数设置的大小后自动创建新的二进制日志文件 。二进制日志文件可能会比max_binlog_size使用大型事务时更大， 因为事务是以一个部分写入文件，而不是在文件之间分割。

为了跟踪已使用的二进制日志文件， mysqld还创建了一个二进制日志索引文件，其中包含所有使用的二进制日志文件的名称。默认情况下，它具有与二进制日志文件相同的基本名称，并带有扩展名'.index'。在mysqld运行时，您不应手动编辑此文件。

术语二进制日志文件通常表示包含数据库事件的单个编号文件。

术语 二进制日志  表示含编号的二进制日志文件集加上索引文件。

SUPER 权限的用户可以使用SET sql_log_bin=0语句禁用其当前环境下自己的语句的二进制日志记录

# mysql主从复制配置

##  Master-Server 配置

### 修改 my.cnf

配置 Master 以使用基于二进制日志文件位置的复制，必须启用二进制日志记录并建立唯一的服务器ID,否则则无法进行主从复制。

停止MySQL服务。

```
$ service mysql.server stop
```

开启binlog ，每台设置不同的 server-id


```
$ cat /etc/my.cnf
[mysqld]
log-bin=mysql-bin
server-id=1
```

启动MySQL服务

```
$ service mysql.server start
```

登录MySQL

```
$ /usr/local/mysql/bin/mysql -uroot -p
```

## 创建用户

每个从库使用MySQL用户名和密码连接到主库，因此主库上必须有用户帐户，从库可以连接。任何帐户都可以用于此操作，只要它已被授予 REPLICATION SLAVE权限。可以选择为每个从库创建不同的帐户，或者每个从库使用相同帐户连接到主库

虽然不必专门为复制创建帐户，但应注意，复制用到的用户名和密码会以纯文本格式存储在主信息存储库文件或表中 。因此，需要创建一个单独的帐户，该帐户只具有复制过程的权限，以尽可能减少对其他帐户的危害。

登录MySQL

```
$ /usr/local/mysql/bin/mysql -uroot -p
mysql> CREATE USER 'replication'@'192.168.252.124' IDENTIFIED BY 'mima';
mysql> GRANT REPLICATION SLAVE ON *.* TO 'replication'@'192.168.252.124';
```

## Slave-Server 配置

### 修改 my.cnf

停止MySQL服务。

```
$ service mysql.server stop
```

```
$ cat /etc/my.cnf
[mysqld]
server-id=2
```

> 如果要设置多个从库，则每个从库的server-id与主库和其他从库设置不同的唯一值。

### 启动MySQL服务

```
$ service mysql.server start
```

### 登录MySQL

```
$ /usr/local/mysql/bin/mysql -uroot -p
```

## 配置主库通信

> 查看 Master-Server ， binlog File 文件名称和 Position值位置 并且记下来

```
mysql>  show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000001 |      629 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)
```

要设置从库与主库进行通信，进行复制，使用必要的连接信息配置从库在从库上执行以下语句 

> 将选项值替换为与系统相关的实际值

> 参数格式，请勿执行

```
mysql> CHANGE MASTER TO
    ->     MASTER_HOST='master_host_name',
    ->     MASTER_USER='replication_user_name',
    ->     MASTER_PASSWORD='replication_password',
    ->     MASTER_LOG_FILE='recorded_log_file_name',
    ->     MASTER_LOG_POS=recorded_log_position;
mysql> CHANGE MASTER TO
    -> MASTER_HOST='192.168.252.123',
    -> MASTER_USER='replication',
    -> MASTER_PASSWORD='mima',
    -> MASTER_LOG_FILE='mysql-bin.000001',
    -> MASTER_LOG_POS=629;
Query OK, 0 rows affected, 2 warnings (0.02 sec)
```

MASTER_LOG_POS=0 写成0 也是可以的

放在一行执行方便

```
CHANGE MASTER TO MASTER_HOST='192.168.252.123', MASTER_USER='replication', MASTER_PASSWORD='mima', MASTER_LOG_FILE='mysql-bin.000001', MASTER_LOG_POS=629;
```

启动从服务器复制线程

```
mysql> START SLAVE;
Query OK, 0 rows affected (0.00 sec)
```

查看复制状态

```
mysql>  show slave status\G
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 192.168.252.123
                  Master_User: replication
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000001
          Read_Master_Log_Pos: 629
               Relay_Log_File: master2-relay-bin.000003
                Relay_Log_Pos: 320
        Relay_Master_Log_File: mysql-bin.000001
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
......
```

检查主从复制通信状态

```
Slave_IO_State #从站的当前状态 
Slave_IO_Running： Yes #读取主程序二进制日志的I/O线程是否正在运行 
Slave_SQL_Running： Yes #执行读取主服务器中二进制日志事件的SQL线程是否正在运行。与I/O线程一样 
Seconds_Behind_Master #是否为0，0就是已经同步了
```

必须都是 Yes

如果不是原因主要有以下 4 个方面：

- 1、网络不通 
- 2、密码不对 
- 3、MASTER_LOG_POS 不对 ps 
- 4、mysql 的 auto.cnf server-uuid 一样（可能你是复制的mysql）

```
$ find / -name 'auto.cnf'
$ cat /var/lib/mysql/auto.cnf
[auto]
server-uuid=6b831bf3-8ae7-11e7-a178-000c29cb5cbc # 按照这个16进制格式，修改server-uuid，重启mysql即可
```

# 测试主从复制

启动MySQL服务

```
$ service mysql.server start
```

登录MySQL

```
$ /usr/local/mysql/bin/mysql -uroot -p
```

在 Master-Server 创建测试库

```
mysql> CREATE DATABASE `replication_wwww.ymq.io`;
mysql> use `replication_wwww.ymq.io`;
mysql> CREATE TABLE `sync_test` (`id` int(11) NOT NULL AUTO_INCREMENT, `name` varchar(255) NOT NULL, PRIMARY KEY (`id`) ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
```

在 Slave-Server 查看是否同步过来

```
mysql> show databases;
+-------------------------+
| Database                |
+-------------------------+
| information_schema      |
| mysql                   |
| performance_schema      |
| replication_wwww.ymq.io |
| sys                     |
+-------------------------+

mysql> use replication_wwww.ymq.io
mysql> show tables;

+-----------------------------------+
| Tables_in_replication_wwww.ymq.io |
+-----------------------------------+
| sync_test                         |
+-----------------------------------+
1 row in set (0.00 sec)
```

一些命令

查看主服务器的运行状态

```
mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000001 |     1190 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
```

查看从服务器主机列表

```
mysql> show slave hosts;
+-----------+------+------+-----------+--------------------------------------+
| Server_id | Host | Port | Master_id | Slave_UUID                           |
+-----------+------+------+-----------+--------------------------------------+
|         2 |      | 3306 |         1 | 6b831bf2-8ae7-11e7-a178-000c29cb5cbc |
+-----------+------+------+-----------+--------------------------------------+
```

获取binlog文件列表

```
mysql> show binary logs;
+------------------+-----------+
| Log_name         | File_size |
+------------------+-----------+
| mysql-bin.000001 |      1190 |
+------------------+-----------+
```

只查看第一个binlog文件的内容

```
mysql> mysql> show binlog events;
+------------------+-----+----------------+-----------+-------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Log_name         | Pos | Event_type     | Server_id | End_log_pos | Info                                                                                                                                                                                                  |
+------------------+-----+----------------+-----------+-------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| mysql-bin.000001 |   4 | Format_desc    |         1 |         123 | Server ver: 5.7.19-log, Binlog ver: 4                                                                                                                                                                 |
| mysql-bin.000001 | 123 | Previous_gtids |         1 |         154 |                                                                                                                                                                                                       |
| mysql-bin.000001 | 420 | Anonymous_Gtid |         1 |         485 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                                                                                                                                                                  |
| mysql-bin.000001 | 485 | Query          |         1 |         629 | GRANT REPLICATION SLAVE ON *.* TO 'replication'@'192.168.252.124'                                                                                                                                     |
| mysql-bin.000001 | 629 | Anonymous_Gtid |         1 |         694 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                                                                                                                                                                  |
| mysql-bin.000001 | 694 | Query          |         1 |         847 | CREATE DATABASE `replication_wwww.ymq.io`                                                                                                                                                             |
| mysql-bin.000001 | 847 | Anonymous_Gtid |         1 |         912 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                                                                                                                                                                  |
| mysql-bin.000001 | 912 | Query          |         1 |        1190 | use `replication_wwww.ymq.io`; CREATE TABLE `sync_test` (`id` int(11) NOT NULL AUTO_INCREMENT, `name` varchar(255) NOT NULL, PRIMARY KEY (`id`) ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 |
+------------------+-----+----------------+-----------+-------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

查看指定binlog文件的内容

```
mysql> mysql> show binlog events in 'mysql-bin.000001';
+------------------+-----+----------------+-----------+-------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Log_name         | Pos | Event_type     | Server_id | End_log_pos | Info                                                                                                                                                                                                  |
+------------------+-----+----------------+-----------+-------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| mysql-bin.000001 |   4 | Format_desc    |         1 |         123 | Server ver: 5.7.19-log, Binlog ver: 4                                                                                                                                                                 |
| mysql-bin.000001 | 123 | Previous_gtids |         1 |         154 |                                                                                                                                                                                                       |
| mysql-bin.000001 | 420 | Anonymous_Gtid |         1 |         485 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                                                                                                                                                                  |
| mysql-bin.000001 | 485 | Query          |         1 |         629 | GRANT REPLICATION SLAVE ON *.* TO 'replication'@'192.168.252.124'                                                                                                                                     |
| mysql-bin.000001 | 629 | Anonymous_Gtid |         1 |         694 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                                                                                                                                                                  |
| mysql-bin.000001 | 694 | Query          |         1 |         847 | CREATE DATABASE `replication_wwww.ymq.io`                                                                                                                                                             |
| mysql-bin.000001 | 847 | Anonymous_Gtid |         1 |         912 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                                                                                                                                                                  |
| mysql-bin.000001 | 912 | Query          |         1 |        1190 | use `replication_wwww.ymq.io`; CREATE TABLE `sync_test` (`id` int(11) NOT NULL AUTO_INCREMENT, `name` varchar(255) NOT NULL, PRIMARY KEY (`id`) ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 |
+------------------+-----+----------------+-----------+-------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

启动从库复制线程

```
mysql> START SLAVE;
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

停止从库复制线程

```
mysql> STOP SLAVE;
Query OK, 0 rows affected (0.00 sec)
```

# 复制实现细节分析

MySQL主从复制功能使用三个线程实现，一个在主服务器上，两个在从服务器上

## Binlog转储线程。

当从服务器与主服务器连接时，主服务器会创建一个线程将二进制日志内容发送到从服务器。 
该线程可以使用 语句 SHOW PROCESSLIST(下面有示例介绍) 在服务器 sql 控制台输出中标识为Binlog Dump线程。

二进制日志转储线程获取服务器上二进制日志上的锁，用于读取要发送到从服务器的每个事件。一旦事件被读取，即使在将事件发送到从服务器之前，锁会被释放。

## 从服务器I/O线程。

当在从服务器sql 控制台发出 START SLAVE语句时，从服务器将创建一个I/O线程，该线程连接到主服务器，并要求它发送记录在主服务器上的二进制更新日志。

从机I/O线程读取主服务器Binlog Dump线程发送的更新 （参考上面 Binlog转储线程 介绍），并将它们复制到自己的本地文件二进制日志中。

该线程的状态显示详情 Slave_IO_running 在输出端 使用 命令SHOW SLAVE STATUS

使用\G语句终结符,而不是分号,是为了，易读的垂直布局

这个命令在上面 查看从服务器状态 用到过

```
mysql> SHOW SLAVE STATUS\G
```

## 从服务器SQL线程。

从服务器创建一条SQL线程来读取由主服务器I/O线程写入的二级制日志，并执行其中包含的事件。

在前面的描述中，每个主/从连接有三个线程。主服务器为每个当前连接的从服务器创建一个二进制日志转储线程，每个从服务器都有自己的I/O和SQL线程。
从服务器使用两个线程将读取更新与主服务器更新事件，并将其执行为独立任务。因此，如果语句执行缓慢，则读取语句的任务不会减慢。

例如，如果从服务器开始几分钟没有运行，或者即使SQL线程远远落后，它的I/O线程也可以从主服务器建立连接时，快速获取所有二进制日志内容。

如果从服务器在SQL线程执行所有获取的语句之前停止，则I/O线程至少获取已经读取到的内容，以便将语句的安全副本存储在自己的二级制日志文件中，准备下次执行主从服务器建立连接，继续同步。

使用命令 SHOW PROCESSLIST\G 可以查看有关复制的信息

命令 SHOW FULL PROCESSLISTG

在 Master 主服务器 执行的数据示例

```
mysql>  SHOW FULL PROCESSLIST\G
*************************** 1. row ***************************
     Id: 22
   User: repl
   Host: node2:39114
     db: NULL
Command: Binlog Dump
   Time: 4435
  State: Master has sent all binlog to slave; waiting for more updates
   Info: NULL
```

Id: 22是Binlog Dump服务连接的从站的复制线程 
Host: node2:39114 是从服务，主机名 级及端口 
State: 信息表示所有更新都已同步发送到从服务器，并且主服务器正在等待更多更新发生。 
如果Binlog Dump在主服务器上看不到 线程，意味着主从复制没有配置成功; 也就是说，没有从服务器连接主服务器。

命令 SHOW PROCESSLISTG

在 Slave 从服务器 ，查看两个线程的更新状态

```
mysql> SHOW PROCESSLIST\G
*************************** 1. row ***************************
     Id: 6
   User: system user
   Host: 
     db: NULL
Command: Connect
   Time: 6810
  State: Waiting for master to send event
   Info: NULL
*************************** 2. row ***************************
     Id: 7
   User: system user
   Host: 
     db: NULL
Command: Connect
   Time: 3069
  State: Slave has read all relay log; waiting for more updates
   Info: NULL
```

Id: 6是与主服务器通信的I/O线程 
Id: 7是正在处理存储在中继日志中的更新的SQL线程

在 运行 SHOW PROCESSLIST 命令时，两个线程都空闲，等待进一步更新

如果在主服务器上在设置的超时，时间内 Binlog Dump线程没有活动，则主服务器会和从服务器断开连接。超时取决于的 服务器系统变量 值 net_write_timeout(在中止写入之前等待块写入连接的秒数，默认10秒)和 net_retry_count;(如果通信端口上的读取或写入中断，请在重试次数，默认10次) 设置 服务器系统变量

该SHOW SLAVE STATUS语句提供了有关从服务器上复制处理的附加信息。请参见 第16.1.7.1节“检查复制状态”。

# 常见主从复制问题

[官方文档常见问题](https://dev.mysql.com/doc/refman/5.7/en/faqs-replication.html)

## 描述msyql replication 机制的实现原理，如何在不停掉mysql主库的情况下，恢复数据不一致的slave的数据库节点？

MySQL的复制（replication）是一个异步的复制，从一个MySQL instace（称之为Master）复制到另一个MySQL instance（称之Slave）。实现整个复制操作主要由三个进程完成的，其中两个进程在Slave（Sql进程和IO进程），另外一个进程在Master（IO进程）上。

引用新浪某位大牛的话：mysql复制就是一句话：基于binlog的单线程异步复制过程。
MySQL Replication复制的基本过程如下：
1、Slave上面的IO进程连接上Master，并请求从指定日志文件的指定位置（或者从最开始的日志）之后的日志内容；


代码如下:
```
mysql> CHANGE MASTER TO
            ->     MASTER_HOST='master_host_name',
            ->     MASTER_USER='replication_user_name',
            ->     MASTER_PASSWORD='replication_password',
            ->     MASTER_LOG_FILE='recorded_log_file_name',
            ->     MASTER_LOG_POS=recorded_log_position;
```
2、Master接收到来自Slave的IO进程的请求后，通过负责复制的IO进程根据请求信息读取制定日志指定位置之后的日志信息，返回给Slave的IO进程。返回信息中除了日志所包含的信息之外，还包括本次返回的信息已经到Master端的bin-log文件的名称以及bin-log的位置；

3、Slave的IO进程接收到信息后，将接收到的日志内容依次添加到Slave端的relay-log文件的最末端，并将读取到的Master端的bin-log的文件名和位置记录到master-info文件中，以便在下一次读取的时候能够清楚的高速Master“我需要从某个bin-log的哪个位置开始往后的日志内容，请发给我”；

4、Slave的Sql进程检测到relay-log中新增加了内容后，会马上解析relay-log的内容成为在Master端真实执行时候的那些可执行的内容，并在自身执行

### 操作过程：
（1）登陆主服务器，查看主服务器的状态 
mysql>show master status；
找到现阶段master的数据偏移量的值。

（2）登陆从服务器，执行同步操作。
mysql>stop slave;
mysql > change master to 直接定位到这个值得位置； 这里也就相当于给slave指明了相应的位置。
mysql > start slave;

（3）从服务器上查看状态
mysql > show slave status