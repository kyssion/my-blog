## 深入springBoot-入门

引申：Spring Boot是由Pivotal团队提供的全新框架，其设计目的是用来简化新Spring应用的初始搭建以及开发过程。该框架使用了特定的方式来进行配置，从而使开发人员不再需要定义样板化的配置。用我的话来理解，就是spring boot其实不是什么新的框架，它默认配置了很多框架的使用方式，就像maven整合了所有的jar包，spring boot整合了所有的框架（不知道这样比喻是否合适）。

### 核心注解@SpringBootApplication

> @SpringBootApplication是一个组合注解，整合了@EnableAutoConfiguration，@ComponentScan，@Configuration，其中@EnableAutoConfiguration会扫描包进行相关的javabean的配置等

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
	@AliasFor(annotation = EnableAutoConfiguration.class, attribute = "exclude")
	Class<?>[] exclude() default {};
	@AliasFor(annotation = EnableAutoConfiguration.class, attribute = "excludeName")
	String[] excludeName() default {};
	@AliasFor(annotation = ComponentScan.class, attribute = "basePackages")
	String[] scanBasePackages() default {};
	@AliasFor(annotation = ComponentScan.class, attribute = "basePackageClasses")
	Class<?>[] scanBasePackageClasses() default {};
}
```

样例

```java
@SpringBootApplication
public class MydemoApplication {
 
	public static void main(String[] args) {
		SpringApplication.run(MydemoApplication.class, args);
	}
}
```

### springboot的配置文件（application.properties or applicatin.yaml）

在springboot中可以指定 @PropertySource 注解进行手动导入spring boot配置的文件（配置文件地址数组）

```java
@SpringBootApplication
@PropertySource({"classpath:application.yaml"})
public class MydemoApplication {
 
	public static void main(String[] args) {
		SpringApplication.run(MydemoApplication.class, args);
	}
}
```

此外@PropertySource注解还能和@Value 和 @ConfigureProperties 注解配合使用，为元素添加属性，，（springboot在启动的时候将会自动的添加application.properties和application.yaml配置文件）

**注意**：和@value连用，只用SPElL表达式进行属性的自动装载

```java
@RestController
@SpringBootApplication
@PropertySource({"classpath:application.yaml","classpath:application.properties"})
public class MydemoApplication {
	@Value("${auther.name}")
	private String name;
	@Value("${auther.password}")
	private String password;
	@RequestMapping("/")
	public String say(){
		System.out.println(this.name+" :"+this.password);
		return this.name+" :"+this.password;
	}
	public static void main(String[] args) {
		SpringApplication.run(MydemoApplication.class, args);
	}
}
```

**注意**：和@ConfigurationProperties连用  注意要提供get和set方法   注解作用是自动的导入 springboot的配置文件（spring.properties或者spring.yml）中的相关属性

```java
@RestController
@SpringBootApplication
@PropertySource({"classpath:application.yaml","classpath:application.properties"})
@ConfigurationProperties(prefix = "auther")
public class MydemoApplication {
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    private String name;
    private String password;
    @RequestMapping("/")
    public String say(){
        System.out.println(this.name+" :"+this.password);
        return this.name+" :"+this.password;
    }
    public static void main(String[] args) {
        SpringApplication.run(MydemoApplication.class, args);
    }
}
```

### spring boot 载入 bean.xml配置文件

sring boot 源自于 spring 自然也能使用spring原生的相关配置文件

使用ImportResource（{“classpath:xxx.xml”}） 自动的导入相关的各种配置文安

```java
@SpringBootApplication
@ImportResource("")
public class SpringbootmybatisApplication implements CommandLineRunner {

    public static void main(String[] args) {
        SpringApplication.run(SpringbootmybatisApplication.class, args);
    }

    @Override
    public void run(String... args) throws Exception {

    }
}
```

### spring boot 非web项目启动

spring boot 启动方式是使用SpringApplication.run(SpringbootmybatisApplication.class, args); 进行启动

当使用自己的逻辑的时候，需要实现CommandLineRunner  接口并在run方法中进行相关逻辑的编写

```java
@MapperScan
@SpringBootApplication
@ImportResource("")
public class SpringbootmybatisApplication implements CommandLineRunner {

    public static void main(String[] args) {
        SpringApplication.run(SpringbootmybatisApplication.class, args);
    }

    @Override
    public void run(String... args) throws Exception {

    }
}
```

### spring boot 自动化配置标签

spring boot 便捷卡快度的根本原因是因为spring boot 提供自动化的Eable标签， 和动态处理@configuration配置类配置的@condition相关注解

1. enable***类

- @EnableConfigurationProperties：关联使用@ConfigurationProperties注解的类，然这个类可以进行初始化并且导入容器中，一般用在自定义starer
- @EnableAutoConfiguration：希望通过之前添加的jar依赖来实现 自动的配置你的Spring Application. 比如, 如果 HSQLDB 在你的 classpath中, 而且你没有配置任何数据库相关的bean,这时我们会自动配置一个内存数据库. 你只能加一个 @EnableAutoConfiguration 注解. 通常建议加在主 @Configuration 类上.   注意了查看源代码可以知道，这个注解组合类 @import注解，import一个EnableAutoConfigurationImportSelector.class类，这个类实现了import接口中的import  selectImports 方法，这个方法可以返回一个 class.getClassName() 数组，用来将相关的bean导入进class中
- @EnableAspectJAutoProxy： 启动spring自动aop 相当一xml文件中的<aop:aspectj-autoproxy> 让@Aspectj注解生效
- @EnableScheduling和@EnableAsync  见博客spring5框架知识整理-多线程和定时器   注意：EnableAsync 注解的configrution类可以实现一个Asyncconfig接口并且实现 接口实现类，返回一个数据连接池Exeturor
- @EnableTransactionManagement开起自动化事务配置<tx:annotation-driven transaction-manager=”myTransactionMamager”/>   @Transactional  标签提供支持

2. condition类 结合 configuuration注解尽心组合判断相关的配置是否有效

- ConditionalOnBean   当存在指定的cbean的时候生效
- ConditionalOnClass   当存在指定的class 文件是生效
- ConditionalOnMissBean  当不存在指定的 bean的时候生效
- ConditionalOnMissClass    当不存在指定的class  时生效
- ConditionalOnExpression    当使用的SpEl表达是true的时候才能进行使用
- ConditionalOnJava    指定java版本进行配置
- ConditionalOnProperty  当springboot 存在指定的相关配置文件中的属性的时候进行相关的配置
- ConditionalOnresource     当指定的资源存在的时候进行相关的配置
- @ConditionalOnSingleCandidate    当前的类在容器中只用一个的时候执行， springboot的例子是加载事务控制器的时候进行相关的操作

condition例子和分析见深入springBoot-自动配置原理和手动实现

