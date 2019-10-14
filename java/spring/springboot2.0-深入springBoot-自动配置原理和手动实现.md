## 深入springBoot-自动配置原理和手动实现

这里深入的分析一下为什么spring boot 可以进行 简单化配置, 如何进行手动配置

### spring如何进行相关的配置

springBoot的自动配置一般配置的源码包是放置在springboot-Autoconfig.jar包下面的

![](blogimg/springboot/1.png)

在springboot进行运行的时候，@SpringBoot注解提供了自动导入配置的@EableAutoConfiguration 注解  查看一下这个注解的源代码

```java
@SuppressWarnings("deprecation")
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@AutoConfigurationPackage
@Import(EnableAutoConfigurationImportSelector.class)
public @interface EnableAutoConfiguration {
    String ENABLED_OVERRIDE_PROPERTY = "spring.boot.enableautoconfiguration";
    Class<?>[] exclude() default {};
    String[] excludeName() default {};
}
```

分析源代码我们可以知道，注解中使用了Import注解将EnableAutoConfigurationImportSelector.class这个类进行运行，这个类将会自动的检测META/spring.factories文件，这个文件中声明了相关的各种配置

![](blogimg/springboot/2.png)

上面文件中的各配置类中都会发现在springboot中声明的各种配置注解 （在autoconfigure.config包下面）如@ConditionalOnProperty  @ConditionalOnMissingBean

```java
@Configuration
@AutoConfigureAfter(JmxAutoConfiguration.class)
@ConditionalOnProperty(prefix = "spring.application.admin", value = "enabled", havingValue = "true", matchIfMissing = false)
public class SpringApplicationAdminJmxAutoConfiguration {
    private static final String JMX_NAME_PROPERTY = "spring.application.admin.jmx-name";
    private static final String DEFAULT_JMX_NAME = "org.springframework.boot:type=Admin,name=SpringApplication";
    private final List<MBeanExporter> mbeanExporters;
    private final Environment environment;
    public SpringApplicationAdminJmxAutoConfiguration(
            ObjectProvider<List<MBeanExporter>> mbeanExporters, Environment environment) {
        this.mbeanExporters = mbeanExporters.getIfAvailable();
        this.environment = environment;
    }
    @Bean
    @ConditionalOnMissingBean
    public SpringApplicationAdminMXBeanRegistrar springApplicationAdminRegistrar()
            throws MalformedObjectNameException {
        String jmxName = this.environment.getProperty(JMX_NAME_PROPERTY,
                DEFAULT_JMX_NAME);
        if (this.mbeanExporters != null) { // Make sure to not register that MBean twice
            for (MBeanExporter mbeanExporter : this.mbeanExporters) {
                mbeanExporter.addExcludedBean(jmxName);
            }
        }
        return new SpringApplicationAdminMXBeanRegistrar(jmxName);
    }
}
```

![](blogimg/springboot/3.png)

分析一下最后一个注解

```java
@Target({ ElementType.TYPE, ElementType.METHOD })
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Conditional(OnWebApplicationCondition.class)
public @interface ConditionalOnWebApplication {}
```

发现使用OnWebApplicationCondition.class 这个类  ，找一下这个类

```java
class OnWebApplicationCondition extends SpringBootCondition{。。。。}
```

这个类就是实现了condition接口的根本类型  总结：如果要实现自定配置，并将这个配置好的类之前使用condition各种判断方法及你想嗯判断，然后放入spring.factories文件中就行（注意配置类就是一个使用@configuration注解进行标记配置类-也就是说，springBoot框架使用这个配置类进行自动花配置，并将配置类中的相关Bean文件提取出来放入公共命名空间）

### 手动实现一个starter

实现一个starter关键的一部就是要实现config类

```java
@Configuration
@EnableConfigurationProperties(MyconfigProperties.class)//允许这个类进行自动转配并且导入配置文件属性
@ConditionalOnClass(UseMyConfig.class)   // 指定进行加载的时候必须要在classpath中有UseMyconfig类
@ConditionalOnProperty(prefix = "myconfig",value = "enable",matchIfMissing = true)  //指定在加载的时候，配置文件必有要有myconfig这个配置参数
public class MyconfigAutoConfig {
    @Autowired
    private MyconfigProperties myconfigProperties ;
    @Bean
    @ConditionalOnMissingBean(UseMyConfig.class)  // 指定在类不存在的时候进行生成这个类
    public UseMyConfig useMyConfig(){
        UseMyConfig myConfig = new UseMyConfig();
        myConfig.setName(myconfigProperties.getName());
        myConfig.setPassword(myconfigProperties.getPassword());
        System.out.println(myConfig.getName()+' '+myConfig.getPassword());
        return myConfig;
    }
}
```

参数导入类：使用这个类就是为了在上面的生成bean的环节中动态的进行导入相关的参数

```java
package com.example;
 
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;
 
@ConfigurationProperties(prefix = "myconfig")
public class MyconfigProperties {
    private String name;
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
}
```

生成的javabean ， 在springboot中实现动态的身成相关的各种配置参数注入类型,注意这个使用了@ConfiguurationProperties 注解的这个类 ，这个类不单单提供了属性的自动注入功能还提供了，对外面暴露配置文件信息的功能

```java
package com.example;
 
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;
 
@ConfigurationProperties(prefix = "myconfig")
public class MyconfigProperties {
    private String name;
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
}
```

接下来就可以在使用maven打包成jar包，进行发布，注意坑点，必须打成jar包，其次要关闭spring boot的maven插件，因为这个插件会强制将 必有要存在main方法否则将会导致相关的mvn install失败

其他类尽心引用：通过上面的分析我们已经知道类，spring boot 进行相关的配置的时候其实是通过一个spring.factories 配置文件进行相关的配置的，所以，当我们进行自定一配置的时候需在resouce文件夹下新建METE-INF/spring.factories 文件，导入自己尽心的相关配置

![](blogimg/springboot/4.png)

```properties
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
  com.example.springbootstartmystart.MyconfigAutoConfig
```

> 其他class类

```java
@RestController
@SpringBootApplication
@PropertySource({"classpath:application.yml"})
@ConfigurationProperties(prefix = "auther")
public class MydemoApplication {
	public String getName() {
		return name;
	}
	@Autowired
	public UseMyConfig useMyConfig;
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
		return this.name+" :"+this.password+" "+useMyConfig.getName()+" "+useMyConfig.getPassword();
	}
	public static void main(String[] args) {
		SpringApplication.run(MydemoApplication.class, args);
	}
}
```

