> AOP 是一种新的属性配置方法这种方法不同与OOP，不是使用继承的方法来增强相关的参数而是使用横向的切面编程的方法来进行相关增强的

### spring中使用xml进行配置的方法

切面类

> 注意： around方式的方法需要第一参数为ProceedingJoinPoint 类型 ，当需要接受参数的时候需要在 exection方法中进行相关的配置

```java
import org.aspectj.lang.ProceedingJoinPoint;
public class CutClass {
	public void before() {
		System.out.println("before: this is before");
	}
	public void afterTwo(int number, String string) {
		System.out.println(" this is after two " + number + " " + string);
	}
	public void after() {
		System.out.println("this is after");
	}
	public void Arround(ProceedingJoinPoint joinPoint) throws Throwable {
		System.out.println("this is start around");
		Object[] objects = joinPoint.getArgs();
		joinPoint.proceed(objects);
		System.out.println("this is after around");
	}
	public void AfterReturn(int number) {
		System.out.println("AfterReturn :" + number);
	}
	public void AfterThrow(Exception exception) {
		try {
			System.out.println("this is exception:" + exception);
		} catch (Exception e) {
			// TODO: handle exception
		}
	}
}
```

被切入类

```java
public class BeCutClass {
	public void say() {
		System.out.println("this is say");
	}
	public int sayHasReturn() {
		return 123;
	}
	public void sayHasEx() {
		int a=1/0;
	}
	public void HasPress(int number,String string) {
		System.out.println("this is sayHasOress"+" number "+number+" string:"+string);
	}
}
```

##### xml配置文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:aop="http://www.springframework.org/schema/aop"
	xmlns:context="http://www.springframework.org/schema/context"
	xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
		http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.3.xsd
		http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-4.3.xsd">
	<bean id="cutpoint"  class="b_spring.c_springAOP.CutClass"></bean>	
	<bean id="becutpoint" class="b_spring.c_springAOP.BeCutClass"></bean>
	<aop:config>
		<aop:pointcut expression="execution(* b_spring.c_springAOP.BeCutClass.say*(..) )" id="pointCurForNoPress"/>
		<aop:pointcut expression="execution(* b_spring.c_springAOP.BeCutClass.HasPress(..))" id="pointCurForPress"/>
		<aop:aspect ref="cutpoint">
			<aop:before method="before" pointcut-ref="pointCurForNoPress"/>
			<aop:after method="after" pointcut-ref="pointCurForNoPress" />
			<aop:after-returning method="AfterReturn" pointcut-ref="pointCurForNoPress" returning="number"/>
			<aop:after-throwing method="AfterThrow" pointcut-ref="pointCurForNoPress" throwing="exception"/>
			<aop:around method="Arround" pointcut-ref="pointCurForPress"></aop:around>
			<aop:after method="afterTwo" pointcut="execution(* b_spring.c_springAOP.BeCutClass.HasPress(..)) and args(number,string)" arg-names="number,string"/>
		</aop:aspect>
	</aop:config>
