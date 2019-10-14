## 深入dubbo（三）配置参考

**配置项分为三大类**：服务发现：表示该配置项用于服务的注册与发现，目的是让消费方找到提供方。服务治理：表示该配置项用于治理服务间的关系，或为开发测试提供便利条件。性能调优：表示该配置项用于调优性能，不同的选项对性能会产生影响。

**注意**：只有 group，interface，version 是服务的匹配条件，三者决定是不是同一个服务，其它配置项均为调优和治理参数。

### 启动时检查参数 check

> 使用标签 reference consumer registry

xml配置法

```xml
<dubbo:reference interface="com.foo.BarService" check="false" />
<dubbo:consumer check="false" />
<dubbo:registry check="false" />
```

配置文件

```
dubbo.reference.com.foo.BarService.check=false
dubbo.reference.check=false
dubbo.consumer.check=false
dubbo.registry.check=false
```

Dubbo 缺省会在启动时检查依赖的服务是否可用，可以通过 check=”false” 关闭检查（有些服务不关心，或者出现了循环依赖，必须有一方先启动， 比如Spring 容器是懒加载的，或者通过 API 编程延迟引用服务）

### 集群容错配置

1. 默认Failover Cluster

失败自动切换，当出现失败，重试其它服务器 1。通常用于读操作，但重试会带来更长延迟。可通过 retries=”2″ 来设置重试次数(不含第一次)。配置如下

```xml
<dubbo:service retries="2" />
<dubbo:reference retries="2" />
 
<dubbo:reference>
    <dubbo:method name="findFoo" retries="2" />
</dubbo:reference>
```

2. Failfast Cluster

快速失败，只发起一次调用，失败立即报错。通常用于非幂等性的写操作，比如新增记录。

3. Failsafe Cluster

失败安全，出现异常时，直接忽略。通常用于写入审计日志等操作。

4. Failback Cluster

失败自动恢复，后台记录失败请求，定时重发。通常用于消息通知操作。

5. Forking Cluster

并行调用多个服务器，只要一个成功即返回。通常用于实时性要求较高的读操作，但需要浪费更多服务资源。可通过 forks=”2″ 来设置最大并行数。

6. Broadcast Cluster
广播调用所有提供者，逐个调用，任意一台报错则报错 2。通常用于通知所有提供者更新缓存或日志等本地资源信息。

7. 集群模式配置
以上六种按照以下示例在服务提供方和消费方配置集群模式

```xml
<dubbo:service cluster="failsafe" />
<dubbo:reference cluster="failsafe" />
```

### 负载均衡配置

1. Random LoadBalance随机，按权重设置随机概率。在一个截面上碰撞的概率高，但调用量越大分布越均匀，而且按概率使用权重后也比较均匀，有利于动态调整提供者权重。
2. RoundRobin LoadBalance轮循，按公约后的权重设置轮循比率。存在慢的提供者累积请求的问题，比如：第二台机器很慢，但没挂，当请求调到第二台时就卡在那，久而久之，所有请求都卡在调到第二台上。
3. LeastActive LoadBalance最少活跃调用数，相同活跃数的随机，活跃数指调用前后计数差。使慢的提供者收到更少请求，因为越慢的提供者的调用前后计数差会越大。

> ConsistentHash LoadBalance一致性 Hash，相同参数的请求总是发到同一提供者。

> 当某一台提供者挂时，原本发往该提供者的请求，基于虚拟节点，平摊到其它提供者，不会引起剧烈变动。

- 缺省只对第一个参数 Hash，如果要修改，请配置 <dubbo:parameter key=”hash.arguments” value=”0,1″ />
- 缺省用 160 份虚拟节点，如果要修改，请配置 <dubbo:parameter key=”hash.nodes” value=”320″ />

**配置方法**

**服务端服务级别**

```xml
<dubbo:service interface="..." loadbalance="roundrobin" />
```
**客户端服务级别**

```xml
<dubbo:reference interface="..." loadbalance="roundrobin" />
```

**服务端方法级别**

```xml
<dubbo:service interface="...">
    <dubbo:method name="..." loadbalance="roundrobin"/>
</dubbo:service>
```

**客户端方法级别**

```xml
<dubbo:reference interface="...">
    <dubbo:method name="..." loadbalance="roundrobin"/>
</dubbo:reference>
```

