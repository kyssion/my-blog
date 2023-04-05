

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


### spring boot 上层异常处理模块FailureAnalyzers

这个模块用来封装一些spring 内置的异常问题，用来显示解决方案，暂时不做深入的研究



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

