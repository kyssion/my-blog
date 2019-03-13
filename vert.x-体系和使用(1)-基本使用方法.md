## vert.x核心功能

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

其实vertx的最核心的东西就是异步和非阻塞

ps:除了极少数例外（即某些文件系统操作以'Sync'结尾），Vert.x中的所有API都不会阻塞调用线程。

## vert.x使用方法

1. vert.x的使用其实非常简单,使用工厂方法既可以创建一个vert实例

```java
Vertx vertx = Vertx.vertx(new VertxOptions().setWorkerPoolSize(20));
```

> ps: 我们可以使用VertxOptions方法创建一个vert配置的参数.

2. vert.x的一些基本的使用方法

```java
//在vertx中使用定时器方法创建一个基本的方法
vertx.setPeriodic(1000,id->{
    System.out.println(id);
});

//阻塞代码的使用方法
vertx.executeBlocking(future->{
    System.out.println("teste");
    future.complete("sdfsdfsdf");
},res->{
    System.out.println(res);
});
```

ps:除了极少数例外（即某些文件系统操作以'Sync'结尾），Vert.x中的所有API都不会阻塞调用线程。