### 线程池

对于Dubbo的服务提供者，主要有两种线程池，一种是IO处理线程池，另一种是服务调用线程池。而作为IO处理线程池，由于Dubbo基于Mina、Grizzly和Netty框架做IO组件，IO线程池都是基于这些框架来配置，比如Netty中的boss和worker线程池，Dubbo选择的是“无边界”的CachedThreadPool，这意味着对所有服务请求先做到“来者不拒”，但它进一步限制了IO处理的线程数，默认是核数+1

如果事件处理的逻辑能迅速完成，并且不会发起新的 IO 请求，比如只是在内存中记个标识，则直接在 IO 线程上处理更快，如果事件处理逻辑较慢，或者需要发起新的IO请求，比如需要查询数据库，则必须派发到IO线程池中

![](blogimg/dubbo/6.jpg)

```xml
<dubbo:protocol name="dubbo" dispatcher="all" threadpool="fixed" threads="100" />
```

Dispatcher

- all 所有消息都派发到线程池，包括请求，响应，连接事件，断开事件，心跳等。
- direct 所有消息都不派发到线程池，全部在 IO 线程上直接执行。
- message 只有请求响应消息派发到线程池，其它连接断开事件，心跳等消息，直接在 IO 线程上执行。
- execution 只请求消息派发到线程池，不含响应，响应和其它连接断开事件，心跳等消息，直接在 IO 线程上执行。
- connection 在 IO 线程上，将连接断开事件放入队列，有序逐个执行，其它消息派发到线程池。

ThreadPool

- fixed 固定大小线程池，启动时建立线程，不关闭，一直持有。(缺省)
- cached 缓存线程池，空闲一分钟自动删除，需要时重建。
- limited 可伸缩线程池，但池中的线程数只会增长不会收缩。只增长不收缩的目的是为了避免收缩时突然来了大流量引起的性能问题。

### 直接链接和只订阅模式

在开发及测试环境下，经常需要绕过注册中心，只测试指定服务提供者，这时候可能需要点对点直连

点对点，可在 <dubbo:reference> 中配置 url 指向提供者，将绕过注册中心，多个地址用分号隔开

```xml
<dubbo:reference id="xxxService" interface="com.alibaba.xxx.XxxService" url="dubbo://localhost:20890" />
```

注意：为了避免复杂化线上环境，不要在线上使用这个功能，只应在测试阶段使用。

只订阅模式：一般和直连连用，解决在测试环境下注册中心共用可能导致，线上业务受到影响的问题

![](blogimg/dubbo/7.jpg)

禁用注册配置

```xml 
<dubbo:registry address="10.20.153.10:9090" register="false" />
<dubbo:registry address="10.20.153.10:9090?register=false" />
```

### 注册到指定的服务器

```xml
<dubbo:registry id="hzRegistry" address="10.20.153.10:9090" />
<dubbo:registry id="qdRegistry" address="10.20.141.150:9090" subscribe="false" />
```

### 使用多个协议和使用多个注册中心

Dubbo 允许配置多协议，在不同服务上支持不同协议或者同一服务上同时支持多种协议。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:dubbo="http://code.alibabatech.com/schema/dubbo"
       xsi:schemaLocation="http://www.springframework.org/schema/beanshttp://www.springframework.org/schema/beans/spring-beans.xsdhttp://code.alibabatech.com/schema/dubbohttp://code.alibabatech.com/schema/dubbo/dubbo.xsd">
    <dubbo:application name="world"  />
    <dubbo:registry id="registry" address="10.20.141.150:9090" username="admin" password="hello1234" />
    <!-- 多协议配置 -->
    <dubbo:protocol name="dubbo" port="20880" />
    <dubbo:protocol name="rmi" port="1099" />
    <!-- 使用dubbo协议暴露服务 -->
    <dubbo:service interface="com.alibaba.hello.api.HelloService" version="1.0.0" ref="helloService" protocol="dubbo" />
    <!-- 使用rmi协议暴露服务 -->
    <dubbo:service interface="com.alibaba.hello.api.DemoService" version="1.0.0" ref="demoService" protocol="rmi" />
    <!--使用多个协议进行配置-->
    <dubbo:service id="helloService" interface="com.alibaba.hello.api.HelloService" version="1.0.0" protocol="dubbo,hessian" />
