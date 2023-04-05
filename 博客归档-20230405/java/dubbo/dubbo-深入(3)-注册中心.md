## 深入dubbo（二）注册中心

注册中心只要解决的问题就是，服务端和消费端的相互发现的问题，断开重链接的问题

### 基于广播实现注册的Multicast 注册中心

Multicast 注册中心不需要启动任何中心节点，只要广播地址一样，就可以互相发现。

![](blogimg/dubbo/3.jpg)

1. 提供方启动时广播自己的地址
2. 消费方启动时广播订阅请求
3. 提供方收到订阅请求时，单播自己的地址给订阅者，如果设置了 unicast=false，则广播给订阅者
4. 消费方收到提供方地址时，连接该地址进行 RPC 调用。

配置方法

```xml
<dubbo:registry address="multicast://224.5.6.7:1234" />
<dubbo:registry protocol="multicast" address="224.5.6.7:1234" />
```

为了减少广播量，Dubbo 缺省使用单播发送提供者地址信息给消费者，如果一个机器上同时启了多个消费者进程，消费者需声明 unicast=false，否则只会有一个消费者能收到消息

```xml
<dubbo:registry address="multicast://224.5.6.7:1234?unicast=false" />
<dubbo:registry protocol="multicast" address="224.5.6.7:1234">
    <dubbo:parameter key="unicast" value="false" />
</dubbo:registry>
```

**注意问题**,hostname需要为本地的ip地址（不能是127.0.0.1），ubuntu系统需要修改hosts文件

### 使用基于zookeeper的注册中心

注册依赖于zookeeper底层树实现

![](blogimg/dubbo/4.jpg)

**流程说明：**

1. 服务提供者启动时: 向 /dubbo/com.foo.BarService/providers 目录下写入自己的 URL 地址
2. 服务消费者启动时: 订阅 /dubbo/com.foo.BarService/providers 目录下的提供者 URL 地址。并向 /dubbo/com.foo.BarService/consumers 目录下写入自己的 URL 地址
3. 监控中心启动时: 订阅 /dubbo/com.foo.BarService 目录下的所有提供者和消费者 URL 地址。

**功能特点：**

1. 提供者出现断电等异常停机时，注册中心能自动删除提供者信息，注册中心重启时，能自动恢复注册数据，以及订阅请求，会话过期时，能自动恢复注册数据，以及订阅请求
2. <dubbo:registry check=“false“ /> 时，记录失败注册和订阅请求，后台定时重试
3. 通过 <dubbo:registry username=“admin“ password=“1234“ /> 设置 zookeeper 登录信息
4. <dubbo:registry group=“dubbo“ /> 设置 zookeeper 的根节点，不设置将使用无根树
5. * 号通配符 <dubbo:reference group=“*“ version=“*“ />，可订阅服务的所有分组和所有版本的提供者
6. 注意：使用zk进行注册中心配置的时候，需要对依赖包尽进行配置

> Zookeeper 单机配置:

```xml
<dubbo:registry address="zookeeper://10.20.153.10:2181" /> 
<!--或者-->
<dubbo:registry protocol="zookeeper" address="10.20.153.10:2181" /> 
```

> Zookeeper 集群配置：

```xml
<dubbo:registry address="zookeeper://10.20.153.10:2181?backup=10.20.153.11:2181,10.20.153.12:2181" /> 
<!--或者-->
<dubbo:registry protocol="zookeeper" address="10.20.153.10:2181,10.20.153.11:2181,10.20.153.12:2181" /> 
```

> 同一 Zookeeper，分成多组注册中心:

```xml
<dubbo:registry id="chinaRegistry" protocol="zookeeper" address="10.20.153.10:2181" group="china" /> 
<dubbo:registry id="intlRegistry" protocol="zookeeper" address="10.20.153.10:2181" group="intl" />
```

### 使用redis作为配置中心

![](blogimg/dubbo/5.jpg)

使用 Redis 的 Key/Map 结构存储数据结构：主 Key 为服务名和类型，Map 中的 Key 为 URL 地址，Map 中的 Value 为过期时间，用于判断脏数据，脏数据由监控中心删除     

具体流程将上图，因为使用很少，暂时不做讨论