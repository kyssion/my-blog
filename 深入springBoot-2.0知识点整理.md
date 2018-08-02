### springboot 配置的核心元素

spring 只用maven的parent继承的方法（gradle类似）进行依赖管理和使用maven插件（gradle同样类似）的方法生成可执行的jar文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<groupId>com.example</groupId>
	<artifactId>myproject</artifactId>
	<version>0.0.1-SNAPSHOT</version>
    <!--使用继承的方法实现自动化配置-->
	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>2.0.1.RELEASE</version>
	</parent>
	<!-- Additional lines to be added here... -->
    <!--使用maven插件实现自动化配置-->
    <build>
	    <plugins>
		    <plugin>
			    <groupId>org.springframework.boot</groupId>
			    <artifactId>spring-boot-maven-plugin</artifactId>
		    </plugin>
	    </plugins>
    </build>
</project>
```

当不使用parent进行依赖配置的时候可以使用dependencyManagement来进行管理

```xml
<dependencyManagement>
		<dependencies>
		    <dependency>
			    <!-- Import dependency management from Spring Boot -->
			    <groupId>org.springframework.boot</groupId>
			    <artifactId>spring-boot-dependencies</artifactId>
			    <version>2.0.1.RELEASE</version>
			    <type>pom</type>
			    <scope>import</scope>
		</dependency>
	</dependencies>
</dependencyManagement>
```
### springBoot starter-springBoot可以实现自动化配置的核心方法

springBoot提供了一系列的starter方便进行自动化配置，比如spring-boot-starter-web

> springBoot starter 明明规则：如果是官法的starter 将会按照spring-boot-starter-* 来进行划分，如果是自己实现的starter方法，建议按照*-spring-boot-starter 来进行命名

这里介绍一个特边的非应用starter，spring-boot-starter-actuator，这个starter实现了监控的功能

```xml
<dependency>  
    <groupId>org.springframework.boot</groupId>  
    <artifactId>spring-boot-starter-actuator</artifactId>  
</dependency>  
```
### spring boot 热部署工具  Developer Tools

spring boot 实现了一定程度下的热部署功能，暂时不做过多的讨论

```xml
<dependencies>
	<dependency>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-devtools</artifactId>
		<optional>true</optional>
	</dependency>
</dependencies>
```

### spring 个性化配置自定义横幅

比如在classpath中写入一个 banner.txt文件springboot将自动的将这个文件打印到开始运行的地方

banner.txt 还可以针对java的MANIFEST.MF文件进行个性化配置比如：

- ${application.formatted-version}，${application.version} 打印在MANIFEST.MF文件中Implementation-Version: 1.0字段的1.0版本号，如果是前者将会带上v前缀 v1.0

- ${spring-boot.formatted-version}，${spring-boot.version} 打印spring的版本号，同样前者有前缀

- ${application.title} 打印在MANIFEST.MF文件中Implementation-Title: MyApp字段中的MyApp

sp：如果要以编程方式生成横幅，则可以使用SpringApplication.setBanner（...）方法。使用org.springframework.boot.Banner接口并实现您自己的printBanner（）方法。
还可以使用spring.main.banner-mode属性来确定横幅是否必须在System.out（控制台）上打印，发送到配置的记录器（日志），还是根本不生成（关闭）

yaml 文件中使用的是如下的配置

```yaml
spring:
	main:
		banner-mode: "off"
```

### spring boot 的启动方法

```java
public static void main(String[] args) {
	SpringApplication app = new SpringApplication(MySpringConfiguration.class);
	app.setBannerMode(Banner.Mode.OFF);
	app.run(args);
}
```
注意这里传递过去的参数是一个配置源，也就是说这个类必须是@Configuration或者是一个继承@Configuration注解标记的类

当然，也可以通过使用application.properties文件来配置SpringApplication，但是这里涉及到springboot外部化配置，见下面

springboot 还可以使用流式布局构建application的上下文关系，具体的实现如下

```java
new SpringApplicationBuilder()
		.sources(Parent.class)
		.child(Application.class)
		.bannerMode(Banner.Mode.OFF)
		.run(args);
