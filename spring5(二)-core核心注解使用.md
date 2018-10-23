### spring 注解配置方法


> 所谓零配置，并不是说一点配置都没有了，而是配置很少而已。通过约定来减少需要配置的数量，提高开发效率。更厉害的是spring boot

xml配置文件

```xml
<!-- base-package-指定扫描的包   resource-pattern-粗过滤 -->
<context:component-scan base-package="b_spring.a_spring的bean的依赖注入.bean" resource-pattern="web*/">
        <!-- 可以指定过滤指定的注解或者使用正则表达式 -->
	<context:exclude-filter type="regex" expression="*.*jkl"/><!-- 不作为过滤器 -->
	<context:include-filter type="annotation" expression=".*jkl"/><!-- 作为过滤器 -->
</context:component-scan>
```   


   
注意：必须还要加上如下的注解，这个注解的作用是开启@Autowired，@ Resource ，@ PostConstruct，@ PreDestroy，@PersistenceContext，@Required 各种支持从而不需要在xml文件中配置相关的类

```xml
<context:annotation-config></context:annotation-config>
```

该隐式注册的后处理器包括 AutowiredAnnotationBeanPostProcessor， CommonAnnotationBeanPostProcessor， PersistenceAnnotationBeanPostProcessor，以及前述 RequiredAnnotationBeanPostProcessor



#### spring 类上的注解

这几个注解在使用上其实是一样只是使用不同的名称来体现可读性

```java
@Controller(value="oneinfo")
@Service
@Repository
@Component
@Configurable    Autowire.NO;//等指定是否支持自动装配
```
------------
####  类属性的注解

```java
@Scope("prototype")//---设置bean对象使用的作用域
@ApplicationScope //作用域简写
@RequestScope //作用域简写
@SessionScope //作用域简写
@DependsOn({"beanTwo"})//相当于xml文件中配置的dependson属性表示依赖关系
@Lazy(true)//表示函数是否进行延迟加载 注意可以修饰@Bean
@Required   //这个注解只能放在setXxxx()方法上，spring检测set方法有没有使用，如果没有使用将会抛出异常
@order和@Priority //见下面啊autowrite方法  指定自动装配时候的优先级别
@Primary //进行这个注解的bean将会优先的进行注入,多个就按照后面的覆盖前面的
@DependsOn //在配置类(configration)中可以指定相关的配置方法
```
------------
@Scope注解 引申:

这个注解存在一个特殊的属性proxyMode

```java
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Scope {

	@AliasFor("scopeName")
	String value() default "";

	@AliasFor("value")
	String scopeName() default "";

	ScopedProxyMode proxyMode() default ScopedProxyMode.DEFAULT;
}
```

这个属性相当于 <aop:scoped-proxy/> 这个属性 不过使用的更加方便, 其中的ScopedProxyMode 提供了三种属性 DEFAULT 默认值(使用cglib代理,详单于CLASS_TYPE属性),NO不进行代理(作用于控制取决于父辈),INTERFACE(使用jdk代理),CLASS_TYPE(使用cglib代理)

------------
#### 类中元素上的注解

```java
@Resource(name="beanTwo")//使用这个注解相当于在框架中使用ref  参数可以为空首先是使用byname匹配法如果没有匹配到将会使用bytype匹配法
//注意 resource这个方法如果使用方法上或者参数上时将会使用参数的名称进行自定装配（但是要注意开启java的参数名称保留的编译选项）
@Autowired//将方法中所有的参数都默认使用bytype模式进行自动的依赖注入  找不到type对应的bean或者存在多个bean都会抛出异常，如果制定了required=false的时候将不会抛出异常。
//该注解可以使用在变量 set 或者普通方法上，他会自动的将相关的属性注入进去，如果有多个匹配，可以使用list，数组，set，map进行接收，否则将会报错
@Qualifier("beanTwo")//用来和autowired连用 表示使用自动转配并且指定相关的bean名称进行自动的装配-！！这个注解同样可以注解在方法的参数上
@Primary // 调整多个多个候选项时候autowirte的注入方式
```
@Autowired 使用方法引申 ：这个注解可以使用在变量 set 或者普通方法上，他会自动的将相关的属性注入进去，如果有多个匹配，可以使用list，数组，set，map进行接收，否则将会报错，如果想要诸如的bean按照顺序，可以使用@order或者@Priority在bean上指定顺序

