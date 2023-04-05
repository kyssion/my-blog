
导引： spring boot的简单配置，基本启动方法，和特殊关闭模式

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

> spring boot 提供了非常多的配置选项，具体的可以到官网上查询

### spring boot 热部署工具  Developer Tools 


spring boot 实现了一定程度下的热部署功能，暂时不做过多的讨论
配置

```xml配置
<dependencies>配置
	<dependency>配置
		<groupId>org.springframework.boot配置</groupId>
		<artifactId>spring-boot-devtools<配置/artifactId>
		<optional>true</optional>
	</dependency>
</dependencies>
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