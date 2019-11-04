spring 从3.0 开始支持java配置所以这里整理一下spring 3之后重要的知识

# spring application

回顾一下application的东西，负责初始化spring bean容器的非常重要的类

# bean

在spring中所有的javabean都将会初始化为BeanDefinition对象

这个类其实承载了javabean中所有的元数据包括：

1. javabean中的各种属性，类名等
2. javabean的实例化对象
3. Bean行为配置元素，用于声明Bean在容器中的行为（作用域，生命周期回调等）
4. 对其他bean进行工作所需的引用。这些引用也称为协作者或依赖项

除了包含有关如何创建特定bean的信息的bean定义之外，通过applicationcontext方法getBeanFactory()返回的BeanFactory 实现DefaultListableBeanFactory可以实现javabean的手动注入。DefaultListableBeanFactory 通过registerSingleton(..)和 registerBeanDefinition(..)方法支持此注册。

# bean的使用范围


范围|内容
---|---
singleton|(默认)将每个Spring IoC容器的单个bean定义范围限定为单个对象实例
prototype|将单个bean定义的作用域限定为任意数量的对象实例
request|将单个bean定义的范围限定为单个HTTP请求的生命周期
session|将单个bean定义的作用域限定为HTTP会话的生命周期
application|将单个bean定义的作用域限定为ServletContext的生命周期
websocket|将单个bean定义的作用域限定为WebSocket的生命周期

在java配置方法中可以使用@ApplicationScope来制定作用环境

# bean作用域自定义

暂时省略

# spring bean 生命周期控制

## spring bean 生命周期回调钩子

spring 提供了两种生命周期回调钩子 接扣和注解

1. 实现Spring InitializingBean和DisposableBean接口，分别提供了afterPropertiesSet()和destroy()后者使bean在初始化和销毁​​bean时执行某些操作
2. 使用@PostConstruct和@PreDestroy 注解

## 监听容器和spring 状态的钩子

- Lifecycle接口，用来监听spring bean状态的钩子

```java
public interface Lifecycle {
    void start();
    void stop();
    boolean isRunning();
}
```

- LifecycleProcessor 用来对ApplicationContext的重启和关闭做反应的接口

```java
public interface LifecycleProcessor extends Lifecycle {
    void onRefresh();
    void onClose();
}
```

## Phased 和SmartLifecycle 

- Phased接口提供提供了优先级，数字越小越早运行越晚关闭

```java
public interface Phased {
    int getPhase();
}
```

- SmartLifecycle 

```java
public interface SmartLifecycle extends Lifecycle, Phased {
    boolean isAutoStartup();
    void stop(Runnable callback);
}
```

该LifecycleProcessor接口还定义了用于刷新和关闭上下文的回调方法。后者驱动关闭过程，就好像stop()已经显式调用了它一样，但是它在上下文关闭时发生。另一方面，“刷新”回调启用了SmartLifecyclebean的另一个功能 。刷新上下文时（在所有对象都被实例化和初始化之后），该回调将被调用。此时，默认的生命周期处理器将检查每个SmartLifecycle对象的isAutoStartup()方法返回的布尔值 。如果为true，则在该点启动该对象，而不是等待上下文或其自身的显式调用start()方法（与上下文刷新不同，对于标准上下文实现，上下文启动不会自动发生）

## 优雅关闭spring  非web项目

使用 使用applicationContext 的 registerShutdownHook() 方法即可

## ApplicationContextAware和BeanNameAware

这两个接口 一个获取上下文信息 一个获取bean的名称

## 其他Aware