------------

#### 类中方法上的注解

```java
@Autowired //用于方法的自动装配
@Qualifier // 配合atutowired 使用 
// 上面这两个方法应该是应用在构造函数中的方法普通的方法在这个地方没什么有用的地方
@Nullable  //指定这个参可以为空
@NotNull // 指定这个参数不可为空
@PostConstruct//spring容器在第一次初始化之后将会调用这个方法
@PreConstruct//spring容器在卸载这个对象的时候将会调用这个方法
@PreDestroy//相当于删除的方法在使用这个方法的时候将会在销毁的时候进行回调
```

#### @Resource, @Autowired 和 @Qualifier自动注入使用

- @Resource： 默认使用name属性进行自动装配，@Resource 没有指定 name 属性，那么使用 byName 匹配失败后，会退而使用 byType 继续匹配，如果再失败，则抛出异常，将其标注在 BeanFactory 类型、ApplicationContext 类型、ResourceLoader 类型、ApplicationEventPublisher 类型、MessageSource 类型上，那么 Spring 会自动注入这些实现类的实例，不需要额外的操作。
- @Autowired 和 @Qualifier 注解执行自动装配： 
- 1. 只能是根据类型进行匹配   
- 2. 可以用于 Setter 方法、构造函数、字段，甚至普通方法，前提是方法必须有至少一个参数   
- 3. 可以用于数组和使用泛型的集合类型。然后 Spring 会将容器中所有类型符合的 Bean 注入进来。 
- 4.  标注作用于 Map 类型，将容器中所有类型符合 Map 的 value 对应的类型的 Bean 增加进来，用 Bean 的 id 或 name 作为 Map 的 key 5.@Autowired 后面增加一个 @Qualifier 标注，提供一个 String 类型的值作为候选的 Bean 的名字

```java
@Autowired(required=false)
@Qualifier("ppp")
public void setPerson(person p){}
@Autowired(required=false)
public void sayHello(@Qualifier("ppp")Person p,String name){}
```

> 5.0 新注解 使用@Nullable 可以忽略@Autowired 应在函数上面的时候的参数

```java
@Autowired
public void setMovieFinder(@Nullable MovieFinder movieFinder) {
     ...
}
```
> @Autowired对于那些众所周知的解析依赖接口：BeanFactory，ApplicationContext，Environment，ResourceLoader， ApplicationEventPublisher，和MessageSource。这些接口及其扩展接口（如ConfigurableApplicationContext或ResourcePatternResolver）会自动解析，无需特殊设置。

> @Autowired，@Inject，@Resource，和@Value注释由Spring处理 **BeanPostProcessor实现**，也就是说不可以使用以上的注解去自动装配**BeanPostProcessor或BeanFactoryPostProcessor类型（如果有的话）**。这些类型必须通过XML或使用Spring @Bean方法明确地手动地进行配置 。

------------

**5,0新注解 使用@Primary微调基于注释的自动装配**

这里指定了相关的java配置类返回的参数

```java
public class MovieConfiguration {
    @Bean
    @Primary
    public MovieCatalog firstMovieCatalog() { ... }
    @Bean
    public MovieCatalog secondMovieCatalog() { ... }
    // ...
}
```
在xml文件中进行如下配置
```xml
 <bean class="example.SimpleMovieCatalog" primary="true">
     <!-- inject any dependencies required by this bean -->
</bean>
```

#### @Qualifier注解 为spring 容器自动装配提供更多选项

这个注解可以进行派生

```java
@Target({ElementType.FIELD, ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
@Qualifier
public @interface MovieQualifier {
    String genre();
    Format format();// 注意fromat是一个枚举
}

public enum Format {
    VHS, DVD, BLURAY
}
```

> 可以让autowirte和自定义的genre动态的进行连用，从而提高自动装配的灵活性

