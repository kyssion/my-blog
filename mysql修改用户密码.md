## mysql修改用户密码

```sql
update mysql.user set authentication_string=password('123qwe') where user='root' and Host = 'localhost'
```