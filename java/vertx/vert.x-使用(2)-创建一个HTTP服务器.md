## vert.x 简单请求处理

```java
import io.vertx.core.MultiMap;
import io.vertx.core.Vertx;
import io.vertx.core.buffer.Buffer;
import io.vertx.core.http.HttpServer;
import io.vertx.core.http.HttpServerOptions;
import java.util.Iterator;
import java.util.Map;
public class WebHttpServer {
    public static void main(String[] args) {
        Vertx vertx = Vertx.vertx();
        HttpServerOptions options = new HttpServerOptions()
                .setMaxWebsocketFrameSize(1000000)
                .setLogActivity(true);
        HttpServer server = vertx.createHttpServer(options);
        server.requestHandler(res->{
            //这将返回一个实例MultiMap- 它类似于普通的Map或Hash，但允许同一个键的多个值 - 这是因为HTTP允许多个头值具有相同的键。
            MultiMap headers = res.headers();
            showMap("header",headers.iterator());
            System.out.println("absoluteURI:"+res.absoluteURI());
            System.out.println("uri:"+res.uri());
            System.out.println("host:"+res.host());
            System.out.println("path:"+res.path());
            System.out.println("query:"+res.query());
            System.out.println("remoteAddress:"+res.remoteAddress());
            MultiMap params = res.params();
            showMap("params",params.iterator());
            System.out.println(res.getParam("param1"));//这个方法只能获取一个值
            System.out.println(params.getAll("param1"));//通过这种方法可以获取多个相同的key的值
            res.response().end("Hello world");
            //使用handle 处理正文(post大字段非url请求)
            Buffer totalBuffer = Buffer.buffer();
            //因为body可能并不是一次性获取成功,需要多次聚合
            res.handler(buffer -> {
                System.out.println("I have received a chunk of the body of length " + buffer.length());
                totalBuffer.appendBuffer(buffer);
            });
            //当整个处理都结束(数据全部读取完)的时候,将会回调这个方法
            res.endHandler((end)->{
                System.out.println("handle end");
                //最终状态的时候一定可以获取到信息,所以直接处理之前缓存的
                System.out.println("Full body received, length = " + totalBuffer.length());
                System.out.println(totalBuffer.toString());
            });
            //vert.x 针对这种情况,将上面的方法统一的实现一个事件 bodyhandle
            res.bodyHandler(buf -> {
                System.out.println("Full body received, length = " + buf.length());
            });

        });
        server.listen(8888,"localhost", res -> {
            if (res.succeeded()) {
                System.out.println("Server is now listening!");
            } else {
                System.out.println("Failed to bind!");
            }
        });
    }
    public static void showMap(String title, Iterator<Map.Entry<String,String>> iterator){
        System.out.println("-------------<"+title+">-------------");
        while (iterator.hasNext()){
            Map.Entry<String,String> item = iterator.next();
            System.out.println(item.getKey()+"  "+item.getValue());
        }
        System.out.println("----------------------------------");
    }
}
```

总结一下,这里说的简单请求处理,其实就是不包括表单提交和文件上传的处理,总结一下

1. vert.x 提供了几种回调的用法

- handle : 最基本的请求处理方法,不保证数据完整
- endHandlle : 最终状态的处理器,这个时候数据完整
- bodyHandle : 专门处理简单类型大body的请求,相当于handle和endhandle配合使用的情况
其他的回调
- loadhandle : 表单文件上下传递御用handle
- exceptionHandler : 异常御用handle



2. vert.x 提供了非常方便的参数处理方法,提供了一个特殊的Map--MultiMap,通过这个方法可以很方便的获取header,params,表单(下面会说明名)中的数据,和普通map的不同点是,MultiMap支持相同的key的情况


## vert.x 简单响应发送处理

1. 状态码设置

vert.x的 request对象可以设置setStatusCode来表示对应的状态码

```java
res.response().setStatusCode(200);
```

2. 写入相关的头部信息

vert.x 提供的很方便的消息头部调用

```java
//使用headerMap直接调用
HttpServerResponse response = request.response();
MultiMap headers = response.headers();
headers.set("content-type", "text/html");
headers.set("other-header", "wibble");
//使用response进行调用
HttpServerResponse response = request.response();
response.putHeader("content-type", "text/html").putHeader("other-header", "wibble");
```

3. vert.x 分块http响应支持

## vert.x 的表单处理方法

vert.x如果要开启表单支持需要配置一些req的相关参数(针对使用了application/x-www-form-urlencoded或multipart/form-data协议的表单)

```java
server.requestHandler(request -> {
    request.setExpectMultipart(true);//开启表单支持
    request.endHandler(v -> {
        // The body has now been fully read, so retrieve the form attributes
        MultiMap formAttributes = request.formAttributes();
    });
});
```

我们之前讨论过MultiMap是啥,这里不多说了,他将会自动的解析表单中的内容

