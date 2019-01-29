
vert.x 的核心就是异步非阻塞，大量使用了流式调用，相比较netty还是非常容易使用的

之前用过undertow 现在发现vert.x 和 undertow 非常相像 , 这里对比一下二者编写一个基本服务器的时候的代码

1. vert.x

```java
public class SimpleWebServer {
    public static void main(String[] args) {
        Vertx vertx = Vertx.vertx(new VertxOptions().setWorkerPoolSize(40));
        HttpServerOptions options = new HttpServerOptions()
                .setMaxWebsocketFrameSize(1000000)
                .setLogActivity(true);
        HttpServer httpServer = vertx.createHttpServer(options);
        httpServer.requestHandler(req->{
            req.response().end("hellow world");
        });
        httpServer.listen(8888,res->{
            if (res.succeeded()){
                System.out.println("server is now listening");
            }else{
                System.out.println("faild to bind!");
            }
        });
    }
}
```

2. undertow

```java
public class HelloWorldServer {
    public static void main(final String[] args) {
        Undertow server = Undertow.builder()
                .addHttpListener(8080, "localhost")
                .setHandler(new HttpHandler() {
                    @Override
                    public void handleRequest(final HttpServerExchange exchange) throws Exception {
                        exchange.getResponseHeaders().put(Headers.CONTENT_TYPE, "text/plain");
                        exchange.getResponseSender().send("Hello World");
                    }
                }).build();
        server.start();
    }
}
```
> 流程其实非常想像 初始状态->配置参数->指定handle->运行

接下来运行这段代码然后输入指定的url地址就可以实现查看相应的结果了

```
hello world
```