```java
public class MovieRecommender {
    @Autowired
    @MovieQualifier(format=Format.VHS, genre="Action")
    private MovieCatalog actionVhsCatalog;
}
```

或者使用xml进行配置，qualitier 这个标签的attribute中使用kye，value唯一定位一个属性如果，自定义注解的时候没有相关的内部属性，可以直接使用type来唯一的限定一个标记

```xml
<bean class="example.SimpleMovieCatalog">
    <qualifier type="MovieQualifier">
        <attribute key="format" value="VHS"/>
        <attribute key="genre" value="Action"/>
    </qualifier>
    <!-- inject any dependencies required by this bean -->
    <bean class="example.SimpleMovieCatalog">
        <qualifier type="Offline"/>
        <!-- 表示有一个注解名字就是Offine -->
    </bean>
</bean>
```

#### @Autowrite注解关联范型（模糊类型增强）举例

javabean

```java

public class User implements Serializable {
    private Long id;
    private String name;
}
public class Organization implements Serializable {
    private Long id;
    private String name;
}
public abstract class BaseRepository<M extends Serializable> {
    public void save(M m) {
        System.out.println("=====repository save:" + m);
    }
}
@Repository
public class UserRepository extends BaseRepository<User> {
}
@Repository
public class OrganizationRepository extends BaseRepository<Organization> {
}
```

新service

```java
public abstract class BaseService<M extends Serializable> {
    @Autowired
    protected BaseRepository<M> repository;
    public void save(M m) {
        repository.save(m);
    } }
@Service
public class UserService extends BaseService<User> {
}
@Service
public class OrganizationService extends BaseService<Organization> {
}
```

旧service

```java
public abstract class BaseService<M extends Serializable> {
    private BaseRepository<M> repository;
    public void setRepository(BaseRepository<M> repository) {
        this.repository = repository;
    }
    public void save(M m) {
        repository.save(m);
    }
}
@Service
public class UserService extends BaseService<User> {
    @Autowired
    public void setUserRepository(UserRepository userRepository) {
        setRepository(userRepository);
    }
}
@Service
public class OrganizationService extends BaseService<Organization> {
    @Autowired
    public void setOrganizationRepository(OrganizationRepository organizationRepository) {
        setRepository(organizationRepository);
    }
}
```

1. 范型注入改进

- 改进：不需要在set方法上在进行一次封装，直接使用@Autowrite进行注入就好了

2. 提供map和list注入

```java
@Autowired
private Map<String, BaseService> map;
@Autowired
private List<BaseService> list;
```

> map会这样注入：key是bean名字；value就是所有实现了BaseService的Bean

> list会这样注入：这样会注入所有实现了BaseService的Bean；但是顺序是不确定的，如果我们想要按照某个顺序获取；在Spring4中可以使用@Order或实现Ordered接口来实现（指定加载的顺序）



------------

**spring5.0 的增强注解 @AliasFor** 这个注解实现了注解继承中的属性继承,从此 spring组合注解不在像之前需要在继承的注解的中写入值,而是可以在注解中进行自定义的操作

```java
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Scope(WebApplicationContext.SCOPE_SESSION)
public @interface SessionScope {
	/**
	* 使用继承注解, 继承
	*/
    @AliasFor(annotation = Scope.class)
    ScopedProxyMode proxyMode() default ScopedProxyMode.TARGET_CLASS;

}
```
这个注解还有一些属性 比如 annotation 哪一个接口(注意这个接口必须是继承的否则会出错) value和attribute(这两个属性表示指定继承注解中哪一个属性,如果没有那就和指定的方法名称同名)

------------

#### 生命周期控制
```java 
@PostConstruct//spring容器在第一次初始化之后将会调用这个方法
@PreConstruct//spring容器在卸载这个对象的时候将会调用这个方法
@PreDestroy//相当于删除的方法在使用这个方法的时候将会在销毁的时候进行回调
```

### 配置类注解@Configuration

>AnnotationConfigApplicationContext

和使用xml进行配置的方法不同,使用configuration基于java配置的时候需要使用这个context,这个context可以在new传入几个javabean,每一个javabean将会按照顺序的进行配置,或者不传入使用手动注册

