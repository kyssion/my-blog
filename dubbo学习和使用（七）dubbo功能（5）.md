##配置规则

向注册中心写入动态配置覆盖规则。该功能通常由监控中心或治理中心的页面完成。

```java
RegistryFactory registryFactory = ExtensionLoader.getExtensionLoader(RegistryFactory.class).getAdaptiveExtension();
Registry registry = registryFactory.getRegistry(URL.valueOf("zookeeper://10.20.153.10:2181"));
registry.register(URL.valueOf("override://0.0.0.0/com.foo.BarService?category=configurators&dynamic=false&application=foo&timeout=1000"));
```

其中：

- override:// 表示数据采用覆盖方式，支持 override 和 absent，可扩展，必填。
- 0.0.0.0 表示对所有 IP 地址生效，如果只想覆盖某个 IP 的数据，请填入具体 IP，必填。
- com.foo.BarService 表示只对指定服务生效，必填。
- category=configurators 表示该数据为动态配置类型，必填。
- dynamic=false 表示该数据为持久数据，当注册方退出时，数据依然保存在注册中心，必填。
- enabled=true 覆盖规则是否生效，可不填，缺省生效。
- application=foo 表示只对指定应用生效，可不填，表示对所有应用生效。
- timeout=1000 表示将满足以上条件的 timeout 参数的值覆盖为 1000。如果想覆盖其它参数，直接加在 override 的 URL 参数上。

> 示例：

> 禁用提供者：(通常用于临时踢除某台提供者机器，相似的，禁止消费者访问请使用路由规则)

```
override://10.20.153.10/com.foo.BarService?category=configurators&dynamic=false&disbaled=true
```

> 调整权重：(通常用于容量评估，缺省权重为 100)

```
 override://10.20.153.10/com.foo.BarService?category=configurators&dynamic=false&weight=200
```

> 调整负载均衡策略：(缺省负载均衡策略为 random)

```
override://10.20.153.10/com.foo.BarService?category=configurators&dynamic=false&loadbalance=leastactive
```

> 服务降级：(通常用于临时屏蔽某个出错的非关键服务)

```
override://0.0.0.0/com.foo.BarService?category=configurators&dynamic=false&application
```

## 服务降级
可以通过服务降级功能临时屏蔽某个出错的非关键服务，并定义降级后的返回策略。

向注册中心写入动态配置覆盖规则：

```java
RegistryFactory registryFactory = ExtensionLoader.getExtensionLoader(RegistryFactory.class).getAdaptiveExtension();
Registry registry = registryFactory.getRegistry(URL.valueOf("zookeeper://10.20.153.10:2181"));
registry.register(URL.valueOf("override://0.0.0.0/com.foo.BarService?category=configurators&dynamic=false&application=foo&mock=force:return+null"));
```

其中：

- mock=force:return+null 表示消费方对该服务的方法调用都直接返回 null 值，不发起远程调用。用来屏蔽不重要服务不可用时对调用方的影响。
- 还可以改为 mock=fail:return+null 表示消费方对该服务的方法调用在失败后，再返回 null 值，不抛异常。用来容忍不重要服务不稳定时对调用方的影响。

## 优雅停机

Dubbo 是通过 JDK 的 ShutdownHook 来完成优雅停机的，所以如果用户使用 kill -9 PID 等强制关闭指令，是不会执行优雅停机的，只有通过 kill PID 时，才会执行。

**原理**

> 服务提供方

停止时，先标记为不接收新请求，新请求过来时直接报错，让客户端重试其它机器。
然后，检测线程池中的线程是否正在运行，如果有，等待所有线程执行完成，除非超时，则强制关闭。

> 服务消费方

停止时，不再发起新的调用请求，所有新的调用在客户端即报错。
然后，检测有没有请求的响应还没有返回，等待响应返回，除非超时，则强制关闭。

> 设置方式

设置优雅停机超时时间，缺省超时时间是 10 秒，如果超时则强制关闭。

# dubbo.properties

```properties
dubbo.service.shutdown.wait=15000
```
如果 ShutdownHook 不能生效，可以自行调用，使用tomcat等容器部署的場景，建议通过扩展

ContextListener等自行调用以下代码实现优雅停机：
```java
ProtocolConfig.destroyAll();
```

## 日志适配
自 2.2.1 开始，dubbo 开始内置 log4j、slf4j、jcl、jdk 这些日志框架的适配，也可以通过以下方式显示配置日志输出策略：

> 命令行

```properties
java -Ddubbo.application.logger=log4j
```

0. 在 `dubbo.properties` 中指定

```properties
dubbo.application.logger=log4j
```

在 dubbo.xml 中配置

```xml
<dubbo:application logger="log4j" />
```

