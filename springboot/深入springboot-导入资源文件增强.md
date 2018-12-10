## 深入springboot-导入资源文件增强

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