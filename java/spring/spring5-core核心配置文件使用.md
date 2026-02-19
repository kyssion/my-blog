### 依赖注入和控制反转

IOC   inversion of control  控制反转

DI   Dependency Injection  依赖注入

#### 依赖注入

当然是某个对象依赖于IoC/DI的容器，对象需要IoC/DI的容器来提供对象需要的外部资源，IoC/DI的容器 注入 某个对象并且注入某个对象所需要的外部资源，由IoC/DI的容器来控制对象了，根本上是控制对象实例的创建

#### 控制反转

如果要在A里面使用C，你会怎么做呢？当然是直接去创建C的对象，也就是说，是在A类中主动去获取所需要的外部资源C，这种情况被称为正向的。那么什么是反向呢？就是A类不再主动去获取C，而是被动等待，等待IoC/DI的容器获取一个C的实例，然后反向的注入到A类中


### spring IOC bean 配置文件

> 注意：不使用构造注入的时候，将会使用setter注入所以必须提供setter函数

```java
1. bean标签就是计入进spring bean工厂中的类 属性 id 是他的名字 class是,底层进行 class 反射的类底层默认使用的反射生成实例 所以 bean必须有无参的构造函数
    相关参数:
	id - 属性的名字-不能重复
	class - 属性的实现类
	parent - 指的是这个bean 要将xml文件中那个bean的标签加入进来，通常和abstract标记连用,继承的属性子类将不能继承父类的depends-on autowire singleton scope lazy-init属性
	abstract - spring容器将不会尝试对他进行单例话而只是用来作为模板用在parent的属性上
	autowrite（会覆盖显示自动装配） - bean对其bean的引用可以自动进行，而不一定用ref=的方式显式声明，有五种表示方法:
		- no  byname-根据注入的属性名（set方法去掉set小写首字- 母）称自动的注入相关的bean的id
		- bytype-查找同名后者同类型的属性超过两个会报错
		- constructor - 使用构造器中的参数类型进行匹配  需要和constructor（使用构造注入的时候相互配合）
	autowirte-candidate- 在bean的自动装配(autowrite)方法中是否忽略这个方法
	depend-on 表示这个方法的实例化优先于那个实例-强制初始化bean实例
	name - 表示这个属性的别名
	lazy-init - 表示spring框架将会进行延迟加载bean方法-（创建的时候不会调用 set方法进行实例化操作）使用的时候才进行创建
	scope-指明bean实例化的时候使用的模式 
		- singleton-单利模式 单例模式相比较prototype 速度要快的多
		- prototype-模版模式 request-对于一次request请求
		- request作用域的bean实例只生成一个实例
		- session -对于一次session session作用域将只生成一次请求
	factory-method 指定spring的加载方式是使用工厂方法的时候调用这个工厂方法中的那个类实现相关的方法
	factory-bean 指定相关的工厂方法进行相关的配置
	destroy-method  指定销毁的方法
	init-method 指定初始化的方法
	profile-这个属性将会检查环境和Profile中的值 是否对应,有选择性的启用Bean的配置,配置在beans 中将会导致全局的效果,配置在bean中将只对这个标签有效
2.property 是要进行依赖注入 的成员变量
		name表示变量名称 
		ref表示要注入的其他bean 实例  （idref：不知道为啥存在感觉没用）
		value 表示要进行注入的基本类型 注意不能注入自己定义的变量 这个可以传入多个值，自动变成list
		     	注意在注入的时候可以使用复合属性名称比如：（此特性针对对象，并且使用保证具有set方法和不为空）
				 	<property name="fred.bob.sammy" value="123" />
		子标签 ：list set mpa orops - 分别对应 List，Set，Map，和Properties
		子标签 ：null - 设置空值 （如果使用“”还是会设置成“”）
3.spring框架默认使用无参数的构造器 如果想使用有参数的构造器需要使用构造器注入
	constructor-agr-标签中可以传入几个参数 
		- index 	表示第几个参数
		- name 	表示参数的名称 ！！！ 注意如果jdk沒有使用保留参数名称的编译选项的时候
					需要使用 @ConstructorProperties({"years", "ultimateAnswer"})显示的表明变量名称
		- ref 	同上
		- value  	同上
		- type 	制定参数的类型，可以使用非基本类型
4. beans 标签 表示一堆bean的集合 里面的属性表示是应用于所有有关这个的方法
	- default-lazy-init
	- default-merge -制定beans下所有的默认合并行为
	- default-autowire
	- dafault-autowire-condiadates
	- default-init-method - 所有bean的默认初始化行为
	- default-destroy-method - 所有bean的默认回收方法
	- profile-这个属性将会检查环境和Profile中的值 是否对应,有选择性的启用Bean的配置,配置在beans 中将会导致全局的效果,配置在bean中将只对这个标签有效
5. 其他标签
    alias - 重命名标签
        - name - 原始名称
		- alias -  重命名之后的名称
```