## vert.x 的文件处理方法

1. 返回文件流

vert.x core并没有提供路径解析的方法,这一点我们需要自己手动模拟,这一段代码实现了输入文件名称返回文件流的信息

```java
public class WebHttpServer {
    public static void main(String[] args) {
        Vertx vertx = Vertx.vertx();
        HttpServerOptions options = new HttpServerOptions()
                .setMaxWebsocketFrameSize(1000000)
                .setLogActivity(true);
        HttpServer server = vertx.createHttpServer(options);
        server.requestHandler(res->{
            String url = res.path();
            res.setExpectMultipart(true);
            if(url.endsWith(".html")){
                res.endHandler(v->{
                    //文件上传超级容易,只要输入一个相对路径行了
                    res.response().sendFile(url.substring(1));
                    //TODO 这里使用substring的原因是vertx获取路径的时候,会多带一个/(比如/text.html)
                });
            }else{
                res.response().end("Hello world");
            }
            res.bodyHandler(req->{
                MultiMap multiMap = res.formAttributes();
                showMap("form",multiMap.iterator());
            });
        });
        server.listen(8888,"localhost", res -> {
            if (res.succeeded()) {
                System.out.println("Server is now listening!");
            } else {
                System.out.println("Failed to bind!");
            }
        });
    }
}
```

2. 接受文件上传请求

vert.x提供了一个时间loadhandle 专门处理文件上传操作

```java
server.requestHandler(request -> {
    request.setExpectMultipart(true);
    //vert.x提供了专门处理文件上传的handle
    request.uploadHandler(upload -> {
        //采用缓存分片,防止文件过大导致缓冲区用尽
        upload.handler(chunk -> {
            System.out.println("Received a chunk of the upload of length " + chunk.length());
        });
        //直接将上传的文件传输到指定的流中
        request.uploadHandler(uploadFile -> {
            uploadFile.streamToFileSystem("myuploads_directory/" + uploadFile.filename());
        });
    });
});
```

## vert.x 对defaule或者gzip压缩体的支持

vert.x提供一个开关来控制是否解压缩gzip方法

```java
HttpServerOptions.setDecompressionSupported(true)//开启对压缩体的支持
```

## vert.x http client客户端处理

vert.x 提供了非常方便的http请求处理函数

1. vert.x创建新的httpClient客户端

```java
Vertx vertx = Vertx.vertx();
HttpClientOptions options = new HttpClientOptions()
        .setKeepAlive(false)//keepAlive头
        .setLogActivity(true)//开启netty 网络日志
        .setDefaultHost("127.0.0.1");//设置默认host地址
HttpClient client = vertx.createHttpClient(options);
```

vert.x 通过使用这种方法,可以更加快速和便利的初始化客户端,并为他初始化指定的host post url等参数

2. vert.x发送简单无body请求

vert.x 为了方便发送简单的http请求,提供了一组方法来处理

```java
client.getNow("foo.othercompany.com", "/other-uri", response -> {
    System.out.println("Received response with status code " + response.statusCode());
});

client.headNow("/other-uri", response -> {
    System.out.println("Received response with status code " + response.statusCode());
});

client.optionsNow("/other-uri", response -> {
    System.out.println("Received response with status code " + response.statusCode());
});
```

vert.x 针对三种请求做了特殊化的处理 GET HEAD OPTIONS , 这三种方法都不会带有body参数,而是直接发出请求

方法所有参数如下,其中host port url等可以省略

```java
client.getNow(8080, "myserver.mycompany.com", "/some-uri", response -> {
  System.out.println("Received response with status code " + response.statusCode());
});
```

3.  发送一般请求

vert.x 提供了request方法用来发送一般的请求

```java
client.request(HttpMethod.GET, "some-uri", response -> {
  System.out.println("Received response with status code " + response.statusCode());
}).end();

client.request(HttpMethod.POST, "foo-uri", response -> {
  System.out.println("Received response with status code " + response.statusCode());
}).end("some-data");
```

这个就很明显了,vert.x 提供了request方法,我们可以指定httpmethod host port url 等等参数

注意最后的end和writer方法,这些方法和server中的类似,将会在body中添加相关的信息数据,并且必须使用了end才会真正的发送数据

4. http客户端拆分写法

```java
HttpClient client = vertx.createHttpClient();

HttpClientRequest request = client.post("some-uri", response -> {
  System.out.println("Received response with status code " + response.statusCode());
});

//指定头部信息
request.putHeader("content-length", "1000");
request.putHeader("content-type", "text/plain");
request.write(body);

//写数据的时候指定编码
request.write("some other data", "UTF-16");

//使用buffer
Buffer buffer = Buffer.buffer().appendDouble(12.34d).appendLong(432l);
request.write(buffer);

request.end();

//另一种方法,将头部信息使用串行写法写出来

client.post("some-uri", response -> {
  System.out.println("Received response with status code " + response.statusCode());
}).putHeader("content-length", "1000").putHeader("content-type", "text/plain").write(body).end();

// Or event more simply:
client.post("some-uri", response -> {
  System.out.println("Received response with status code " + response.statusCode());
}).putHeader("content-type", "text/plain").end(body);
```

