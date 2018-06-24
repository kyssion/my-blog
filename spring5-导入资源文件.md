## spring5-导入资源文件

一般情况下一些配置属性都是使用配置文件进行导入的，在一定的程度上进行了解藕，这里整理一下java 和spring框架在获取资源上的一些配配置

### java进行资源的配置

```java
public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        method();
    }
    //简单使用java进行配置文件的读取
    public static void method(){
        Properties properties= new Properties();
        try {
            properties.load(new FileInputStream(Thread.currentThread().getContextClassLoader().getResource("bean.properties").getPath()));
        } catch (IOException e) {
            e.printStackTrace();
        }
        User user = new User();
        user.setName(properties.getProperty("user.name"));
        user.setPassword(properties.getProperty("user.password"));
        user.say();
    }
}
```

**坑点**：Thread.currentThread().getContextClassLoader() 可以获得项目编译后的执行根目录相当于 maven项目 的resource， 这一点非常重要

### 使用spring的bean.xml配置文件导入相关的配置 

```xml

<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
    <bean id="propertyConfigurer"
          class="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer">
        <property name="locations">
            <list>
                <value>classpath:bean.properties</value>
            </list>
        </property>
    </bean>
    <bean id="user" class="org.demo.bean.User" scope="singleton">
        <property name="name" value="${user.name}"></property>
        <property name="password" value="${user.password}"></property>
    </bean>
</beans>
```

### spring 增强配置文件处理使用注解进行相关的各种配置

```java
@Service
@PropertySource("classpath:bean.properties")
public class User {
    @Value("${user.name}")
    private String name;
    @Value("${user.password}")
    private String password;
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
    public void say(){
        System.out.println(this.name+" "+this.password);
    }
}
```
使用 java 的@value 和 PropertySource 注解结合使用

### springboot-导入资源文件增强

spring boot 通过注解的方法将各种属性通过自动化的形式加载进javabean中，简化操作。
```java
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

配置文件

```
auther.name=liyuelin
auther.password=14159265jkl
```

@ConfigurationProperties注解将会对 自动注入相关配置文件中的属性省去 前缀自动的注入到相关的配置文件中

升级版注解  @EnableConfigurationProperties(MyconfigProperties.class)  一般结合 @configuration注解使用    —-将指定的类似上面javabean的bean 自动完成属性注入功能

```java
@Configuration
@EnableConfigurationProperties(MyconfigProperties.class)//允许这个类进行自动转配并且导入配置文件属性
@EnableAspectJAutoProxy
@EnableAutoConfiguration
@ConfigurationProperties
 
public class MyconfigAutoConfig {
 
}
```