| 名称                           | 注入依赖                                                                                    | 在...中解释                                   |
|--------------------------------|---------------------------------------------------------------------------------------------|-----------------------------------------------|
| ApplicationContextAware        | 宣告ApplicationContext。                                                                    | ApplicationContextAware 和 BeanNameAware      |
| ApplicationEventPublisherAware | 附件的事件发布者ApplicationContext。                                                        | 的其他功能 ApplicationContext                 |
| BeanClassLoaderAware           | 类加载器，用于加载Bean类。                                                                  | 实例化豆                                      |
| BeanFactoryAware               | 宣告BeanFactory。                                                                           | ApplicationContextAware 和 BeanNameAware      |
| BeanNameAware                  | 声明bean的名称。                                                                            | ApplicationContextAware 和 BeanNameAware      |
| BootstrapContextAware          | BootstrapContext容器在其中运行的资源适配器。通常仅在支持JCA的ApplicationContext实例中可用。 | JCA CCI                                       |
| LoadTimeWeaverAware            | 定义的编织器，用于在加载时处理类定义。                                                      | 在Spring Framework中使用AspectJ进行加载时编织 |
| MessageSourceAware             | 解决消息的已配置策略（支持参数化和国际化）。                                                | 的其他功能 ApplicationContext                 |
| NotificationPublisherAware     | Spring JMX通知发布者。                                                                      | 通知事项                                      |
| ResourceLoaderAware            | 配置的加载程序，用于对资源的低级别访问。                                                    | 资源资源                                      |
| ServletConfigAware             | 当前ServletConfig容器在其中运行。仅在可感知网络的Spring中有效 ApplicationContext。          | 春季MVC                                       |
| ServletContextAware            | 当前ServletContext容器在其中运行。仅在可感知网络的Spring中有效 ApplicationContext。         | 春季MVC                                       |

# BeanPostProcessor

这个接口可以在spring bean初始化完成之后之前的回调接口

```java
package scripting;

import org.springframework.beans.factory.config.BeanPostProcessor;

public class InstantiationTracingBeanPostProcessor implements BeanPostProcessor {
    // simply return the instantiated bean as-is
    public Object postProcessBeforeInitialization(Object bean, String beanName) {
        return bean; // we could potentially return any object reference here...
    }
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        System.out.println("Bean '" + beanName + "' created : " + bean.toString());
        return bean;
    }
}
```

# PropertySourcesPlaceholderConfigurer 和 BeanFactoryPostProcessor 暂时不研究

# FactoryBean

FactoryBean界面提供了三种方法：
- Object getObject()：返回此工厂创建的对象的实例。实例可以共享，具体取决于该工厂是否返回单例或原型。
- boolean isSingleton()：true如果FactoryBean返回单例或false其他，则返回 。
- Class getObjectType()：返回getObject()方法返回的对象类型，或者null如果类型未知，则返回该对象类型。

# spring 资源化处理

## Resource InputStreamSource 

```java
public interface Resource extends InputStreamSource {
    //返回boolean指示此资源是否实际以物理形式存在。
    boolean exists();
    //返回，boolean指示此资源是否代表具有打开流的句柄。如果为true，InputStream则不能多次读取，必须只读取一次，然后将其关闭以避免资源泄漏。返回false所有常用资源实现（除外）InputStreamResource
    boolean isOpen();
    URL getURL() throws IOException;
    File getFile() throws IOException;
    Resource createRelative(String relativePath) throws IOException;
    String getFilename();
    //返回对此资源的描述，以便在使用该资源时用于错误输出。这通常是标准文件名或资源的实际URL
    String getDescription();
}

public interface InputStreamSource {
    //找到并打开资源，并返回一个资源以InputStream供读取。预计每次调用都会返回一个新的 InputStream。呼叫者有责任关闭流。
    InputStream getInputStream() throws IOException;
}
```

## 核心实现

UrlResource：能获取网络等所有的属性
ClassPathResource：能获取jar包中的文件
FileSystemResource：基本文件操作
ServletContextResource
InputStreamResource
ByteArrayResource

## 使用applicationContext 的 ResourceLoader 获取Resource

注意所有的applicationContext都实现了ResourceLoader接口

```java
public interface ResourceLoader {
    Resource getResource(String location);
}
```