```

注意：Web组件必须包含在子上下文中，并且父环境和子环境都使用相同的环境

### spring boot 上层异常处理模块FailureAnalyzers

这个模块用来封装一些spring 内置的异常问题，用来显示解决方案，暂时不做深入的研究

### spring boot 中的上下文监听器和事件

spring boot的事件和 spring原生的事件没有什么差别但是，spring boot 有一些自己的事件

1. ApplicationStartingEvent在运行开始时但在任何处理之前发送，除了注册侦听器和初始化器之外。

2. ApplicationEnvironmentPreparedEvent当在上下文中使用的环境是已知的但在创建上下文之前发送。

3. ApplicationPreparedEvent在刷新开始之前但在bean定义加载之后发送。

4. ApplicationStartedEvent在刷新上下文之后但在调用任何应用程序和命令行参赛者之前发送。

5. ApplicationReadyEvent在任何应用程序和命令行参数被调用后发送。 它表示应用程序已准备好为请求提供服务。

6. ApplicationFailedEvent如果启动时出现异常，则发送。

在spring boot 中可以使用如下的方法注册监听器

使用方法：SpringApplication.addListeners(…​)， SpringApplicationBuilder.listeners(…​)，

配置文件中添加：META-INF/spring.factories 中 org.springframework.context.ApplicationListener

注意了：因为spring拥有上下文的关系，而监听器除了监听自己的时间还会监听子元素的时间，所以在实现监听器的时候官方推荐同时实现ApplicationContextAware接口，来比较事件的context和和自身context的关系

### spring boot 应用环境的判断

1. 首先spring boot 判断这个环境是不是spring mvc 环境如果是马么webappcationcontext 选择AnnotationConfigServletWebServerApplicationContext

2. 否则判断是否是webflux 环境如果是 就使用AnnotationConfigReactiveWebApplicationContext

3. 最后如果都不是，使用AnnotationConfigApplicationContext

这样有一个问题，如果是spring mvc 和spring webflux 同时使用的时候将会造成使用springmvc 的环境，为了解决这个问题，可以使用setWebApplicationType(WebApplicationType)方法，或者使用setApplicationContextClass(…​)**有待确认**.

### spring boot 启动前执行特定的程序

要想实现这个方法，需要在spring 容器中添加实现CommandLineRunner接口的bean或者ApplicationRunner接口的bean

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
    @Override
    public void run(ApplicationArguments args) throws Exception {
        // Do something...
		这里传入的是spring 对传入数据的封装
    }
}
```

#spring boot 带有状态的结束 使用exit 运行程序

在调用SpringApplication.exit（）时希望返回特定的退出代码，那么bean可以实现org.springframework.boot.ExitCodeGenerator接口。 ，然后可以将此退出代码传递给System.exit（）以将其作为状态代码返回，

```java
/**
* 接口只有一个方法
* @Compomet
* class Runtest implements ExitCodeGenerator {
*     @Override
*     public int getExitCode() {
*         return 0;
*     }
* }
*/

@SpringBootApplication
public class ExitCodeApplication {
	@Bean
	public ExitCodeGenerator exitCodeGenerator() {
		return () -> 42;
	}
	public static void main(String[] args) {
		System.exit(SpringApplication
				.exit(SpringApplication.run(ExitCodeApplication.class, args)));
	}
}
```

###spring boot 核心注解

spring boot 是spring 零配置的升级，通过各种注解增强了spring容器

#### @SpringBootApplication

这个其实是一个聚合接口，这个接口聚合了@SpringBootConfiguration（和Configuration注解相同），@EnableAutoConfiguration，@ComponentScan注解，实现了自动化配置等功能，同样可以实现自己的方法来实现自动化配置

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(excludeFilters = {
		@Filter(type = FilterType.CUSTOM, classes = TypeExcludeFilter.class),
		@Filter(type = FilterType.CUSTOM, classes = AutoConfigurationExcludeFilter.class) })
public @interface SpringBootApplication {

	@AliasFor(annotation = EnableAutoConfiguration.class)
	Class<?>[] exclude() default {};

	@AliasFor(annotation = EnableAutoConfiguration.class)
	String[] excludeName() default {};

	@AliasFor(annotation = ComponentScan.class, attribute = "basePackages")
	String[] scanBasePackages() default {};

	@AliasFor(annotation = ComponentScan.class, attribute = "basePackageClasses")
	Class<?>[] scanBasePackageClasses() default {};
}
```

#### @Configuration

spring boot 鼓励使用java配置类的配置方法，如果一定要使用xml的配置，也同样**建议使用@Configuration注解并加上下面的注解**

#### @ImportResource

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@Documented
public @interface ImportResource {
	@AliasFor("locations")
	String[] value() default {};
	@AliasFor("value")
	String[] locations() default {};
	Class<? extends BeanDefinitionReader> reader() default BeanDefinitionReader.class;
}

```
这个注解注解在java类上面，通过importResource的value或者locations指定，文件的路径，reader是一个解析器，默认情况下，阅读器将适应指定的资源路径：“.groovy”文件将使用GroovyBeanDefinitionReader进行处理; 而所有其他资源将使用XmlBeanDefinitionReader进行处理。

#### @Enable* 系列注解

@Enable* 系列注解是springboot实现自动化配置的核心方法，这种方法将自动的将相关的需要配置的方法进行配置

官方文档中介绍的，springboot 的自动化配置是非侵入的方式，自己实现的方法将会覆盖系统实现的方法。如果想要知道springboot应用了什么自动化配置，请使用debug模式运行springboot，并且打印出springboot的配置调用日志

1. @EnableAutoConfiguration

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@AutoConfigurationPackage
@Import(AutoConfigurationImportSelector.class)
public @interface EnableAutoConfiguration {
	String ENABLED_OVERRIDE_PROPERTY = "spring.boot.enableautoconfiguration";
	Class<?>[] exclude() default {};
	String[] excludeName() default {};
}
```

2. 

#### @ComponentScan

并不是springboot特有的接口，应为springboot 需要spring零配置相关的功能，所以记录在这里，如果没有参数将会通过这个方法作为跟路径向下搜索自动化配置的相关信息


#### @Import({ MyConfig.class, MyAnotherConfig.class })

这个注解可以自定义配置需要的配置类，从而实现自定义类似@springbootapplication注解

```java
package com.example.myapplication;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
@SpringBootApplication // same as @Configuration @EnableAutoConfiguration @ComponentScan
public class Application {
	public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}
}
```

