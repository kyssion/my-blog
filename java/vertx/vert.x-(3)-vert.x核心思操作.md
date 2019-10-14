vert.x 其实在本质上并不单单是一个网络框架，更多的是封装了一层的函数式或者异步回掉的框架

vert.x 在使用的时候要求使用者尽量不使用阻塞的方法，支持非阻塞的方法，这些其实就是vert.x最初的设计哲学

### 一个基本列子，展示vert.x 的非阻塞操作

```java
Vertx vertx = Vertx.vertx();
vertx.setPeriodic(1000, i->{
    System.out.println("the i is "+i);
});
```

这个例子是一个定时执行任务的例子，后面的lamble表达式就是回调函数，之前表示执行的时间间隔，这个函数将会在1000毫秒后执行

### vert.x 运行阻塞代码

vert.x 提供两种方法来运行阻塞的代码

#### 1. 使用executeBlocking 方法来实现阻塞调用

```java
vertx.executeBlocking(function->{
    String hhh = "sdfsdf";
    try {
        Thread.sleep(2000);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    function.complete(hhh);
}，false,(res)->{
    System.out.println(res.result());
});
```

注意默认情况下，如果 executeBlocking 在同一个上下文环境中（如：同一个 Verticle 实例）被调用了多次，那么这些不同的 executeBlocking 代码块会 顺序执行（一个接一个）。

若您不需要关心您调用 executeBlocking 的顺序，可以将 ordered 参数(函数中的第二个参数)的值设为 false。这样任何 executeBlocking 都会在 Worker Pool 中并行执行。

#### 使用 Worker Verticle 实现阻塞代码

一个 Worker Verticle 始终会使用 Worker Pool 中的某个线程来执行。

默认的阻塞式代码会在 Vert.x 的 Worker Pool 中执行，通过 setWorkerPoolSize 配置。

可以为不同的用途创建不同的池：

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

Worker Executor 在不需要的时候必须被关闭：

```java
executor.close();
```

当使用同一个名字创建了许多 worker 时，它们将共享同一个 pool。当所有的 worker executor 调用了 close 方法被关闭过后，对应的 worker pool 会被销毁。

如果 Worker Executor 在 Verticle 中创建，那么 Verticle 实例销毁的同时 Vert.x 将会自动关闭这个 Worker Executor。

Worker Executor 可以在创建的时候配置：

```java
int poolSize = 10;
// 2分钟
long maxExecuteTime = 120000;
WorkerExecutor executor = vertx.createSharedWorkerExecutor("my-worker-pool", poolSize, maxExecuteTime);
```