</beans>
```

Dubbo 支持同一服务向多注册中心同时注册，或者不同服务分别注册到不同的注册中心上去，甚至可以同时引用注册在不同注册中心上的同名服务。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:dubbo="http://code.alibabatech.com/schema/dubbo"
       xsi:schemaLocation="http://www.springframework.org/schema/beanshttp://www.springframework.org/schema/beans/spring-beans.xsdhttp://code.alibabatech.com/schema/dubbohttp://code.alibabatech.com/schema/dubbo/dubbo.xsd">
    <dubbo:application name="world"  />
    <!-- 多注册中心配置 -->
    <dubbo:registry id="hangzhouRegistry" address="10.20.141.150:9090" />
    <dubbo:registry id="qingdaoRegistry" address="10.20.141.151:9010" default="false" />
    <!-- 向多个注册中心注册 -->
    <dubbo:service interface="com.alibaba.hello.api.HelloService" version="1.0.0" ref="helloService" registry="hangzhouRegistry,qingdaoRegistry" />
    <!--使用不同的注册中心-->
    <!-- 向中文站注册中心注册 -->
    <dubbo:service interface="com.alibaba.hello.api.HelloService" version="1.0.0" ref="helloService" registry="chinaRegistry" />
    <!-- 向国际站注册中心注册 -->
    <dubbo:service interface="com.alibaba.hello.api.DemoService" version="1.0.0" ref="demoService" registry="intlRegistry" />
</beans>
```

同时链接到多个不同的注册中心    service 省略 registry属性将自动的使用默认配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:dubbo="http://code.alibabatech.com/schema/dubbo"
       xsi:schemaLocation="http://www.springframework.org/schema/beanshttp://www.springframework.org/schema/beans/spring-beans.xsdhttp://code.alibabatech.com/schema/dubbohttp://code.alibabatech.com/schema/dubbo/dubbo.xsd">
    <dubbo:application name="world"  />
    <!-- 多注册中心配置，竖号分隔表示同时连接多个不同注册中心，同一注册中心的多个集群地址用逗号分隔 -->
    <dubbo:registry address="10.20.141.150:9090|10.20.154.177:9010" />
    <!-- 引用服务 -->
    <dubbo:reference id="helloService" interface="com.alibaba.hello.api.HelloService" version="1.0.0" />
</beans>
```

### 分组聚合

按组合并返回结果 ，比如菜单服务，接口一样，但有多种实现，用group区分，现在消费方需从每种group中调用一次返回结果，合并结果返回，这样就可以实现聚合菜单项。

```xml
<!--合并指定的分组-->
<dubbo:reference interface="com.xxx.MenuService" group="*" merger="true" />
<dubbo:reference interface="com.xxx.MenuService" group="aaa,bbb" merger="true" />
<!--指定方法的结果进行整合-->
<dubbo:reference interface="com.xxx.MenuService" group="*">
    <dubbo:method name="getMenuItems" merger="true" />
</dubbo:service>
<!--指定某一个方法不进行整合-->
<dubbo:reference interface="com.xxx.MenuService" group="*" merger="true">
    <dubbo:method name="getMenuItems" merger="false" />
</dubbo:service>
```

注意：dubbo只有默认的四种组合，list set map array ，所以返回的结果值必须要是以上几种类型

### 结果缓存

结果缓存 ，用于加速热门数据的访问速度，Dubbo 提供声明式缓存，以减少用户加缓存的工作量 2。

```xml
<dubbo:reference interface="com.foo.BarService" cache="lru" />
<dubbo:reference interface="com.foo.BarService">
    <dubbo:method name="findBar" cache="lru" />
</dubbo:reference>
```

### 回声测试

回声测试用于检测服务是否可用，回声测试按照正常请求流程执行，能够测试整个调用是否通畅，可用于监控。

所有服务自动实现 EchoService 接口，只需将任意服务引用强制转型为 EchoService，即可使用。

```xml
<dubbo:reference id="memberService" interface="com.xxx.MemberService" />
```
 
 ```java
