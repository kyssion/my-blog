### http状态碼

> 2xx表示成功

- 200：OK 表示服务器正常处理
- 206：表示客户端进行了范围请求，服务返回行了范围请求

> 3xx重定向

- 301：永久重定向，表示uri已经分配了新的地址，以后使用这个uri访问资源
- 302：临时重定向，表示只是暂时的分配了新的地址，本次请求使用新的地址
- 303：临时重定向，和302区别时要求客户端使用get方法进行请求
- 304:为满足条件，表示服务器可以进行请求，但是没有满足head中的（if-×）类型字段的条件

> 4xx表示客户端错误

- 400：语法错误
- 401：需要进行验证
- 403：访问被拒绝
- 404：服务器上无法找到被请求的资源

> 5xx服务器错误

- 500：服务器故障
- 503：服务器超负荷，或停机维护，服务器返回Retry-after表示需要的时间

### http协议首部字段的书写格式

![](/blogimg/http2/1.png)

### http协议通用首部字段

![](/blogimg/http2/2.png)

#### cache-Control

**格式**

```java
Cache-Control: private,max-age=0,no-cache
```

**作用：**操作缓存机制

> 缓存请求指令

![](/blogimg/http2/3.png)

![](/blogimg/http2/4.png)

> 缓存响应指令

![](/blogimg/http2/5.png)

####  connection

控制代理表明相关的字段不被转发 和管理持久链接

```java
Connection:不被转发的字段名称
```

> 关闭持久链接

```java
connection:close
```

> 开启持久链接

```java
connection:keep-alive
```

####  data

> 创建时间的报文

```java
Date:Sun, 08 Oct 2017 11:30:41 GMT
```

> Trailer

首部字段Trailer会事先说明报文主体后记录了那些首部字段。该首部字段可应用在HTTP/1.1版本分块传输编码时。

```java
Transfer-Encoding:chunk
Trailer:Expires
 
cf0   <---16进制 10进制3312
-----3312-字节-----
0 <----表示结束
Expires：Thu，15 Apr  2010  20：00：00  GMT;
```

#### Transfer-Encoding:chunk

> http1.1中表示分块请求

```java
Transfer-Encoding:chunk
Trailer:Expires
cf0   <---16进制 10进制3312
-----3312-字节-----
392
----914字节-----
0 <----表示结束
Expires：Thu，15 Apr  2010  20：00：00  GMT;
```

#### upgrade

表明是否支持更加高级的协议

![](/blogimg/http2/6.png)

#### via

> 一般和trace连用用来追踪服务器信息

![](/blogimg/http2/7.png)

### http协议请求首部字段

![](/blogimg/http2/8.png)

#### Accept等

```java
Accept:image/webp,image/apng,image/*,*/*;q=0.8
Accept-Encoding:gzip, deflate, br
Accept-Language:zh-CN,zh;q=0.8
Accept-Charset:UTF-8;q=0.8,iso-8859-5
```

#### authorization和proxy-authrization

认证相关：401等

#### form

使用代理的时候告诉电子邮箱的地址

```java
form: 1409915687@qq.com
```

#### if-xxx

if-match：比对match参数和文件的ETag值 相同返回200 否则412

![](/blogimg/http2/9.png)

if-Modified-Since:表示返回文件的最后更新底线，如果文件的实际更新时间在字段时间之前则失败反之成功  （if-unmodifed-since 和这个作用相反）
![](/blogimg/http2/10.png)
if-no-match:和if-mathch 作用相反，不匹配的时候返回成功
![](/blogimg/http2/11.png)
if-Range：如果该字段的ETag值或者时间相同就允许做范围资源请求
![](/blogimg/http2/12.png)

#### Max-forwards

指定转发的次数

![](/blogimg/http2/13.png)

#### Range

范围返回

```java
Range：bytes：100-2000
```

#### TE

指定传输编码的方式– 可以使用trailers指定的相关字段

```java
TE:trailers
```

#### User-Agent

用户的浏览器相关的信息

```java
User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36
```

### http协议响应首部字段

![](/blogimg/http2/14.png)

![](/blogimg/http2/15.png)

#### ETag

资源的唯一标识符，当使用不同的语言环境的时候可能会出现相同的uri地址但是指向的却是不同的资源，这就使用ETag进一步标识所要使用的资源

![](/blogimg/http2/16.png)

#### location

配合3xx 表示重定向的地址

#### Retry-after

指定多久呵在进行相应，配合503

#### server

表示服务器信息

```java
server：nginx/1.12.0
```

#### Vary

![](/blogimg/http2/17.png)

### http协议实体首部字段

![](/blogimg/http2/18.png)

#### allow

指定服务器指定的uri请求方法GET等

```java
Allow：GET,POST
```

#### Content-*

实体部分的编码

```java
Content-Encode：gzip
Content-Language：zh-CN
Content-Length:15000
Content-Location:www.hi-kys.me
Content-MD5:UEUEJDJNWIQSNNFIFNEF=
Content-Range:bytes:500-1000/1000
Content-Type:text/html;charset=UTF-8
```

#### Expires

指定资源失效的日期，优先级小于Cache-Control：max-age

```java
Expires：Thu，15 Apr 2010 20：00：00 GMT;
```

#### last-Modified

返回文件最终修改日期

```java
Last-Modified：Thu，15 Apr  2010  20：00：00  GMT
```

### 其他非http/1.1首部

#### cookie和setcookie

cookie相应格式

```java
Set-Cookie:sid=123[;name=value....];status=enable;expires=Thu ' 15 Apr 2019 20:00:00  GMT;path=/;domain=.hackr.com
```

相关字段属性

![](/blogimg/http2/19.png)

![](/blogimg/http2/20.png)

- Domain：域，表示当前cookie所属于哪个域或子域下面。
- Path：表示cookie的所属路径。
- Expire time/Max-age：表示了cookie的有效期。expire的值，是一个时间，过了这个时间，该cookie就失效了。或者是用max-age指定当前cookie是在多长时间之后而失效。如果服务器返回的一个cookie，没有指定其expire time，那么表明此cookie有效期只是当前的session，即是session cookie，当前session会话结束后，就过期了。对应的，当关闭（浏览器中）该页面的时候，此cookie就应该被浏览器所删除了。
- secure：表示该cookie只能用https传输。一般用于包含认证信息的cookie，要求传输此cookie的时候，必须用https传输。
- httponly：表示此cookie必须用于http或https传输。这意味着，浏览器脚本，比如javascript中，是不允许访问操作此cookie的。


从客户端发送cookie给服务器的时候，是不发送cookie的各个属性的，而只是发送对应的名称和值。

```java
Cookie：sid=123[;name=value....]
```

### http首部基于缓存代理和非缓存代理行为的分类

1. 端到端首部 : 转换过程中不能丢失，必须转发的首部
2. 逐跳首部 : http1.1需要提供connection字段，经过一层代理之后可以不进行转发

