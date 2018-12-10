## 深入dubbo（一）基本使用初探

### 互联网架构升级过程图

![](blogimg/dubbo/1.jpg)

单一应用架构(单机部署所有的应用)——>垂直应用架构(将单机的应用部署到相关的各种分开的服务器上，各个服务器相互独立)——>分布式服务架构(在之前的各个部分出现了交互的过程)——>流动计算架构soa(当系统变得复杂，各种交互混乱，玉树出现了基于中央调度的整合配置机制)——>微服务

### dubbo的作用

- 作为服务注册中心，动态的注册和发现服务，使服务的位置透明并通过在消费方获取服务提供方地址列表，实现软负载均衡和 Failover（失效备份），降低对 F5 硬件负载均衡器的依赖
- 自动画出应用间的依赖关系图，以帮助架构师理清理关系。
- 将服务现在每天的调用量，响应时间，都统计出来，作为容量规划的参考指标，可以动态调整权重，在线上，将某台机器的权重一直加大，并在加大的过程中记录响应时间的变化，直到响应时间到达阀值，记录此时的访问量，再以此访问量乘以机器数反推总容量

### dubbo的基本架构

![](blogimg/dubbo/2.jpg)

节点|角色说明
---|---
Provider|暴露服务的服务提供方
Consumer|调用远程服务的服务消费方
Registry|服务注册与发现的注册中心
Monitor|统计服务的调用次调和调用时间的监控中心
Container|服务运行容器

### 基本使用方法

引申，其实dubbo并没有那么难，首先他需要的一组公共的接口，作为对外面提供的服务的入口，dubbo框架处理了寻找服务提供者等过程，使用者可以就像使用spring框架那样进行dubbo的使用，见下面的例子

1. 公共的接口

注意：这个公共的接口一定要有包名，否则dubbo内部的反射处理方法将会报空值错误

```java
package service;
public interface DemoService {
    public String say();
}
```

提供maven贡其他组件使用

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>demo</artifactId>
        <groupId>org.fen</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>
    <artifactId>demoAPI</artifactId>
</project>
```

2. provider服务提供者

xml配置文件，注意对外提供的服务一定要是接口

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:dubbo="http://code.alibabatech.com/schema/dubbo"
       xmlns="http://www.springframework.org/schema/beans"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-2.5.xsd
	http://code.alibabatech.com/schema/dubbo http://code.alibabatech.com/schema/dubbo/dubbo.xsd">
    <dubbo:application name="provider"></dubbo:application>
    <dubbo:registry address="multicast://224.5.6.10:1253"/>
    <dubbo:protocol name="dubbo" port="20880"/>
    <bean id="myfirstdemo" class="DemoSayImp"></bean>
    <dubbo:service interface="service.DemoService" ref="myfirstdemo"></dubbo:service>
</beans>
```

> 接口实现类

```java
import service.DemoService;
 
//public class DemoSayImp implements DemoSay{
public class DemoSayImp implements DemoService {
    public String say() {
        System.out.println("this is my say");
        return "sdfsdf";
    }
}
```
> 服务启动入口

```java
import org.springframework.context.support.ClassPathXmlApplicationContext;
 
import java.io.IOException;
 
public class Main {
    public static void main(String[] args) {
        ClassPathXmlApplicationContext applicationContext =
                new ClassPathXmlApplicationContext("bean.xml");
        applicationContext.start();
        try {
            System.in.read();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

注意：linux系统需要修改/etc/hosts文件将hostname对应的ip地址改成现在电脑对应网卡的ip地址

3. consumer 消费者

> xml配置文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:dubbo="http://code.alibabatech.com/schema/dubbo"
       xmlns="http://www.springframework.org/schema/beans"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-2.5.xsd
	http://code.alibabatech.com/schema/dubbo http://code.alibabatech.com/schema/dubbo/dubbo.xsd">
    <dubbo:application name="consumer"></dubbo:application>
    <dubbo:registry address="multicast://224.5.6.10:1253"/>
    <dubbo:reference interface="service.DemoService" id="demoService"></dubbo:reference>
</beans>
```

> 消费者程序入口

```java
import org.springframework.context.support.ClassPathXmlApplicationContext;
import service.DemoService;
 
public class Main {
    public static void main(String[] args) {
        ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext(new String[]{"bean.xml"});
        //context.start();
        DemoService demoService = (DemoService) context.getBean("demoService"); // 获取远程服务代理
        String hello = demoService.say(); // 执行远程方法
        System.out.println(hello); // 显示调用结果
    }
}
```
