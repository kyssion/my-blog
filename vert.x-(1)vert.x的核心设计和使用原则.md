### vert.x 的核心功能

- 编写 TCP 客户端和服务端
- 编写支持 WebSocket 的 HTTP 客户端和服务端
- 事件总线(Event Bus)
- 共享数据 —— 本地的Map和分布式集群Map
- 周期性、延迟性动作
- 部署和撤销 Verticle 实例
- 数据报套接字
- DNS客户端
- 文件系统访问
- 高可用性
- 集群

### vert.x 使用的三原则

#### 1. 流式

简单的说就是.x().y().z() 这种写法

```java
request.response().putHeader("Content-Type", "text/plain").write("some text").end();
```

#### 2. 回调

最核心的特性，我们没有使用函数而是使用定义函数，由框架或者编译器来决定什么时候运行

```java
vertx.setPeriodic(1000, id -> {
  // This handler will get called every second
  // 这个处理器将会每隔一秒被调用一次
  System.out.println("timer fired!");
});
```

#### 3. 非阻塞

这个是最重要的，因为vert.x 底层使用的单线程轮询的操作，如果将线程阻塞掉的话，换回导致所有的逻辑都在阻塞中

vert.x 本质上是多线程板的eventLoop 模式又叫Multi-Reactor 模式


### vert.x 运行阻塞代码

#### 第一种方法，使用vertx.executeBlocking

```java
vertx.executeBlocking(future -> {
  // 调用一些需要耗费显著执行时间返回结果的阻塞式API
  String result = someAPI.blockingMethod("hello");
  future.complete(result);
}, res -> {
  System.out.println("The result is: " + res.result());
});
```

#### 第二种方法使用WorkerExecutor

```java
WorkerExecutor executor = vertx.createSharedWorkerExecutor("my-worker-pool");
executor.executeBlocking(future -> {
  // 调用一些需要耗费显著执行时间返回结果的阻塞式API
  String result = someAPI.blockingMethod("hello");
  future.complete(result);
}, res -> {
  System.out.println("The result is: " + res.result());
});
```

这种方法相当于生成一个新的线程池让阻塞的代码在线程中运行



