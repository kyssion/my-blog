## 简单的说明一下vert.x eventLoop的相关信息

Vert.x使用了Reactor模型，通过Event driven的方式，将Events分发到handlers中进行处理，任何event都不会阻塞Eventloop线程，这样Eventloop线程可以一直保持高速分发Events的速度。

假设在同一时间有很多HTTP请求到达服务器，Eventloop会将每一个http request分发到handler中处理，比如有10K个Requests,假设服务器想在1s内处理这些requests，那么平均算下来Eventloop必须能在0.1ms内分发完每个event，一旦Eventloop被阻塞，整个服务器吞吐量都会受到极大影响。

所以Eventloop绝对不应该被阻塞住，所有交给Eventloop去处理的event都应该是non-blocking(I/O)的方式或者CPU执行时间较短的，这样才能确保每个event得到及时的分发。

而Vert.x不仅仅实现了Reactor模型，还实现了Multi-Reactor模型，也就是说，每个Vertx instance都会有多个Eventloop，默认的设置是Eventloop数量对应CPU核心数量乘以2，在VertxOptions类中可以看到

```java
/**
 * The default number of event loop threads to be used  = 2 * number of cores on the machine
 */
public static final int DEFAULT_EVENT_LOOP_POOL_SIZE = 2 * CpuCoreSensor.availableProcessors();
```

可以通过setEventLoopPoolSize()方法改变Vertx实例拥有Eventloop的数量。

## vert使用的三大原则

### 1. 流式

简单的说就是.x().y().z() 这种写法

```java
request.response().putHeader("Content-Type", "text/plain").write("some text").end();
```

### 2. 回调

最核心的特性，我们没有使用函数而是使用定义函数，由框架或者编译器来决定什么时候运行

```java
vertx.setPeriodic(1000, id -> {
  // This handler will get called every second
  // 这个处理器将会每隔一秒被调用一次
  System.out.println("timer fired!");
});
```

### 3. 非阻塞

这个是最重要的，因为vert.x 底层使用的单线程轮询的操作，如果将线程阻塞掉的话，换回导致所有的逻辑都在阻塞中

vert.x 本质上是多线程板的eventLoop 模式又叫Multi-Reactor 模式