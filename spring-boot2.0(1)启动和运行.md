
spring boot 一般基于maven进行配置

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