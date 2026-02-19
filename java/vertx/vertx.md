# Vert.x 快速入门和进阶使用

# Vert.x 快速入门

## vertx简介

- vertx 的现状和背后支持的组织
- - vertx 是 eclipse基金会的一个顶级项目,目前社区非常活跃,是在国外非常火的一个框架

- vertx的核心思想
- - Reactive : 事件驱动式编程模型 [reactive组织宣言](https://www.reactivemanifesto.org/)

- vertx生态系统完善
- - 和spring 进行对比

|    项目        |    Spring               |    Vertx                 |
|----------------|-------------------------|--------------------------|
|    核心框架    |    spring-core          |    vertx-core            |
|    Web开发     |    spring-webmvc        |    vertx-web             |
|    jdbc框架    |    spring-jdbc          |    vertx-jdbc-client     |
|    redis       |    spring-data-redis    |    vertx-redis-client    |
|    微服务      |    spring-cloud         |    vertx-hazelcast       |

## vertx核心功能点

### 1. 使用reactive模型快速构建简单web应用

vertx 构建简单 web应用分为三步
- 1. 创建并配置Vertx对象实例
- 2. 创建并配置HttpServer对象实例
- 3. 使用回调方式编写业务逻辑代码

完整示例

```java
public class VertxMain {
    private static final Logger logger = LoggerFactory.getLogger(VertxMain.class);
    public static void main(String[] args) {
        VertxOptions vertxOptions = new VertxOptions().setEventLoopPoolSize(8);
        Vertx vertx = Vertx.vertx(vertxOptions);
        HttpServerOptions httpServerOptions = new HttpServerOptions();
        HttpServer httpServer = vertx.createHttpServer(httpServerOptions);
        httpServer.requestHandler((req)->{
            req.bodyHandler((buf)->{
                String stringData = buf.toString();
                logger.info("data : {0}",stringData);
            });
            req.response().setChunked(true);
            req.response().write("hello world").end();
        }).listen(8088,(vo)->{
            if(vo.succeeded()){
                logger.info("server success !");
            }else{
                logger.info("server failed !");
            }
        });
    }
}
```

### 2. 内置微服务/分布式支持EventBus

> eventBus简介

- eventBus 官方对的定义是vertx的"神经系统",用来模糊掉系统相互调用时候的强耦合\硬编码的部分.
- eventBus 将各个逻辑模块化,并且支持不同语言编写的模块相互通信
- event bus支持发布/订阅模式，点对点模式，和请求/响应模式。

#### EventBus 使用方法

EventBus 的使用方法非常简单,只需要在上面实现的简单服务器加上几行就可以实现了

```java
public class EventBusServer {
    private static final Logger logger = LoggerFactory.getLogger(EventBusServer.class);
    public static void main(String[] args) {
        VertxOptions vertxOptions = new VertxOptions();
        Vertx vertx = Vertx.vertx(vertxOptions);
        EventBus eventBus = vertx.eventBus();
        eventBus.consumer("event_bus_1",(msg)->{
            logger. info("this is server 1 address : {0}",msg.body());
            msg.reply("this is server get the message");
        }).completionHandler((res)->{
            if(res.succeeded()){
                logger.info("comple sucess!");
            }else{
                logger.info("comple error!");
            }
        });
        HttpServerOptions httpServerOptions = new HttpServerOptions();
        HttpServer httpServer = vertx.createHttpServer(httpServerOptions);
        httpServer.requestHandler((req)->{
            req.bodyHandler((msg)->{
                DeliveryOptions options = new DeliveryOptions();
                options.addHeader("some-header", "some-value");
                eventBus.request("event_bus_1",msg.toString(),(message)->{
                    System.out.println(message.result().body());
                });
                req.response().end("hello world");
            });
        }).listen(8088,(vo)->{
            if(vo.succeeded()){
                logger.info("lisence  sucess!");
            }else{
                logger.info("lisence error!");
            }
        });
    }
}
```

#### EventBus 扩展到分布式模式

Vertx 内置了一个接口ClusterManager,通过这个接口可以自己实现 分布式逻辑

Vertx 官方提供了一个默认的ClusterManager实现 - Hazelcast

> Hazelcast 简介

Hazelcast 是由Hazelcast公司开发和维护的开源产品，可以为基于jvm环境运行的各种应用提供分布式集群和分布式缓存服务。类似golang的etcd,不过可以嵌入到java中运行可以做"服务发现治理","分布式存储"的底层依赖.

> Vertx 嵌入 Hazelcast 实现分布式非常简单,只需要在EventBus上面增加几行代码就能实现

```xml
<dependency>
    <groupId>io.vertx</groupId>
    <artifactId>vertx-hazelcast</artifactId>
    <version>version</version>
</dependency>
```

> server

```java
public class EventBusClusterServer {
    private static final Logger logger  = LoggerFactory.getLogger(EventBusClusterServer.class);
    public static void main(String[] args) {
        //创建ClusterManger对象
        ClusterManager mgr = new HazelcastClusterManager();
        //设置到Vertx启动参数中
        VertxOptions options = new VertxOptions().setClusterManager(mgr);
        Vertx.clusteredVertx(options, res -> {
            if (res.succeeded()) {
                Vertx vertx = res.result();
                EventBus eventBus = vertx.eventBus();
                eventBus.consumer("event_bus_2",(msg)->{
                    logger. info("this is server 1 address : {0}",msg.address());
            logger.info("data: {0}",msg.body());
                }).completionHandler((result)->{
                    if(result.succeeded()){
                        logger.info("comple sucess!");
                    }else{
                        logger.info("comple error!");
                    }
                });
            } else {
                // failed!
                logger.info("create cluster error!");
            }
        });
    }
}
```

> client

```java
public class EventBusClusterClient {
    private static final Logger logger  = LoggerFactory.getLogger(EventBusClusterClient.class);
    public static void main(String[] args) {
        //创建ClusterManger对象
        ClusterManager mgr = new HazelcastClusterManager();
        //设置到Vertx启动参数中
        VertxOptions options = new VertxOptions().setClusterManager(mgr);
        Vertx.clusteredVertx(options, res -> {
            if (res.succeeded()) {
                Vertx vertx = res.result();
                EventBus eventBus = vertx.eventBus();
                HttpServer httpServer = vertx.createHttpServer();
                httpServer.requestHandler((requst)->{
                    requst.bodyHandler((buf)->{
                        eventBus.send("event_bus_2",buf.toString());
                        requst.response().end("hello word");
                    });
                }).listen(8088,(vo)->{
                    if(vo.succeeded()){
                        logger.info("lisence  sucess!");
                    }else{
                        logger.info("lisence error!");
                    }
                });
            } else {
                // failed!
                logger.info("create cluster error!");
            }
        });
    }
}
```

### 3. 插件化代码组织方式

vertx支持基于Verticle接口的方式组织代码,沿用一种插件化编程的思想,最大限度的提高功能或者代码逻辑组织过程中的灵活度

> 插件化思想的历史

插件化思想最早是来源于android开发,早期的android开发因为android jvm的问题存在64K方法数魔咒-android的Dalvik vm的可执行文件规范限制了单个.dex文件最多引用的方法数是65536个。

为了解决这个问题,有人想想出了利用java热部署的能力开发插件化功能,支持插件化的app可以在运行时加载和运行class文件，这样便可以将app中一些不常用的功能模块做成插件，减小了安装包的大小和函数数量 , **并且实现了app功能的动态扩展**

> vertx 引入插件化开发同样非常简单 共需要两部

1. 构造好Verticle接口实现类
2. Vertx加载这个实现类

```java
import io.vertx.core.AbstractVerticle

public class HelloWorldHttpVerticle extends AbstractVerticle {
    @Override
    public void start() throws Exception {
        System.out.println("hello world");
    }
}

public class VertxVerticle {
    public static void main(String[] args) {
        Vertx vertx = Vertx.vertx();
        vertx.deployVerticle("test.java", (v) -> {
            if (v.succeeded()) {
                System.out.println("ok java");
            }
        });
    }
}
```

### 4. 基于jvm的多语言支持

vertx的多语言支持其实依赖于 Vertx的插件化部署和jvm的多语言支持

例子 groovy Verticle 部署

```groovy
import io.vertx.core.AbstractVerticle

class HelloWorldHttpVerticle extends AbstractVerticle {
    void start() {
        for(int a in 0..199){
            println a;
        }
    }
    void stop() {
        println("Stopping")
    }
}
public class VertxVerticle {
    public static void main(String[] args) {
        Vertx vertx = Vertx.vertx();
        vertx.deployVerticle("test.groovy", (v) -> {
            if (v.succeeded()) {
                System.out.println("ok java");
            }
        });
    }
}
```

## vertx 基础部分总结

vertx 提供了四大特性

1. 高性能 - 底层netty / 异步化编程
2. EventBus内置分布式 Hazelcast
3. Verticle插件化 高度扩展性
4. 多语言支持 依赖jvm

# vertx进阶 - 实用vertx 实现一个简单的在线函数运行平台(Faas平台)

## 一个Faas需要的东西

1. 支持函数运行
2. 分布式调用(函数及服务)
3. 多语言支持 (多种语言编写函数)

## Vertx 和Faas 需求的对比

1. 函数运行 - vertx Verticle 可以实现
2. 分布式调用 - vertx Verticle 可以内置的使用EventBus实现分布式
3. 多语言支持 - vertx 天然支持多语言

## 实现 - >

[轻量级函数运行时引擎](https://github.com/kyssion/mini_fn_engine)