### spring 自动配置内部类

#### 内部类注入方式一：添加内部类默认构造函数参数

非静态的内部类默认的构造函数有一个参数，这个参数指向其外部类的实例，所以我们需要给此内部类的bean添加constructor-arg节点，并指向外部类即可，配置文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans
           http://www.springframework.org/schema/beans/spring-beans.xsd">
	<bean class="cn.outofmemory.spring.Person" id="person">
		<property name="hands">
			<list>
				<bean class="cn.outofmemory.spring.Person$Hand">
					<constructor-arg ref="person"></constructor-arg>
					<property name="strength" value="90"/>
				</bean>
			</list>
		</property>
	</bean>
</beans>
```

#### 内部类注入方式二：将内部类修改为static

这个使用不需要访问外部，所以就和外部类型等同了

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans
           http://www.springframework.org/schema/beans/spring-beans.xsd">
	<bean class="cn.outofmemory.spring.Person" id="person">
		<property name="hands">
			<list>
				<bean class="cn.outofmemory.spring.Person$Hand">
					<property name="strength" value="90"/>
				</bean>
			</list>
		</property>
	</bean>
</beans>
```

> 注意spring 声明内部类的时候需要特殊处理,需要通过外部类$内部类名来使用

```xml
<bean id="serviceAware" class="com.qing.platform.schedule.scheduling.impl.Utils$ServiceAware" />
```


#### parent abstract和list  map set Properties   属性使用

```xml
<bean id="baseBeanForDemoOne" abstract="true">
    <description>联系spring的使用使用抽象类进行操作</description>
    <property name="string" value="this is string"></property>
    <property name="number" value="123"></property>
</bean>
<!-- parent list  map  属性使用 -->
<bean id="demoOne" class="b_spring.a_spring的bean的依赖注入.bean.DemoBeanOne" parent="baseBeanForDemoOne">
    <property name="items"><!-- 使用list方法进行注入  -->
        <list value-type="java.lang.String">
            <value>one</value>
            <value>two</value>
            <value>three</value>
            <value type="java.lang.String">four</value>
        </list>
    </property>
    <property name="itemMap"><!-- 使用map方法进行注入 -->
        <map key-type="java.lang.String" value-type="java.lang.Integer">
            <entry key="one" value="123"></entry>
            <entry key="two" value="223"></entry>
        </map>
    </property>
    <property name="set">
        <set value-type="java.lang.String">
            <value>ddddd</value>
        </set>
    </property>
    <property name="properties">
        <props>
            <prop key="pro">eeee</prop>
        </props>
    </property>
</bean>
```

```java
import java.util.ArrayList;
import java.util.HashMap;
public class DemoBeanOne {
## 	//注意使用spring的set注入方法的时候必须提供set方法
	private  String string;
	private  int number;
	private ArrayList<String> items;
	private HashMap<String, Integer> itemMap;
	private Set<String> set;
	private Properties properties;
	//注意使用spring的set注入方法的时候必须提供set方法
	.......get和set的方法.......
}
```

parent 和 abstract 只是相当于在配置文件中指定一个参数的继承方法，相当于实现一个参数的模板，而集合类型的配置，例子中使用了基本类型使用value标签进行配置其实和可以传入bean的引用。