</beans>
```

##### 测试类

```java
@org.junit.Test
public void test() {
	BeCutClass class1 = context.getBean("becutpoint", BeCutClass.class);
	class1.say();
	class1.sayHasReturn();
	class1.HasPress(123, "jjj");
	class1.sayHasEx();
}
```

##### 输出结果

```java
this is before
this is say
this is after
this is before
AfterReturn :123
this is after
this is start around
this is sayHasOress number 123 string:jjj
this is after two 123 jjj
this is after around
this is before
this is exception:java.lang.ArithmeticException: / by zero
this is after
```

### 使用注解方法进行配置

#### 增强类

```java
import org.springframework.stereotype.Component;
import n_springAOP.noconfig.FatherBean;
@Component
public class AopBeanOne implements FatherBean{
	//--这里面 左面的小图标消失的启示-当实现接口的时候 spring框架自动使用jdk代理,没有使用接口的时候使用cglib代理
	//当使用使用了接口的时候aop增强的不是接口中的方法会导致spring的插件不识别但是spring的代码没有出现错误 说明是spring框架中使用的
	//了自动的判断方法
	@Override
	public String say(String one,String two){
		System.out.println("i'am aopbeanone");
		return "beanOneReturn"+one+two;
	}
} 
```

#### 切面类

```java
//定义切面类
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.After;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.AfterThrowing;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;
//使用这个注解表明这个类是一个切面类 用来给其他的一些类进行增强处理
//spring的aop主要用来增强方法
@Component//注意在不使用配置文件的时候要进行aop时候必须使用这条注解将所需要的方法放进spring容器中
@Aspect
public class MyAop implements Ordered{
	//aop增强表示在这个方法调用之前进行处理的过程
	//！！！注意在切入的点上还可以添加一个&&args(one,two)或者&&args(one,two,..)-前者表示匹配存在两个参数的方法并且讲参数传入进来-后一个表示匹配两个参数及其以上的方法
	@Before(value="execution(* n_springAOP.noconfig.aopbeanOne.*.*(..))&&args(one,two)")
	public void methodForBefore(String one ,String two){
		System.out.println("i am is aop before"+one+two);
	}
	//在aop增强的方法返回后进行的操作 returning 属性将会被动态的添加到Object参数中
	//这里使用了定义切入点方法 切人的函数在必要的时候可以是全限定名称
	@AfterReturning(returning="returning",pointcut="myPintCut()")
	public void methodForAfterReturning(Object returning){
		System.out.println("this is afterReturning return is "+returning);
	}
	//这个增强表示在aop的方法抛出异常之后进行调用的方法  throwing 的属性将会动态的添加进ext参数中
	@AfterThrowing(throwing="ext" ,value="execution(* n_springAOP.noconfig.aopbeanOne.*.*(..))")
	public void methodAfterThrowing(Throwable ext){
		
	}
	//这个增强表示在框架的执行过程中进行增强处理 之一使用Around 运行时增强的时候第一个参数必须是ProceedingJoinPoin类型
	//当调用ProceedingJoinPoint参数的proceed()方法的时候才会动态的调用需要增强的方法 里面的参数可以传递一个object[]的对象表示相关的调用方法的参数
	//这个参数存在一个getArgs方法 返回一个 object[] 表示调用时候传递进来的参数
	//这个增强可以出处理增强方法处理的时机 
	@Order(1)
	@Around(value="execution(* n_springAOP.noconfig.aopbeanOne.*.*(..))")
	public String methodForAround(ProceedingJoinPoint jp) throws Throwable{
		Object[] oo=jp.getArgs();		//返回调用的时候传递进来的参数
		jp.getTarget();					//返回进行aop增强的原始类
		jp.getTarget();					//返回进行aop增强的原始类
		System.out.println("This is Around begin....");
		String a=(String) jp.proceed(oo);
		System.out.println("this is Around end.....");
		return a;
	}
	//当多个切面作用在一个方法上的时候使用这个方法将会返回一优先级数值越小优先级高
	//除此之外还能使用注解定义优先级--使用继承接口的方法只是对全局进行定义的
	@Override
	public int getOrder() {
		// TODO Auto-generated method stub
		return 1;
	}
	@After("execution(* n_springAOP.noconfig.aopbeanOne.*.*(..))")
	public void MethodAfter(){
		System.out.println("this is after");
	}
	//切入点的使用相当的繁杂所以我们使用函数表示切入点 -详细情况见上面的afterReturning方法
	@Pointcut(value="execution(public * n_springAOP.noconfig.aopbeanOne.*.*(..))")
	public void myPintCut(){}
	//  execution(modifier-pattern? ret-type-pattern declaring-type-pattern? name-pattern(param-pattern) throws-pattern?)
	// modifier-pattern-指定方法的修饰符(public等) 支持通配符 可省略
	// ret-type-pattern -- 返回值类型 支持通配符
	//declaring-type-pattern- 方法所属的全限定类名称 可以使用通配可省略
	// name-pattern 方法的名称 可使用通配符*
	//(param-pattern) 表示接受的形参列表 可以使用 *-匹配一个参数 ..匹配多个参数 或者使用基本类型
	//表达式的扩展属性 	args 指定参数是指定类型的
	//					target 指定目标对象是指定类型的
	//主属性和扩展属性的链接符(连接不同的函数) && 同时满足匹配 || 只满足一个或者多个匹配 ! 不满足匹配
}
```

> 切入点表达式 支持如下的几个,with(examples.chap03.Horseman) 指定类名称的所有方法,通过类名指定，同时包含所有子类target(examples.chap03.Horseman),args(java.util.String) 指定参数(如果使用的不是基本类型,那就会匹配对应的变量名称),annotation(org.springframework.transaction.annotation.Transactional) 指定标注了指定的注解的方法,这些参数必须是全限定名称

#### xml文件配置文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:aop="http://www.springframework.org/schema/aop"
	xmlns:context="http://www.springframework.org/schema/context"
	xmlns:tx="http://www.springframework.org/schema/tx"
	xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
		http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.3.xsd
		http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-4.3.xsd
		http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-4.3.xsd">
	<context:component-scan base-package="n_springAOP.noconfig"></context:component-scan>
	<!-- 不进行注册bean而是让注册了的bean进行相关的数据添加 -->
	<context:annotation-config></context:annotation-config>
	<!-- 这个标记表示启用注解形式的aop编程风格 -->
	<!-- 注意使用aop的时候需要添加 aspectj的库 -->
	<aop:aspectj-autoproxy></aop:aspectj-autoproxy>
	<!-- 如果不使用上面的aop配置文件需要启用这个bean后置处理器来为spring 框架中的所有bean -->
	<!--
		<bean class="org.springframework.aop.aspectj.annotation.AnnotationAwareAspectJAutoProxyCreator"></bean>
    -->
</beans>
```

> 注意上面的配置方法其实可以替换成如下的方法

```java
@Configurable //使用注解模式
@ComponentScan //自动扫描路径
@EnableAspectJAutoProxy  // 启动aop支持
public class ConfigApp{
	............
}
```



> 注意:完整的AspectJ切入点语言支持Spring中不支持的其他切入点指示符。这些是：call, get, set, preinitialization, staticinitialization, initialization, handler, adviceexecution, withincode, cflow, cflowbelow, if, @this，和@withincode


> 注意: 使用注解的缺点,支持“singleton”方面的实例化模型，并且不可能组合使用XML声明的命名切入点。使用XML方法的缺点是您无法通过组合这些定义来定义切入点。

> 注意: spring不支持final的调用,应为final不支持覆盖

> 注意当在代理中使用方法的方法的时候不能使用代理自己的方法,因为解析器会使用this.xxx()来运行 而不是使用 proxy来运行,所以应该使用如下的方法进行代理

> 注意: 使用的表达式格式 - execution(modifiers-pattern? ret-type-pattern declaring-type-pattern?name-pattern(param-pattern) throws-pattern?)

```java
public class SimplePojo implements Pojo {
    public void foo() {
        // this works, but... gah!
        ((Pojo) AopContext.currentProxy()).bar();
    }
    public void bar() {
        // some logic...
    }
}
```