// 远程服务引用
MemberService memberService = ctx.getBean("memberService"); 
EchoService echoService = (EchoService) memberService; // 强制转型为EchoService
// 回声测试可用性
String status = echoService.$echo("OK"); 
assert(status.equals("OK"));
```

### 上下文信息获取和从客户端向服务端传递参数

上下文中存放的是当前调用过程中所需的环境信息。所有配置信息都将转换为 URL 的参数

RpcContext 是一个 ThreadLocal 的临时状态记录器，当接收到 RPC 请求，或发起 RPC 请求时，RpcContext 的状态都会变化。比如：A 调 B，B 再调 C，则 B 机器上，在 B 调 C 之前，RpcContext 记录的是 A 调 B 的信息，在 B 调 C 之后，RpcContext 记录的是 B 调 C 的信息。

> 对于服务的消费方，注意只有在使用rpc调用之后才状态会发生改变

```java
// 远程调用
xxxService.xxx();
// 本端是否为消费端，这里会返回true
boolean isConsumerSide = RpcContext.getContext().isConsumerSide();
// 获取最后一次调用的提供方IP地址
String serverIP = RpcContext.getContext().getRemoteHost();
// 获取当前服务配置信息，所有配置信息都将转换为URL的参数
String application = RpcContext.getContext().getUrl().getParameter("application");
// 注意：每发起RPC调用，上下文状态会变化
yyyService.yyy();
```

> 服务提供方，注意只有在服务类中进行注册才能坚挺到数据

```java
public class XxxServiceImpl implements XxxService {
 
    public void xxx() {
        // 本端是否为提供端，这里会返回true
        boolean isProviderSide = RpcContext.getContext().isProviderSide();
        // 获取调用方IP地址
        String clientIP = RpcContext.getContext().getRemoteHost();
        // 获取当前服务配置信息，所有配置信息都将转换为URL的参数
        String application = RpcContext.getContext().getUrl().getParameter("application");
        // 注意：每发起RPC调用，上下文状态会变化
        yyyService.yyy();
        // 此时本端变成消费端，这里会返回false
        boolean isProviderSide = RpcContext.getContext().isProviderSide();
    } 
}
```

### 参数传递流程图

![](blogimg/dubbo/6.png)

> 在服务消费方端设置隐式参数

```java
RpcContext.getContext().setAttachment("index", "1"); // 隐式传参，后面的远程调用都会隐式将这些参数发送到服务器端，类似cookie，用于框架集成，不建议常规业务使用
xxxService.xxx(); // 远程调用
```

> 在服务提供方端获取隐式参数

```java
public class XxxServiceImpl implements XxxService {
 
    public void xxx() {
        // 获取客户端隐式传入的参数，用于框架集成，不建议常规业务使用
        String index = RpcContext.getContext().getAttachment("index"); 
    }
}
```

### 异步调用

![](blogimg/dubbo/8.jpg)

**注意**:要在客户端进行配置

```xml
<dubbo:reference id="fooService" interface="com.alibaba.foo.FooService">
      <dubbo:method name="findFoo" async="true" />
</dubbo:reference>
<dubbo:reference id="barService" interface="com.alibaba.bar.BarService">
      <dubbo:method name="findBar" async="true" />
</dubbo:reference>
```

调用代码

```java
// 此调用会立即返回null
fooService.findFoo(fooId);
// 拿到调用的Future引用，当结果返回后，会被通知和设置到此Future
Future<Foo> fooFuture = RpcContext.getContext().getFuture(); 
// 此调用会立即返回null
barService.findBar(barId);
// 拿到调用的Future引用，当结果返回后，会被通知和设置到此Future
Future<Bar> barFuture = RpcContext.getContext().getFuture(); 
// 此时findFoo和findBar的请求同时在执行，客户端不需要启动多线程来支持并行，而是借助NIO的非阻塞完成
// 如果foo已返回，直接拿到返回值，否则线程wait住，等待foo返回后，线程会被notify唤醒
Foo foo = fooFuture.get(); 
// 同理等待bar返回
Bar bar = barFuture.get(); 
// 如果foo需要5秒返回，bar需要6秒返回，实际只需等6秒，即可获取到foo和bar，进行接下来的处理。
```

> 你也可以设置是否等待消息发出

- sent=”true” 等待消息发出，消息发送失败将抛出异常。
- sent=”false” 不等待消息发出，将消息放入 IO 队列，即刻返回。

```xml
<dubbo:method name="findFoo" async="true" sent="true" />
```

> 如果你只是想异步，完全忽略返回值，可以配置 return=”false”，以减少 Future 对象的创建和管理成本

```xml
<dubbo:method name="findFoo" async="true" return="false" />
```

**注意**:如果服务端长时间进行堵塞，客户端可能会发生超时问题，所以有时可能要在前台设置超时时间


**坑点**：dubbo的一部调用会延续一次，也就是说a一部调用b，b同步调用c，其实上b还是异步调用c

### dubbo内置调用拦截

在本地拦截方法调用过程中的 before after throww  return过程  其实相当于为dubbo远程调用的处理工程提供了统一的模板 （注意dubbo的哲学思想——提供一个公共的api，使用api进行相互的调用）

服务端配置方法

```xml
<dubbo:service interface="com.foo.BarService" stub="true" />
<dubbo:service interface="com.foo.BarService" stub="com.foo.BarServiceStub" />
```

公共api提供，Barservice接口的Stub实现

```java
package com.foo;
public class BarServiceStub implements BarService { 
    private final BarService barService;
 