> 使用配置文件的方法只是一种简单的方法,这种方法无法使用xml中的模版依赖这种特性,spring不知用cglib这种代理,而是用一种类似工厂方法的方式将需要的bean注入到容器中.

```java
ApplicationContext ctx = new AnnotationConfigApplicationContext(MyServiceImpl.class, Dependency1.class, Dependency2.class);
MyService myService = ctx.getBean(MyService.class);
myService.doStuff();

//手动进行相关bean的配置
AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext();
ctx.register(AppConfig.class, OtherConfig.class);
ctx.register(AdditionalConfig.class);
ctx.refresh();
MyService myService = ctx.getBean(MyService.class);
myService.doStuff();
```

#### 相关的注解

```java
@Configuration
@ComponentScan(basePackages = {"org.bean"})//扫描指定的包可以将@Component，@Repository， @Service，@Controller，或@Configuration自动的注入
@PropertySource("needpro.properties")//导入指定的配置文件，可以指定编码格式
@profile //这个属性将会检查环境和Profile中的值 是否对应,有选择性的启用Bean的配置,配置在@configuration标签中将会导致全局的效果,配置在@bean中将只对这个标签有效
@DependsOn  // 这个方法除了可以在javabean上面声明还可以子啊config类中的bean上面声明
@Bean  // 可以指定一个方法 方法的返回值就是这个bean
@Description("Provides a basic example of a bean") // 用在config配置类中bean返回的方法上,用来对相关的javaBean添加一线描述
@Import({ServiceConfig.class, RepositoryConfig.class}) // 可以 应用其他的注解的配置属性
@ImportResource("classpath:/com/acme/properties-config.xml") //加入一个配置文件
```
#### @ComponentScan 类扩展

@ComponentScan 这个直接和配置文件中的自动扫描配置相同 支持的方法有：

类型|示例表达|描述
---|---|---
annotation(包名称)|org.example.SomeAnnotation|要在目标组件中的类型级别出现的注释。
assignable(指定类)org.example.SomeClass|目标组件可分配给（扩展/实现）的类（或接口）。
aspectJ(aop 路径配置)|org.example..*Service+|要由目标组件匹配的AspectJ类型表达式。
regex(正则表达式)|org\.example\.Default.*|要由目标组件类名匹配的正则表达式。
custom|org.example.MyTypeFilter|org.springframework.core.type .TypeFilter接口的自定义实现。

例子

```java
@Configuration
@ComponentScan(basePackages = "org.example",
        includeFilters = @Filter(type = FilterType.REGEX, pattern = ".*Stub.*Repository"),
        excludeFilters = @Filter(Repository.class))
public class AppConfig {
    ...
}
```
注意上面这里有一个内部接口注解 @Filter 这个方法可以指定过滤的级别

```java
@Retention(RetentionPolicy.RUNTIME)
@Target({})
@interface Filter {
	//指定 过滤的方法 具体拥有的方法见使用xml配置文件
	FilterType type() default FilterType.ANNOTATION;

	//指定class名称的文件过滤
	@AliasFor("classes")
	Class<?>[] value() default {};
	@AliasFor("value")
	Class<?>[] classes() default {};

	//当type 为使用正则表单式等其他非class文件的方式的必须传入的方法
	String[] pattern() default {};
}
```

自定的扩展:

- 如果你不想依赖默认的bean命名策略，你可以提供一个自定义的bean命名策略。首先，实现 BeanNameGenerator 接口，并确保包含一个默认的无参数构造函数。
- 要为范围解析提供自定义策略，而不是依赖基于注释的方法，请实现 ScopeMetadataResolver 接口，并确保包含默认的无参数构造函数
- scopedProxy :当使用非单利作用域的时候,可以指定代理的方法 no ,interface ,targer_class

```java
@ComponentScan(nameGenerator = NameGenerator.class,scopeResolver = MyScopeResolver.class)
```

```java
public class genAndScope implements BeanNameGenerator, ScopeMetadataResolver {
    @Override
    public String generateBeanName(BeanDefinition beanDefinition, BeanDefinitionRegistry beanDefinitionRegistry) {
        return null;
    }
    @Override
    public ScopeMetadata resolveScopeMetadata(BeanDefinition definition) {
        return null;
    }
}
```

