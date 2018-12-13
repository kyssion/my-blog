
导引： 1. spring boot监听事件的使用 2. spring boot 内置监听事件初始化applicationContext 3. CommandLineRunner接口和ApplicationRunner类

### spring boot 中的上下文监听器和事件

spring boot的事件和 spring原生的事件没有什么差别但是，spring boot 有一些自己的事件

1. ApplicationStartingEvent在运行开始时但在任何处理之前发送，除了注册侦听器和初始化器之外。
2. ApplicationEnvironmentPreparedEvent当在上下文中使用的环境是已知的但在创建上下文之前发送。
3. ApplicationPreparedEvent在刷新开始之前但在bean定义加载之后发送。
4. ApplicationStartedEvent在刷新上下文之后但在调用任何应用程序和命令行参赛者之前发送。
5. ApplicationReadyEvent在任何应用程序和命令行参数被调用后发送。 它表示应用程序已准备好为请求提供服务。
6. ApplicationFailedEvent如果启动时出现异常，则发送。

注意有些事件可能是在applicatincontext之前就出发了，所以不能使用@bean的方法注册在容器中，在spring boot 中可以应如下的方法注册监听器,使用方法：SpringApplication.addListeners(…​)， SpringApplicationBuilder.listeners(…​)，配置文件中添加：META-INF/spring.factories 中 org.springframework.context.ApplicationListener

注意了：因为spring拥有上下文的关系，而监听器除了监听自己的时间还会监听子元素的事件，所以在实现监听器的时候官方推荐同时实现ApplicationContextAware接口，来比较事件的context和和自身context的关系。

```java
public class MyApplicationListener implements ApplicationListener<ApplicationEvent>{
	@Override
	public void onApplicationEvent(ApplicationEvent arg0) {
	}
}
```

> 总结添加事件的三种方法

1. @bean
2. SpringApplication.addListeners(…​)， SpringApplicationBuilder.listeners(…​)
3. 配置文件中添加：META-INF/spring.factories 中 org.springframework.context.ApplicationListener

### spring boot 应用环境的判断构建ApplicationContext

我们在没有使用spring boot 单纯的使用spring 或者使用spring mvc 的时候通常使用的application是XmlServletWebServerApplicationContext，或者ClasspathXmlApplicationContext ， 同样spring boot 基于注解方法使用了一套特殊的context

1. 首先spring boot 判断这个环境是不是spring mvc 环境如果是马么webappcationcontext 选择AnnotationConfigServletWebServerApplicationContext

2. 否则判断是否是webflux 环境如果是 就使用AnnotationConfigReactiveWebApplicationContext

3. 最后如果都不是，使用AnnotationConfigApplicationContext

这样有一个问题，如果是spring mvc 和spring webflux 同时使用的时候将会造成使用springmvc 的环境，为了解决这个问题，可以使用setWebApplicationType(WebApplicationType)方法，或者使用setApplicationContextClass(…​)**有待确认**.

### spring bootW启动前执行特定的程序

在spring boot中 ， spring boot 会在容器彻底启动前运行实现现CommandLineRunner接口的bean或者ApplicationRunner接口的bean

```java
import org.springframework.boot.*;
import org.springframework.stereotype.*;
@Component
public class MyBean implements CommandLineRunner {
	public void run(String... args) {
		// Do something...
		args就是main传入的string数组
	}
}
```

```java
class Runtest implements ApplicationRunner {
	//自动注入进来
	@AutoWrite
	ApplicationArguments run;

    @Override
    public void run(ApplicationArguments args) throws Exception {
        // Do something...
		这里传入的是spring 对传入数据的封装
    }
}
```

注意这两个接口其中第二个接口传递命令的额外参数使用的是ApplicationArguments这个类（第一个和main相同）

> 注意如果系统想使用，运行的时候传入的数据的话，可以使用ApplicationArguments 这个参数将相关的值注入进来或者使用ApplicationRunner接口或者CommandLineRunner初始化