```xml
<property name="list">
    <list value-type="bean.People">
        <!--传入制定的bean的名称-->
        <ref bean="jjj"></ref>
    </list>
</property>
<property name="map">
   <map key-type="java.lang.String" value-type="bean.People">
        <entry key="one" value-ref="jjj"></entry>
    </map>
</property>
<property name="set">
    <set value-type="bean.People">
        <ref bean="jjj"></ref>
    </set>
</property>
```

#### 获取bean容器

使用applicationContext 获得 spring 容器  而 BeanFactory是 application的父类   二者区别

applicationContext接口,它由BeanFactory接口派生而来，因而提供BeanFactory所有的功能。ApplicationContext以一种更向面向框架的方式工作以及对上下文进行分层和实现继承，ApplicationContext包还提供了以下的功能：

- MessageSource, 提供国际化的消息访问
- 资源访问，如URL和文件
- 事件传播
- 载入多个（有继承关系）上下文 ，使得每一个上下文都专注于一个特定的层次，比如应用的web层

其他区别：

- BeanFactroy采用的是延迟加载形式来注入Bean的，即只有在使用到某个Bean时(调用getBean())，才对该Bean进行加载实例化，这样，我们就不能发现一些存在的Spring的配置问题。而ApplicationContext则相反，它是在容器启动时，一次性创建了所有的Bean。这样，在容器启动时，我们就可以发现Spring中存在的配置错误。 
- BeanFactory和ApplicationContext都支持BeanPostProcessor、BeanFactoryPostProcessor的使用，但两者之间的区别是：BeanFactory需要手动注册，而ApplicationContext则是自动注册

```java
ClassPathXmlApplicationContext applicationContext = new ClassPathXmlApplicationContext("/a_bean.xml");
ApplicationContext applicationContext = new  FileSystemXmlApplicationContext("a_bean.xml");
```

#### autowrite  + autowirte-candidate  lazy-init（spring只用在使用的时候才会加载bean）

> 通过 名称或者类型自动装载但是要注意一个问题就是唯一性（姓名的唯一性和类型的唯一性），注意，在xml中使用autowrite的时候如果使用的list集合就可以出现相同的类型的情况，spring会将所有的正确的类型注入到集合中

autowrite : 只用自动装配的方法
autowrite-candidate：忽略自动装配（也就是是说spring在查找可自动装配的候选项时忽略这个选项，就是不能被自动装配）

```java
<bean id="demoTwo" autowire="byName" depends-on="demoOne" class="b_spring.a_spring的bean的依赖注入.bean.DemoBeanTwo"></bean>
<bean id="demoTwo2" autowire="byType" depends-on="demoOne" class="b_spring.a_spring的bean的依赖注入.bean.DemoBeanTwo"></bean>
```

#### scope

spring有 如下的作用域（在作用域内默认使用单例），表示这个对象在这一个区域的独立性（比如单例在不同的区域就是表现的不同），singleton ， prototype，request ，session ，application（servletcontext做用域），websocket后面的四种只用在使用springmvc或者进行一些配置并且使用的web应用的时候才有效，配置如下：

```xml
<web-app>
    ...
    <listener>
        <listener-class>
            org.springframework.web.context.request.RequestContextListener
        </listener-class>
    </listener>
    ...
</web-app>

<web-app>
    ...
    <filter>
        <filter-name>requestContextFilter</filter-name>
        <filter-class>org.springframework.web.filter.RequestContextFilter</filter-class>
    </filter>
    <filter-mapping>
        <filter-name>requestContextFilter</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
    ...
</web-app>
```

注意了：如果长的scope引用短的scope中的bean 将会导致短的scope在长的scope中无法随着短的scope生命周期的结束而结束，而是以长的scope作为标准，如果想要以完美的方法需要进行如下的配置，添加<aop:scoped-proxy/>

```xml
<bean id="userPreferences" class="com.foo.UserPreferences" scope="session">
    <aop:scoped-proxy/>
</bean>

<bean id="userManager" class="com.foo.UserManager">
    <property name="userPreferences" ref="userPreferences"/>
</bean>
```