> xml配置方法

```xml
<beans>
    <context:component-scan base-package="org.example" scope-resolver="org.example.MyScopeResolver"/>
</beans>
<beans>
    <context:component-scan base-package="org.example"
        name-generator="org.example.MyNameGenerator" />
</beans>
```

#### @Bean 使用扩展

> 这个注解相当于 xml中的<bean>标签

在类中使用的方法

```java
@Configuration
public class AppConfig {
   	@Bean(initMethod = "init")
	@Scope("prototype")
	public TransferService transferService(AccountRepository accountRepository) {
        return new TransferServiceImpl(accountRepository);
    }
	@Bean(name = { "dataSource", "subsystemA-dataSource", "subsystemB-dataSource" })
	public Item hehe(){
		return Item();
	} 
}
```
看上面的例子, 注意
- @Bean 使用指定的方法,可以存在参数,spring将会自动的注入需要的属性,同样可以使用@Autowrite

- @Bean 注解可以指定函数的构造方法或者析构方法

- 可以指定这个并的作用域@Scope

- @Bean 中可以指定一组的名称指定别名

```java
@Bean(initMethod = "init")
@Bean(destroyMethod = "cleanup")
```
- config 类中实现javaBean的依赖可以直接的调用相关的参数,可以使用@Qualitfier使用id指定需要注入的元素，否则将使用type进行依赖的注入

```java
@Configuration
public class AppConfig {
    @Bean
    public Foo foo() {
        //这里直接生成新的元素
        return new Foo(bar());
    }
    @Bean
    public Bar bar() {
        return new Bar();
    }
    @Bean
    public TestBean protectedInstance(
            @Qualifier("public") TestBean spouse,
            @Value("#{privateInstance.age}") String country) {
        TestBean tb = new TestBean("protectedInstance", 1);
        tb.setSpouse(spouse);
        tb.setCountry(country);
        return tb;
    }
}
```

> 请注意，单个类可以@Bean为同一个bean 保存多个方法，作为根据运行时可用依赖项使用多个工厂方法的安排。这与在其他配置方案中选择“最贪婪”构造函数或工厂方法的算法相同：将在构造时选择具有最多可满足依赖项的变体，类似于容器在多个@Autowired构造函数之间进行选择的方式。

**特殊性 configuration 类 在spring内部使用的cglib方法进行构建的,导致下面的ClientDao 将不会出现数据对象的情况**

> 注意 @configuration 注解比较特殊 系统使用cglib进行初始化而component系列的使用的和xml相同的方法

```java
@Configuration
public class AppConfig {
    @Bean
    public ClientService clientService1() {
        ClientServiceImpl clientService = new ClientServiceImpl();
        clientService.setClientDao(clientDao());
        return clientService;
    }
    @Bean
    public ClientService clientService2() {
        ClientServiceImpl clientService = new ClientServiceImpl();
        clientService.setClientDao(clientDao());
        return clientService;
    }
    @Bean
    public ClientDao clientDao() {
        return new ClientDaoImpl();
    }
}
```

-----


@value 标签使用spEL 表达式进行配置

```java

@Value("这是spring的配置文件")//传入简单的string类型
private String name;
@Value("#{systemProperties['os.name']}")//使用springEl传入系统属性
private String osName;
@Value("#{T(java.lang.Math).random()*100.0}")//使用EL调用系统方法
private double randomNumber;
@Value("${book.name}")//传入配置文件中指定的参数
private String bookName;
@Value("#{book.name}")//获得指定bean的参数
private String beanINfo;
```

```java
@Bean(name = "abook") //还提供 initMethod he destroyMethod 配置文件等同于在xml中进行配置
@Scope("prototype")
@Profile("pro")  //指定返回bean执行的版本信息可以在容器启动的时候动态的导入
public Book mybook() {
   return new Book();
}
```

####  使用@Conditional注解实现更加颗粒化的控制(在springboot 自定义starter中还会有说)

之前看过了一个注解@Profile 这个注解看一下源代码

