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

> Futuer 描述的是这个异步执行的结果状态，通过这种方法可以将下层的异步监听方法在上层反馈到

Funtuer的compose方法用于顺序组合Future 实现多个futuer 链式调用

```java

FileSystem fs = vertx.fileSystem();
Future<Void> startFuture = Future.future();

Future<Void> fut1 = Future.future();
fs.createFile("/foo", fut1.completer());

fut1.compose(v -> {
  // fut1中文件创建完成后执行
  Future<Void> fut2 = Future.future();
  fs.writeFile("/foo", Buffer.buffer(), fut2.completer());
  return fut2;
}).compose(v -> {
  // fut2文件写入完成后执行
  fs.move("/foo", "/bar", startFuture.completer());
},
// 如果任何一步失败，将startFuture标记成failed
startFuture);
```

这里例子中，有三个操作被串起来了：

1. 一个文件被创建（fut1）
2. 一些东西被写入到文件（fut2）
3. 文件被移走（startFuture）

这个方法的参数有两种的形式

1. 只有一个函数 :
2. 两个函数 : 


> CompsiteFuture 方法监听传入的Future类的状态，可以传入一个list列表或者最多留个Future参数

CompsiteFuture 提供的整理方法

- any : 只要有一个成功，传入下一个handle中的状态就是成功
- all : 必须全部成功，传入下一个handle中的状态才能是成功
- join : 所有的future 都执行完成了没有一场无论结果是否失败，传入到下一个handle中的状态就是成功

### vert.x Verticle

Vertticle是vert.x提供的一个简单便捷的、可扩展的、类似 Actor Model 的部署和并发模型机制

Verticle 是由 Vert.x 部署和运行的代码块。默认情况一个 Vert.x 实例维护了N（默认情况下N = CPU核数 x 2）个 Event Loop 线程。Verticle 实例可使用任意 Vert.x 支持的编程语言编写，而且一个简单的应用程序也可以包含多种语言编写的 Verticle。

可以将 Verticle 想成 Actor Model 中的 Actor。

一个应用程序通常是由在同一个 Vert.x 实例中同时运行的许多 Verticle 实例组合而成。不同的 Verticle 实例通过向 Event Bus 上发送消息来相互通信。


