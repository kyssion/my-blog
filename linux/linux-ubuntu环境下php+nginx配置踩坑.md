> nginx安装方法—进入官网

查看官方教程就好了http://nginx.org/en/linux_packages.html#stable

> php安装 使用ppa方法进行相关的安装
```shell
add-apt-repository ppa:ondrej/php
apt-get update
```
> 接下来按照相关的规定进行安装就好哦
nginx 配置  打开/etc/nginx/ 目录下的配置文件修改如下
```
server {
    listen       80;
    server_name  localhost;
 
    #charset koi8-r;
    #access_log  /var/log/nginx/log/host.access.log  main;
 
    location / {
        #指定静态文件的目录
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
 
    #error_page  404              /404.html;
 
    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
 
    # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #
    #location ~ \.php$ {
    #    proxy_pass   http://127.0.0.1;
    #}
 
    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    location ~ \.php$ {
        root           /home/kys/myphp;
        fastcgi_pass   127.0.0.1:4444;
        fastcgi_index  index.php;
        #指定脚本文件的目录
        fastcgi_param  SCRIPT_FILENAME  /home/kys/myphp$fastcgi_script_name;
        include        fastcgi_params;
    }
 
    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}
```
修改php-fpm 相关配置如下 添加如下字段
```shell
listen = 127.0.0.1:4444
```
开启php调试模式 修改fpm cli等php.ini中的如下字段
```shell
display_errors = On
display_startup_errors = On
```