注意点:
1. 当写入请求时，第一次调用write将导致请求标头被写入线路
2. 实际写入是异步的，可能在调用返回后的某个时间才会发生
3. 具有请求主体的非分块HTTP请求需要提供Content-Length标头。
4. 因此，如果您没有使用分块HTTP，则必须Content-Length在写入请求之前设置标头，否则将为时已晚。
5. 如果您正在调用end带有字符串或缓冲区的方法之一，则Vert.x将Content-Length在写入请求主体之前自动计算并设置标头。
6. 如果您使用HTTP分块，Content-Length则不需要标头，因此您无需预先计算大小。

## vert.x 标准头写入

1. 第一种方法,使用head的Multipmap实现

```java
MultiMap headers = request.headers();
headers.set("content-type", "application/json").set("other-header", "foo");
```

2. request 直接写入header

```java
request.putHeader("content-type", "application/json").putHeader("other-header", "foo");
```

## 分块的HTTP请求

这允许HTTP请求主体以块的形式写入，并且通常在大型请求主体流式传输到服务器时使用，服务器的大小事先不知道。

您使用HTTP将HTTP请求置于分块模式setChunked。

在chunked模式下，每次调用write都会导致新的块被写入线路。在分块模式下，无需预先设置Content-Length请求。

```java
request.setChunked(true);
// Write some chunks
for (int i = 0; i < 10; i++) {
  request.write("this-is-chunk-" + i);
}
request.end();
```

## http超时

client 或者 Client的Option可以设置Timeout超时事件

```java
req.setTimeout();
HttpClientOption.setConnectTimeout();
```

## 客户端以文件内容发送请求信息

vert.x 可以将本地文件的内容作为输出,发送出去

```java
request.setChunked(true);
Pump pump = Pump.pump(file, request);
file.endHandler(v -> request.end());
pump.start();
```

## 客户端异常处理

vert.x 提供了一个方法可以处理客户端的异常问题

```java
HttpClientRequest request = client.post("some-uri");
request.handler(response -> {
    System.out.println("Received response with status code " + response.statusCode());
});
```

## 客户端处理响应

```java
HttpClientRequest request = client.request(HttpMethod.GET,8888,"127.0.0.1","sdf");
//设置创建链接的时候使用的回调函数
request.connectionHandler(con->{
    System.out.println("connection success!");
});
//响应正文处理
request.handler(res->{
    //获取相应头信息
    MultiMap header=res.headers();
    res.handler(buf->{

    });
    //和server相同
    res.bodyHandler(buf->{

    });
    //和server相同  
    res.endHandler(buf->{

    });
});
//请求结束时候的回调
request.endHandler(vo->{

});
//异常出现的回调
request.exceptionHandler(throwable->{
   throwable.fillInStackTrace();
});

//一下三种,佛悉回调,不知道干啥,暂时不研究
request.pushHandler(req->{

});
request.continueHandler(vo->{

});
request.drainHandler(vo->{

});
```

引申一下:vert.x其实本质上还是能在client中直接编写回调函数的,提供一定的便利性,比如这样

```java
client.getNow("some-uri", response -> {

  response.bodyHandler(totalBuffer -> {
    // Now all the body has been read
    System.out.println("Total response body length is " + totalBuffer.length());
  });
});
```

## vert.x client的cookie获取

```java
List<String> cookie = res.cookies();
```

## vert.x 重定向和自定义重定向

1. vert.x默认重定向使用方法

```java
//vert.x 支持自定义最大重定向次数,值默认是16
HttpClient client = vertx.createHttpClient(
    new HttpClientOptions()
        .setMaxRedirects(32));
client.get("some-uri", response -> {
  System.out.println("Received response with status code " + response.statusCode());
}).setFollowRedirects(true).end();//注意要使用重定向必须开启setFollowRedirects==true
```

2. 自定义重定向

```java
client.redirectHandler(response -> {
    // Only follow 301 code
    if (response.statusCode() == 301 && response.getHeader("Location") != null) {
        // Compute the redirect URI
        String absoluteURI = response.request().absoluteURI();
        // Create a new ready to use request that the client will use
        return Future.succeededFuture(client.getAbs(absoluteURI));
    }
    // We don't redirect
    return null;
});
```

该政策处理原始HttpClientResponse收到并返回null 或者a Future<HttpClientRequest>。
- 当null返回，原来的响应被处理
- 返回Future时，请求将在成功完成后发送
- 返回future时，将在失败时调用请求中设置的异常处理程序