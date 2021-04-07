## mysql修改用户密码

```sql
update mysql.user set authentication_string=password('123qwe') where user='root' and Host = 'localhost'
```

注意有的时候还是无法使用密码登入mysql操作系统中，这个时候还需要处理user中的plugin参数，让这个参数变成mysql_native_password

```sql
update mysql.user set plugin = 'mysql_native_password' where user='root'
```
mysql 8.0 使用alter user 'root'@'localhost' identified by '设置的新密码' 修改密码

生效和刷新

```sql
flush privileges;
```
