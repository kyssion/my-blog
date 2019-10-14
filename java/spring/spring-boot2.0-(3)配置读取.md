导引： spring boot 总体上提供了三种外化配置 1. 使用@Value注释将属性值直接注入到bean中 2. pring的Environment抽象访问 3. 通过@ConfigurationProperties绑定到结构化对象，这里介绍一下

### spring boot 可以提供参数方式和覆盖原则

spring boot 可以通过如下的方法倒入相应的属性之，并且按照如下从上到下的顺序进行覆盖

1. Devtools 主目录上的全局设置属性（~/.spring-boot-devtools.properties当devtools处于活动状态时）。
2. @TestPropertySource 测试上的注释。
3. @SpringBootTest#properties 测试中的注释属性。
4. 命令行参数。
5. 来自SPRING_APPLICATION_JSON（嵌入在环境变量或系统属性中的内联JSON）的属性。
6. ServletConfig init参数。
7. ServletContext init参数。
8. JNDI属性来自java:comp/env。
9. Java系统属性（System.getProperties()）。
10. OS环境变量。
11. 一RandomValuePropertySource，只有在拥有性能random.*。
12. 特定于配置文件的应用程序属性在打包的jar（application-{profile}.properties和YAML变体）之外。
13. 打包在jar中的特定于配置文件的应用程序属性（application-{profile}.properties 以及YAML变体）。
14. 应用程序属性在打包的jar之外（application.properties和YAML变体）。
15. 打包在jar中的应用程序属性（application.properties和YAML变体）。
16. @PropertySource 你的@Configuration课上的注释。
17. 默认属性（由设置指定SpringApplication.setDefaultProperties）。

提供一个简单的使用内置属性的列子

```java
import org.springframework.stereotype.*;
import org.springframework.beans.factory.annotation.*;
@Component
public class MyBean {
    @Value("${name}")
    private String name;
    // ...
}
```

@Value 将会将环境中的name参数注入到MyBean的name属性中

> 注意: 这里解释一下上面的第五条： SPRING_APPLICATION_JSON 这个属性是一个环境变量属性，可以在环境中进行相关的配置，或者直接使用命令行$ SPRING_APPLICATION_JSON='{"acme":{"name":"test"}}' java -jar myapp.jar。

> 注意： json的方式解析在spring boot 中拥有两个地方，第一个上面的第9条：java -Dspring.application.json='{"name":"test"}' -jar myapp.jar 。第二个上面的第4条，$ java -jar myapp.jar --spring.application.json='{"name":"test"}'

> 注意： 解释上面的11 条随机参数

这个方法可以生成随机参数可以生成整数，长整数，uuids或字符串，如以下示例所示：

```
my.secret=${random.value}
my.number=${random.int}
my.bignumber=${random.long}
my.uuid=${random.uuid}
my.number.less.than.ten=${random.int(10)}
my.number.in.range=${random.int[1024,65536]}
```

注意最后两个使用了表达式的方法，int[start,end] 表示从start到end区间随机取数 int(max) 这种方式表示取的值不大于max