```java
Resource template = ctx.getResource("some/resource/path/myTemplate.txt");
```

- 针对ClassPathXmlApplicationContext，该代码返回ClassPathResource。如果对FileSystemXmlApplicationContext实例执行相同的方法，则将返回 FileSystemResource。对于WebApplicationContext，它将返回 ServletContextResource。类似地，它将为每个上下文返回适当的对象

- 另一方面，ClassPathResource无论应用程序上下文类型如何，您都可以通过指定特殊classpath:前缀来强制使用

```java
Resource template = ctx.getResource("classpath:some/resource/path/myTemplate.txt");
Resource template = ctx.getResource("file:///some/resource/path/myTemplate.txt");
Resource template = ctx.getResource("https://myhost.com/resource/path/myTemplate.txt");
```

## 还可以使用ResourceLoaderAware 接口直接获得上下文的ResourceLooader

类似applicationAware的模式

```java
public interface ResourceLoaderAware {
    void setResourceLoader(ResourceLoader resourceLoader);
}
```

# spring 自动化配置

## @Required

注释适用于bean属性setter方法， 5.1 弃用

## @Autoweiter

### 使用位置

这个注解是spring 推荐使用的注解,支持三个位置的注入

- 属性

```java
public class MovieRecommender {
    private final CustomerPreferenceDao customerPreferenceDao;
    @Autowired
    private MovieCatalog movieCatalog;
    // ...
}
```

- 构造函数

```java
public class MovieRecommender {
    private final CustomerPreferenceDao customerPreferenceDao;
    @Autowired
    public MovieRecommender(CustomerPreferenceDao customerPreferenceDao) {
        this.customerPreferenceDao = customerPreferenceDao;
    }
    // ...
}
```

> 注意 : 从Spring Framework 4.3开始，@Autowired如果目标bean只定义一个构造函数，则不再需要在该构造函数上添加注释。但是，如果有几个构造函数可用，则必须至少注释一个构造函数，@Autowired以指示容器使用哪个构造函数。



- 普通方法

```java
public class MovieRecommender {
    private MovieCatalog movieCatalog;
    private CustomerPreferenceDao customerPreferenceDao;
    @Autowired
    public void prepare(MovieCatalog movieCatalog,
            CustomerPreferenceDao customerPreferenceDao) {
        this.movieCatalog = movieCatalog;
        this.customerPreferenceDao = customerPreferenceDao;
    }
    // ...
}
```

### 多个相同的类型支持

实用AutoWrite 默认情况下是使用类型进行注入的,如果有多个类型就会报错,所有spring支持数组接收方法

```java
@Autowired
private MovieCatalog[] movieCatalogs;
```

spring 还支持map 注入的方法

```java
public class MovieRecommender {
    private Map<String, MovieCatalog> movieCatalogs;
    @Autowired
    public void setMovieCatalogs(Map<String, MovieCatalog> movieCatalogs) {
        this.movieCatalogs = movieCatalogs;
    }
    // ...
}
```

默认情况下，当给定注入点没有匹配的候选bean可用时，自动装配将失败。对于声明的数组，集合或映射，至少应有一个匹配元素。???/

###  @AutoWrite spring5 新注解

从Spring Framework 5.0开始，您还可以使用@Nullable注释（任何包中的任何注释，例如，javax.annotation.Nullable来自JSR-305 的注释）

### 其他

您还可以使用@Autowired对于那些众所周知的解析依赖接口：BeanFactory，ApplicationContext，Environment，ResourceLoader， ApplicationEventPublisher，和MessageSource。这些接口及其扩展接口（例如ConfigurableApplicationContext或ResourcePatternResolver）将自动解析，而无需进行特殊设置。以下示例自动装配ApplicationContext对象：

```java
public class MovieRecommender {

    @Autowired
    private ApplicationContext context;

    public MovieRecommender() {
    }

    // ...
}
```

