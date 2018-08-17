### 创建用户:

命令:

```sql
CREATE USER 'username'@'host' IDENTIFIED BY 'password';
```
说明:username - 你将创建的用户名, host - 指定该用户在哪个主机上可以登陆,如果是本地用户可用localhost, 如果想让该用户可以从任意远程主机登陆,可以使用通配符%. password - 该用户的登陆密码,密码可以为空,如果为空则该用户可以不需要密码登陆服务器.

例子:

```sql
CREATE USER 'dog'@'localhost' IDENTIFIED BY 'password';
CREATE USER 'pig'@'192.168.1.100' IDENDIFIED BY 'password';
CREATE USER 'pig'@'192.168.1.%' IDENDIFIED BY 'password';
CREATE USER 'pig'@'%' IDENTIFIED BY 'password';
CREATE USER 'pig'@'%' IDENTIFIED BY '';
CREATE USER 'pig'@'%';
```

### 授权:

命令:

```sql
GRANT privileges ON databasename.tablename TO 'username'@'host'
```

说明: privileges - 用户的操作权限,如SELECT , INSERT , UPDATE 等(详细列表见该文最后面).如果要授予所的权限则使用ALL.;databasename - 数据库名,tablename-表名,如果要授予该用户对所有数据库和表的相应操作权限则可用*表示, 如*.*.

例子:

```sql
GRANT SELECT, INSERT ON test.user TO 'pig'@'%';
GRANT ALL ON *.* TO 'pig'@'%';
```

> 注意:用以上命令授权的用户不能给其它用户授权,如果想让该用户可以授权,用以下命令:          
```sql
GRANT privileges ON databasename.tablename TO 'username'@'host' WITH GRANT OPTION;
```

权限信息用user、db、host、tables_priv和columns_priv表被存储在MySQL数据库中(即在名为mysql的数据库中)。

权限|列|Context
---|---|---
select|Select_priv|表
insert|Insert_priv|表
update|Update_priv|表
delete|Delete_priv|表
index|Index_priv|表
alter|Alter_priv|表
create|Create_priv|数据库、表或索引
drop|Drop_priv|数据库或表
grant|Grant_priv|数据库或表
references|References_priv|数据库或表
reload|Reload_priv|服务器管理\
shutdown|Shutdown_priv|服务器管理
process|Process_priv|服务器管理
file|File_priv|在服务器上的文件存取

### 设置与更改用户密码

命令:

```sql
SET PASSWORD FOR 'username'@'host' = PASSWORD('newpassword');如果是当前登陆用户用SET PASSWORD = PASSWORD("newpassword");
```
例子:

```sql
SET PASSWORD FOR 'pig'@'%' = PASSWORD("123456");
```

### 撤销用户权限

命令:

```sql
REVOKE privilege ON databasename.tablename FROM 'username'@'host';
```

说明: privilege, databasename, tablename - 同授权部分.
例子: REVOKE SELECT ON *.* FROM 'pig'@'%';
注意: 假如你在给用户'pig'@'%'授权的时候是这样的(或类似的):GRANT SELECT ON test.user TO 'pig'@'%', 则在使用REVOKE SELECT ON *.* FROM 'pig'@'%';命令并不能撤销该用户对test数据库中user表的SELECT 操作.相反,如果授权使用的是GRANT SELECT ON *.* TO 'pig'@'%';则REVOKE SELECT ON test.user FROM 'pig'@'%';命令也不能撤销该用户对test数据库中user表的Select 权限.

具体信息可以用命令SHOW GRANTS FOR 'pig'@'%'; 查看.

### 删除用户

命令:

```sql
DROP USER 'username'@'host';
```

查看用户的授权 

```sql
mysql> show grants for 'test01'@'localhost';
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Grants for test01@localhost                                                  |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'test01'@'localhost'                                              |
| GRANT INSERT, UPDATE, DELETE, CREATE, DROP, REFERENCES, INDEX, ALTER, CREATE TEMPORARY TABLES, LOCK TABLES, EXECUTE, CREATE VIEW, SHOW VIEW, CREATE ROUTINE, ALTER ROUTINE, EVENT, TRIGGER ON `test001`.* TO 'test01'@'localhost' |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
2 rows in set (0.01 sec)
mysql> show grants for 'test02'@'localhost'; 
+-------------------------------------------------------------+
| Grants for test02@localhost         |
+-------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'test02'@'localhost'     |
| GRANT ALL PRIVILEGES ON `test001`.* TO 'test02'@'localhost' |
+-------------------------------------------------------------+
2 rows in set (0.00 sec)
```

以上所述是小编给大家介绍的mysql5.7创建用户授权删除用户撤销授权，希望对大家有所帮助，如果大家有任何疑问请给我留言，小编会及时回复大家的。在此也非常感谢大家对脚本之家网站的支持！