```java
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Conditional(ProfileCondition.class)
public @interface Profile {
	String[] value();
}
```

> 这个注解其实是一个组合注解,有一个重点的注解就是上面的@Conditional和传入的里面的ProfileCondition.class这个类,接下来看看这个类

```java
class ProfileCondition implements Condition {
	@Override
	public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
		MultiValueMap<String, Object> attrs = metadata.getAllAnnotationAttributes(Profile.class.getName());
		if (attrs != null) {
			for (Object value : attrs.get("value")) {
				if (context.getEnvironment().acceptsProfiles((String[]) value)) {
					return true;
				}
			}
			return false;
		}
		return true;
	}
}
```

> 这个类实现了一个Condition 接口,这个接口有一个方法matches() 通过返回false或者true来告诉spring容器要不要注入的这个bean,context 就是spring的上下文信息,我可以通过这个方法进行相关容器的配置.metadata实现了注解的相关的数据.

#### @Profile 实现环境控制

上面我们已经知道了 这个注解其实是一个Condition注解的一个子注解,他可以通过 环境来判断那些属性需要被注入的相关的属性中

注意这个方法**context.getEnvironment()** 这个方法将会将会获取系统中相关的环境信息获取出来

添加环境变量属性

1. 第一种方法, 使用context 添加相关的属性
```java
AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext();
ctx.getEnvironment().setActiveProfiles("development");
ctx.register(SomeConfig.class, StandaloneDataConfig.class, JndiDataConfig.class);
ctx.refresh();
```

2. spring.profiles.active 使用配置文件配置属性

使用java 的启动参数 -Dspring.profiles.active="profile1,profile2"

建议使用注解的方法 ,@PropertySource("classpath:/com/myco/app.properties")
ctx.getEnvironment().setActiveProfiles("profile1", "profile2");

```java
@Configuration
@PropertySource("classpath:/com/myco/app.properties")
public class AppConfig {
    @Autowired
    Environment env;
    @Bean
    public TestBean testBean() {
        TestBean testBean = new TestBean();
        testBean.setName(env.getProperty("testbean.name"));
        return testBean;
    }
}
```

#### 使用value 实现特殊的表达式注入

xml文件

配置文件

```properties
jdbc.properties
jdbc.url = JDBC：HSQLDB：HSQL：//本地主机/ XDB
jdbc.username = SA
jdbc.password =2222
```
```xml
<beans>
    <context:property-placeholder location="classpath:/com/acme/jdbc.properties"/>
</beans>
```

```java
@Configuration
@ImportResource("classpath:/com/acme/properties-config.xml")
public class AppConfig {
    @Value("${jdbc.url}")
    private String url;
    @Value("${jdbc.username}")
    private String username;
    @Value("${jdbc.password}")
    private String password;
    @Bean
    public DataSource dataSource() {
        return new DriverManagerDataSource(url, username, password);
    }
}

```

#### 一个例子

```java
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import javax.annotation.Resource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Controller;
@Controller
class Demo1 {
	@Autowired
	@Qualifier("itemService")
	private ItemService itemService;
	@Resource(name = "itemService")
	private ItemService itemService2;
	private String item = "sdfdf";
	public String getItem() {
		return item;
	}
	public void setItem(String item) {
		this.item = item;
	}
	@PostConstruct
	public void init() {
		System.out.println("start");
	}
	@PreDestroy
	public void destory() {
		System.out.println("end");
	}
}
```
> 注意:BeanPostProcessor和BeanFactoryPostProcessor 应该声明为static @Bean方法 , 防止processor生效之前有数据被初始化

### spring lookup 方法注入注解@Lookup

具体的功能和xml相同，LookUp提供了两种参数当有参数的时候将会自动寻找容器中beanid对应参数的bean，否则将会基于返回类型进行添加

```java
public abstract class CommandManager {

    public Object process(Object commandState) {
        Command command = createCommand();
        command.setState(commandState);
        return command.execute();
    }

    @Lookup("myCommand")
    protected abstract Command createCommand();

    @Lookup
    protected abstract MyCommand createCommand();
}
```