### @AutoWrite 其他内容

@AutoWrite注解在方法上的场景???

## @Primary

用于当有多个候选者的时候进行装配优先是使用的标记

```java
@Configuration
public class MovieConfiguration {
    @Bean
    @Primary
    public MovieCatalog firstMovieCatalog() { ... }
    @Bean
    public MovieCatalog secondMovieCatalog() { ... }
    // ...
}
```

## @Qualifier

可用于自定义构造限制条件的注解,相当于一个自定义构造注入的扩展点

比如针对如下的定义

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:context="http://www.springframework.org/schema/context"
    xsi:schemaLocation="http://www.springframework.org/schema/beans
        https://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/context
        https://www.springframework.org/schema/context/spring-context.xsd">

    <context:annotation-config/>

    <bean class="example.SimpleMovieCatalog1">
        <qualifier value="main"/> 

        <!-- inject any dependencies required by this bean -->
    </bean>
    <bean class="example.SimpleMovieCatalog2">
        <qualifier type="Genre" value="Action"/>
        <!-- inject any dependencies required by this bean -->
    </bean>
</beans>
```

```java

@Target({ElementType.FIELD, ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
@Qualifier
public @interface Genre {

    String value();
}

public class MovieRecommender {

    //使用自定义的规则注入对象
    @Autowired
    @Genre("Action")
    private SimpleMovieCatalog2 actionCatalog;


    @Autowired
    @Qualifier("main")
    private SimpleMovieCatalog1 actionCatalog;

    // ...
}
```

## 自动装配泛型支持

spring 其实还支持泛型的自动装配,不同的泛型类型在java中算是不同的类型???

## Resource

和 @AutoWrite 类型相同 , 只是这个可以携带上name关键字表示实用名称来进行注入

# spring 注解高级玩法

## 元注解组合

在spring中可以讲一些注解进行任意的组合生成新的注解,并包含组合的注解的功能

```java
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Scope(WebApplicationContext.SCOPE_SESSION)
public @interface SessionScope {
    /**
     * Alias for {@link Scope#proxyMode}.
     * <p>Defaults to {@link ScopedProxyMode#TARGET_CLASS}.
     */
    @AliasFor(annotation = Scope.class)
    ScopedProxyMode proxyMode() default ScopedProxyMode.TARGET_CLASS;
}
```

@AliasFor注解表示使用继承的注解的哪个属性,对外暴漏,这个时候暴漏的熟悉属性可以在外层被覆盖掉

```java
@Service
@SessionScope(proxyMode = ScopedProxyMode.INTERFACES)
public class SessionScopedUserService implements UserService {
    // ...
}
```

## spring 自动化扫描功能支持 @Configuration  @ComponentScan(basePackages = "org.example")

## 注意这个功能必须@Configuration和ComponentScan连用才可以

```java
@Configuration
@ComponentScan(basePackages = "org.example")
public class AppConfig  {
    ...
}
```

## 指定扫描范围

```java
@Configuration
@ComponentScan(basePackages = "org.example", nameGenerator = MyNameGenerator.class)
public class AppConfig {
    ...
}
```

## 指定范围扫描自定义策略 ???

```java
@Configuration
@ComponentScan(basePackages = "org.example", scopeResolver = MyScopeResolver.class)
public class AppConfig {
    ...
}   
```

## scoped-proxy ???

```java
@Configuration
@ComponentScan(basePackages = "org.example", scopedProxy = ScopedProxyMode.INTERFACES)
public class AppConfig {
    ...
}
```

## 注意: 这个还支持过滤功能

```java
@Configuration
@ComponentScan(basePackages = "org.example",
        includeFilters = @Filter(type = FilterType.REGEX, pattern = ".*Stub.*Repository"),
        excludeFilters = @Filter(Repository.class))
public class AppConfig {
    ...
}
```


??? 增加支持过滤的表格信息

## @Bean 注册bean

```java
@Component
public class FactoryMethodComponent {

    private static int i;

    @Bean
    @Qualifier("public")
    public TestBean publicInstance() {
        return new TestBean("publicInstance");
    }

    // use of a custom qualifier and autowiring of method parameters
    @Bean
    protected TestBean protectedInstance(
            @Qualifier("public") TestBean spouse,
            @Value("#{privateInstance.age}") String country) {
        TestBean tb = new TestBean("protectedInstance", 1);
        tb.setSpouse(spouse);
        tb.setCountry(country);
        return tb;
    }

    @Bean
    private TestBean privateInstance() {
        return new TestBean("privateInstance", i++);
    }

    @Bean
    @RequestScope
    public TestBean requestScopedInstance() {
        return new TestBean("requestScopedInstance", 3);
    }
}
```

## 定义的时候提供限制符号

```java
@Component
@Qualifier("Action")
public class ActionMovieCatalog implements MovieCatalog {
    // ...
}
```


# spring 自动化配置 ??? 移动到上面和bean整理到一起

## spring bean自动化配置的承载类 AnnotationConfigApplicationContext 

这个ApplicationContext其实承载了java config类的解析功能

```java
public static void main(String[] args) {
    ApplicationContext ctx = new AnnotationConfigApplicationContext(MyServiceImpl.class, Dependency1.class, Dependency2.class);
    MyService myService = ctx.getBean(MyService.class);
    myService.doStuff();
}
//第二种方法使用 编程的方法构建
public static void main(String[] args) {
    AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext();
    ctx.register(AppConfig.class, OtherConfig.class);
    ctx.register(AdditionalConfig.class);
    ctx.refresh();
    MyService myService = ctx.getBean(MyService.class);
    myService.doStuff();
}
```

## @bean 描述依赖关系

在使用@Bean来描述依赖关系的时候,可以使用对应方法中的参数来进行依赖

```java
@Configuration
public class AppConfig {

    @Bean
    public TransferService transferService(AccountRepository accountRepository) {
        return new TransferServiceImpl(accountRepository);
    }
}
```

## @Bean 生命周期依赖


```java
public class BeanOne {

    public void init() {
        // initialization logic
    }
}

public class BeanTwo {

    public void cleanup() {
        // destruction logic
    }
}

@Configuration
public class AppConfig {

    @Bean(initMethod = "init")
    public BeanOne beanOne() {
        return new BeanOne();
    }

    @Bean(destroyMethod = "cleanup")
    public BeanTwo beanTwo() {
        return new BeanTwo();
    }
}
```

## bean范围???

```java
@Configuration
public class MyConfiguration {

    @Bean
    @Scope("prototype")
    public Encryptor encryptor() {
        // ...
    }
}
```

@Scope 和 scoped-proxy
Spring提供了一种通过作用域代理处理作用域依赖性的便捷方法 。使用XML配置时创建此类代理的最简单方法是<aop:scoped-proxy/>元素。使用@Scope注释在Java中配置bean 可以为该proxyMode属性提供同等的支持。默认值为无代理（ScopedProxyMode.NO），但您可以指定ScopedProxyMode.TARGET_CLASS或ScopedProxyMode.INTERFACES。

## 自定义Bean命名

```java
@Configuration
public class AppConfig {

    @Bean(name = "myThing")
    public Thing thing() {
        return new Thing();
    }
}
```

## bean @Description

提供bean的描述功能

```java
@Configuration
public class AppConfig {

    @Bean
    @Description("Provides a basic example of a bean")
    public Thing thing() {
        return new Thing();
    }
}
```

# @Configuration

## configuration import 加载其他类定义

```java
@Configuration
public class ConfigA {

    @Bean
    public A a() {
        return new A();
    }
}

@Configuration
@Import(ConfigA.class)
public class ConfigB {

    @Bean
    public B b() {
        return new B();
    }
}
```

## 灵活的注入配置@Conditional 