这种方法让传入长的scope中的对象不是短的scope的bean而是这个短的scope的代理,使用的是cglib（aop），这个代理只随着session的创建而创建，销毁而销毁。注意cglib只能代理公有方法，所以不要调用非公有方法

也可以使用jdk代理 <aop:scoped-proxy proxy-target-class="false"/>， 这个方法将会自动的使用的jdk代理。

一个例子：
配置文件：

```xml
<bean id="demoThree" class="b_spring.a_spring的bean的依赖注入.bean.DemoBeanThree" scope="prototype" lazy-init="true">
	<property name="string" value="this is demo three"></property>
	<property name="number" value="123"></property>
	<property name="demoBeanOne" ref="demoOne"></property>
</bean>
<bean id="demoFour" class="b_spring.a_spring的bean的依赖注入.bean.DemoBeanFour" lazy-init="true">
	<property name="string" value="this is demo four"></property>
	<property name="number" value="123"></property>
	<property name="beanThree" ref="demoThree"></property>
</bean>
```

javabean：

```java
public class DemoBeanThree {
	private String string;
	private int number;
	private DemoBeanOne demoBeanOne;
	.....get 和 set 方法
}
public class DemoBeanFour {
	private String string;
	private int number;
	private DemoBeanThree beanThree;
	.....get 和 set 方法
}
```

测试类：

```java
public void testFour() {
	DemoBeanThree d= context.getBean("demoThree",DemoBeanThree.class);
	DemoBeanThree d2= context.getBean("demoThree",DemoBeanThree.class);
	DemoBeanFour dFour=context.getBean("demoFour", DemoBeanFour.class);
	DemoBeanFour dFour2=context.getBean("demoFour", DemoBeanFour.class);
	System.out.println(d==d2);
	System.out.println("-------");//注意使用原型模式注入但单例模式的时候,或者使用单例模式注入原型模式的时候，一次操作中注入的对象是相同的
	System.out.println(d.getDemoBeanOne()==d2.getDemoBeanOne());
	System.out.println("-------");
	System.out.println(dFour.getBeanThree()==dFour2.getBeanThree());
	dFour.getBeanThree().setNumber(1233);
	System.out.println(dFour2.getBeanThree().getNumber());
}
```

> 注意一个结论：注意使用原型模式注入但单例模式的时候,或者使用单例模式注入原型模式的时候，一次操作中注入的对象是相同的 ，如果想要让单例模式注入原型模式的时候取得数据为原型模式就要使用lookup方法

#### lookup method
使用lookup 方法，其实本质上就是让一个单例bean使用一个原型bean的时候，去实现这个单例bean中的一个抽象方法，让这个抽象方法返回一个单例bean

一个有抽象方法的单例bean

```java
public abstract class BeanOne {
	private BeanTwo beanTwo;
	public abstract BeanTwo getBeanTwo();
	public void say(){
		getBeanTwo().say();
	}
	public void setBeanTwo(BeanTwo beanTwo) {
		this.beanTwo = beanTwo;
	}
}
```

对应的原型bean

```java
public class BeanTwo {
	public void say(){
		System.out.println(this);
	}
}
```
main函数中的方法

```java
ApplicationContext context = new ClassPathXmlApplicationContext("bean.xml");
BeanOne beanOne1 = context.getBean("beanone",BeanOne.class);
BeanOne beanOne2 = context.getBean("beanone",BeanOne.class);
BeanOne beanOne3 = context.getBean("beanone",BeanOne.class);
beanOne1.say();
beanOne2.say();
beanOne3.say();
```

配置文件

```xml
	<bean id="beanone" class="j_spring框架出处理单例模式下的非单例成员.BeanOne">
		<lookup-method name="getBeanTwo" bean="beanTwo"/>
		<!-- spring框架在抽象类中将会自动使用动态代理实现这个抽象方法，讲指定的bean对象进行返回
				如果对象实现了借口  spring框架将会使用jdk代理 否则使用cglib代理  推荐使用接口
		 -->
	</bean>
```

输出结果