    // 构造函数传入真正的远程代理对象
    public (BarService barService) {
        this.barService = barService;
    }
 
    public String sayHello(String name) {
        // 此代码在客户端执行, 你可以在客户端做ThreadLocal本地缓存，或预先验证参数是否合法，等等
        try {
            return barService.sayHello(name);
        } catch (Exception e) {
            // 你可以容错，可以做任何AOP拦截事项
            return "容错数据";
        }
    }
}
```

本地伪装  通常用于服务降级，比如某验权服务，当服务提供方全部挂掉后，客户端不抛出异常，而是通过 Mock 数据返回授权失败。

服务端配置方法

```xml
<dubbo:service interface="com.foo.BarService" mock="true" />
<dubbo:service interface="com.foo.BarService" mock="com.foo.BarServiceMock" />
```

公共api提供接口的Mock实现

```java
package com.foo;
public class BarServiceMock implements BarService {
    public String sayHello(String name) {
        // 你可以伪造容错数据，此方法只在出现RpcException时被执行
        return "容错数据";
    }
}
```

这样当发生调用异常的时候，将会调用上面Mock类相应的方法，使用调用

### 服务懒链接和延迟暴露和对应调用

```xml
<dubbo:service delay="5000" />
<dubbo:service delay="-1" /> 等到spring框架初始化完成后再进行调用
```

```xml
<dubbo:protocol name="dubbo" lazy="true" />当调用发起后再进行相应的链接
```

```xml
<dubbo:protocol name="dubbo" sticky="true" />  尽可能让调用者一直调用相同的服务器
```

### 并发控制和链接控制

服务端和客户端并发控制配置

```xml
限制 com.foo.BarService 的每个方法，服务器端并发执行（或占用线程池线程数）不能超过 10 个
<dubbo:service interface="com.foo.BarService" executes="10" />
限制 com.foo.BarService 的 sayHello 方法，服务器端并发执行（或占用线程池线程数）不能超过 10 个：
<dubbo:service interface="com.foo.BarService">
    <dubbo:method name="sayHello" executes="10" />
</dubbo:service>
限制 com.foo.BarService 的每个方法，每客户端并发执行（或占用连接的请求数）不能超过 10 个：
<dubbo:service interface="com.foo.BarService" actives="10" />
或
<dubbo:reference interface="com.foo.BarService" actives="10" />
限制 com.foo.BarService 的 sayHello 方法，每客户端并发执行（或占用连接的请求数）不能超过 10 个：
<dubbo:service interface="com.foo.BarService">
    <dubbo:method name="sayHello" actives="10" />
</dubbo:service>
<dubbo:reference interface="com.foo.BarService">
    <dubbo:method name="sayHello" actives="10" />
</dubbo:service>
```

**注意**：服务端的并发执行参数控制只能在服务端配置，配置参数executes  ， 客户端 并发执行参数，可在服务端或者客户端配置 参数active 客户端优先

服务端链接控制

```xml
<dubbo:provider protocol="dubbo" accepts="10" />
<dubbo:protocol name="dubbo" accepts="10" />
```

客户端链接控制

```xml
<dubbo:reference interface="com.foo.BarService" connections="10" />
<dubbo:service interface="com.foo.BarService" connections="10" />
```

### 一个概念：范化引用

泛化接口调用方式主要用于客户端没有 API 接口及模型类元的情况，参数及返回值中的所有 POJO 均用 Map 表示，通常用于框架集成，