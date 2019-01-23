### Vertx类


### WorkerExecutor类

### Future类 和 CompositeFuture 类

vert.x 支持并发合并操作，实现的方法就是使用上面的两个类

一个例子

```java
Future<HttpServer> httpServerFuture = Future.future();
httpServer.listen(httpServerFuture.completer());
Future<NetServer> netServerFuture = Future.future();
netServer.listen(netServerFuture.completer());
CompositeFuture.all(httpServerFuture, netServerFuture).setHandler(ar -> {
    if (ar.succeeded()) {
        // 所有服务器启动完成
    } else {
        // 有一个服务器启动失败
    }
});
```

CompsiteFuture 方法监听传入的Future类的状态，可以传入一个list列表或者最多留个Future参数

CompsiteFuture 提供的整理方法

- any : 只要有一个成功，传入下一个handle中的状态就是成功
- all : 必须全部成功，传入下一个handle中的状态才能是成功
- join : 所有的future 都执行完成了没有一场无论结果是否失败，传入到下一个handle中的状态就是成功





