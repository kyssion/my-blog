nginx是一个非常棒的web代理服务器， 这里记录一下nginx 使用localtion字段，来进行访问控制的处理方法

### location匹配顺序
- "="前缀指令匹配，如果匹配成功，则停止其他匹配
- 普通字符串指令匹配，顺序是从长到短，匹配成功的location如果使用^~，则停止其他匹配（正则匹配）
- 正则表达式指令匹配，按照配置文件里的顺序，成功就停止其他匹配
- 如果第三步中有匹配成功，则使用该结果，否则使用第二步结果

> 注意点

匹配的顺序是先匹配普通字符串，然后再匹配正则表达式。另外普通字符串匹配顺序是根据配置中字符长度从长到短，也就是说使用普通字符串配置的location顺序是无关紧要的，反正最后nginx会根据配置的长短来进行匹配，但是需要注意的是正则表达式按照配置文件里的顺序测试。找到第一个比配的正则表达式将停止搜索。

一般情况下，匹配成功了普通字符串location后还会进行正则表达式location匹配。有两种方法改变这种行为，其一就是使用“=”前缀，这时执行的是严格匹配，并且匹配成功后立即停止其他匹配，同时处理这个请求；另外一种就是使用“^~”前缀，如果把这个前缀用于一个常规字符串那么告诉nginx 如果路径匹配那么不测试正则表达式。

### 匹配模式及顺序

- location = /uri 　　　=开头表示精确匹配，只有完全匹配上才能生效。

- location ^~ /uri 　　^~ 开头对URL路径进行前缀匹配，并且在正则之前。

- location ~ pattern 　~开头表示区分大小写的正则匹配。

- location ~* pattern 　~*开头表示不区分大小写的正则匹配。

- location /uri 　　　　不带任何修饰符，也表示前缀匹配，但是在正则匹配之后。

- location / 　　　　　通用匹配，任何未匹配到其它location的请求都会匹配到，相当于switch中的default。 

### location中的root 和alias

nginx的location中的root和alias

```json
location /img/ {
	alias /var/www/image/;
}
```

> 若按照上述配置的话，则访问/img/目录里面的文件时，ningx会自动去/var/www/image/目录找文件

```json
location /img/ {
	root /var/www/image;
}
```

> 若按照这种配置的话，则访问/img/目录下的文件时，nginx会去/var/www/image/img/目录下找文件

### 举一个例子

如果我想把127.0.0.1/item 目录映射到 /user/share/html路径下，我只需要这么配置皆可以了

```json
server {
    listen       80;
    server_name  localhost;

    #charset koi8-r;
    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        alias   /usr/share/nginx/html;
        index  index.html index.htm;
    }
}
```