## 开启访问日志
如果你想记录每一次请求信息，可开启访问日志，类似于apache的访问日志。注意：此日志量比较大，请注意磁盘容量。

将访问日志输出到当前应用的log4j日志：

```xml
<dubbo:protocol accesslog="true" />
```
将访问日志输出到指定文件：

```xml
<dubbo:protocol accesslog="http://10.20.160.198/wiki/display/dubbo/foo/bar.log" />
```

## 服务容器

服务容器是一个 standalone 的启动程序，因为后台服务不需要 Tomcat 或 JBoss 等 Web 容器的功能，如果硬要用 Web 容器去加载服务提供方，增加复杂性，也浪费资源。

服务容器只是一个简单的 Main 方法，并加载一个简单的 Spring 容器，用于暴露服务。

服务容器的加载内容可以扩展，内置了 spring, jetty, log4j 等加载，可通过容器扩展点进行扩展。配置配在 java 命令的 -D 参数或者 dubbo.properties 中。

> 容器类型

Spring Container

自动加载 META-INF/spring 目录下的所有 Spring 配置。

配置 spring 配置加载位置：

dubbo.spring.config=classpath*:META-INF/spring/*.xml

### Jetty Container

* 启动一个内嵌 Jetty，用于汇报状态。
* 配置：
    * `dubbo.jetty.port=8080`：配置 jetty 启动端口
    * `dubbo.jetty.directory=/foo/bar`：配置可通过 jetty 直接访问的目录，用于存放静态文件
    * `dubbo.jetty.page=log,status,system`：配置显示的页面，缺省加载所有页面


### Log4j Container

* 自动配置 log4j 的配置，在多进程启动时，自动给日志文件按进程分目录。
* 配置：
    * `dubbo.log4j.file=/foo/bar.log`：配置日志文件路径
    * `dubbo.log4j.level=WARN`：配置日志级别
    * `dubbo.log4j.subdirectory=20880`：配置日志子目录，用于多进程启动，避免冲突

## 容器启动

缺省只加载 spring

```sh
java com.alibaba.dubbo.container.Main
通过 main 函数参数传入要加载的容器

java com.alibaba.dubbo.container.Main spring jetty log4j
通过 JVM 启动参数传入要加载的容器

java com.alibaba.dubbo.container.Main -Ddubbo.container=spring,jetty,log4j
通过 classpath 下的 dubbo.properties 配置传入要加载的容器

dubbo.container=spring,jetty,log4j
```

## ReferenceConfig 缓存

ReferenceConfig 实例很重，封装了与注册中心的连接以及与提供者的连接，需要缓存。否则重复生成 ReferenceConfig 可能造成性能问题并且会有内存和连接泄漏。在 API 方式编程时，容易忽略此问题。

因此，自 2.4.0 版本开始， dubbo 提供了简单的工具类 ReferenceConfigCache用于缓存 ReferenceConfig 实例。

使用方式如下：

```java
ReferenceConfig<XxxService> reference = new ReferenceConfig<XxxService>();
reference.setInterface(XxxService.class);
reference.setVersion("1.0.0");
......
ReferenceConfigCache cache = ReferenceConfigCache.getCache();
// cache.get方法中会缓存 Reference对象，并且调用ReferenceConfig.get方法启动ReferenceConfig
XxxService xxxService = cache.get(reference);
// 注意！ Cache会持有ReferenceConfig，不要在外部再调用ReferenceConfig的destroy方法，导致Cache内的ReferenceConfig失效！
// 使用xxxService对象
xxxService.sayHello();
```
消除 Cache 中的 ReferenceConfig，将销毁 ReferenceConfig 并释放对应的资源。

```java
ReferenceConfigCache cache = ReferenceConfigCache.getCache();
cache.destroy(reference);
```

缺省 ReferenceConfigCache 把相同服务 Group、接口、版本的 ReferenceConfig 认为是相同，缓存一份。即以服务 Group、接口、版本为缓存的 Key。

可以修改这个策略，在 ReferenceConfigCache.getCache 时，传一个 KeyGenerator。详见 ReferenceConfigCache 类的方法。

```java
KeyGenerator keyGenerator = new ...
ReferenceConfigCache cache = ReferenceConfigCache.getCache(keyGenerator );
```

## 现场dump

当业务线程池满时，我们需要知道线程都在等待哪些资源、条件，以找到系统的瓶颈点或异常点。dubbo通过Jstack自动导出线程堆栈来保留现场，方便排查问题

默认策略:

导出路径，user.home标识的用户主目录
导出间隔，最短间隔允许每隔10分钟导出一次
指定导出路径：

```properties
dubbo.application.dump.directory=/tmp
```
```xml
<dubbo:application ...>
    <dubbo:parameter key="dump.directory" value="/tmp" />
</dubbo:application>
```