```java
i_spring框架出处理单例模式下的非单例成员.BeanTwo@5512cb5f
i_spring框架出处理单例模式下的非单例成员.BeanTwo@5bf3101d
i_spring框架出处理单例模式下的非单例成员.BeanTwo@230b9680
```
可以看出BeanTwo的结果是不同的

#### factory-method   factory-bean  constructor-arg

> 这个工厂方法并不是我们去使用的而是让spring容器使用的工厂方法，spring容器使用这个工厂方法进行实例的生成，在spring中使用构造注入的形式调用指定的工厂法，并传入属性(可以理解成使用方法作为构造函数进行注入)，引申spring也能使用构造注入但是需要提供对应的构造函数

```xml
<bean id="staticFactory" class="b_spring.a_spring的bean的依赖注入.bean.DemoBeanStaticFactory" factory-method="createBeanOne">
	<constructor-arg index="0" value="staticfactory"></constructor-arg>
	<constructor-arg index="1" value="222"></constructor-arg>
</bean>
<!-- 使用动态方法进行构建 -->
<bean id="getOne" class="b_spring.a_spring的bean的依赖注入.bean.DemoBeanFactory"></bean>
<bean id="beanfactory" factory-bean="getOne" factory-method="getDemoBeanOne">
	<constructor-arg index="0" value="beanfactory"></constructor-arg>
	<constructor-arg index="1" value="222"></constructor-arg>
</bean>
```

```java
DemoBeanFour demoBeanOne = context.getBean("staticFactory", DemoBeanFour.class);
DemoBeanFour demoBeanOne2= context.getBean("beanfactory", DemoBeanFour.class);
System.out.println(demoBeanOne.getString()+" "+demoBeanOne2.getString());
```

#### spring 生命周期管理，初始化和销毁

实现方法

1. 继承并且实现 InitializingBean，DisposableBean 接口
2. 在xml文件中bean的属性指明 destroy-method="" init-method="" 对应的方法
3. 使用注解 @PostConstruct and @PreDestroy  @PreConstruct-容器在卸载这个bean的时候将会调用的方法 

spring框架 通过BeanPostProcessor 类来实现生命周期的管理的。

引申优雅关闭spring容器

如果使用的web项目使用webapplication的时候并不需要特殊配置spring框架自动的将相关的各种配置都实现了
如果使用的是非web项目那么需要手动进行配置，通过ConfigurableApplicationContext 类进行配置，使用registerShutdownHook方法优雅停机

```java
ConfigurableApplicationContext applicationContext = 
		new ClassPathXmlApplicationContext("./bean.xml");
applicationContext.registerShutdownHook();
```

### 引申一个:使用context简化配置操作

```xml
<beans>
    <!-- picks up and registers AppConfig as a bean definition -->
    <context:component-scan base-package="com.acme"/>
    <context:property-placeholder location="classpath:/com/acme/jdbc.properties"/>

    <bean class="org.springframework.jdbc.datasource.DriverManagerDataSource">
        <property name="url" value="${jdbc.url}"/>
        <property name="username" value="${jdbc.username}"/>
        <property name="password" value="${jdbc.password}"/>
    </bean>
</beans>
```

------

### 特殊用法 metho完全替换

使用基于XML的配置元数据，您可以使用被替换的方法元素将已有的方法实现替换为已部署的bean

比如需要替换MyValueCalculator类的cmputeValue方法

> MyValueCalculator类

```java
public class MyValueCalculator {
    public String computeValue(String input) {
        // some real code...
    }
    // some other methods...
}
```

> 替换的方法需要继承MethodReplacer接口并且在xml中进行配置

```java
public class ReplacementComputeValue implements MethodReplacer {
    public Object reimplement(Object o, Method m, Object[] args) throws Throwable {
        // get the input value, work with it, and return a computed result
        String input = (String) args[0];
        ...
        return ...;
    }
}
```

```xml
<bean id="myValueCalculator" class="x.y.z.MyValueCalculator">
    <!-- arbitrary method replacement -->
    <replaced-method name="computeValue" replacer="replacementComputeValue">
        <arg-type>String</arg-type>
    </replaced-method>
</bean>
<bean id="replacementComputeValue" class="a.b.c.ReplacementComputeValue"/>
```

