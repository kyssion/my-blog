### spring事务概述

> 事物：数据库事务(Database Transaction) ，是指作为单个逻辑工作单元执行的一系列操作，要么完全地执行，要么完全地不执行。一个逻辑工作单元要成为事务，必须满足所谓的ACID（原子性、一致性、隔离性和持久性）属性

- 原子性（Atomic）（Atomicity)：事务必须是原子工作单元；对于其数据修改，要么全都执行，要么全都不执行。

- 隔离性（Insulation）(Isolation)：由并发事务所作的修改必须与任何其它并发事务所作的修改隔离。事务查看数据时数据所处的状态，要么是另一并发事务修改它之前的状态，要么是另一事务修改它之后的状态，事务不会查看中间状态的数据。

- 一致性（Consistent）(Consistency)：事务在完成时，必须使所有的数据都保持一致状态。在相关数据库中，所有规则都必须应用于事务的修改，以保持所有数据的完整性。不能只修改了一半

- 持久性（Duration）(Durability）：事务完成之后，它对于系统的影响是永久性的。该修改即使出现致命的系统故障也将一直保持。

> spring中事务的传播行为

1. PROPAGATION_REQUIRED–支持当前事务，如果当前没有事务，就新建一个事务。这是最常见的选择。

2. PROPAGATION_SUPPORTS–支持当前事务，如果当前没有事务，就以非事务方式执行。

3. PROPAGATION_MANDATORY–支持当前事务，如果当前没有事务，就抛出异常。 

4. PROPAGATION_REQUIRES_NEW–新建事务，如果当前存在事务，把当前事务挂起。 

5. PROPAGATION_NOT_SUPPORTED–以非事务方式执行操作，如果当前存在事务，就把当前事务挂起。 

6. PROPAGATION_NEVER–以非事务方式执行，如果当前存在事务，则抛出异常。

### spring中事物的隔离级别

- Serializable：最严格的级别，事务串行执行，资源消耗最大；

- repeatable READ：保证了一个事务不会修改已经由另一个事务读取但未提交（回滚）的数据。避免了“脏读取”和“不可重复读取”的情况，但是带来了更多的性能损失。

- READ COMMITTED:大多数主流数据库的默认事务等级，保证了一个事务不会读到另一个并行事务已修改但未提交的数据，避免了“脏读取”。该级别适用于大多数系统。

- Read Uncommitted：保证了读取过程中不会读取到非法数据。

### 并发中可能发生的3中不讨人喜欢的事情

- Dirty reads–读脏数据。也就是说，比如事务A的未提交（还依然缓存）的数据被事务B读走，如果事务A失败回滚，会导致事务B所读取的的数据是错误的。

- non-repeatable reads–数据不可重复读。比如事务A中两处读取数据-total-的值。在第一读的时候，total是100，然后事务B就把total的数据改成200，事务A再读一次，结果就发现，total竟然就变成200了，造成事务A数据混乱。

- phantom reads–幻象读数据，这个和non-repeatable reads相似，也是同一个事务中多次读不一致的问题。但是non-repeatable reads的不一致是因为他所要取的数据集被改变了（比如total的数据），但是phantom reads所要读的数据的不一致却不是他所要读的数据集改变，而是他的条件数据集改变。比如Select account.id where account.name=”ppgogo*”,第一次读去了6个符合条件的id，第二次读取的时候，由于事务b把一个帐号的名字由”dd”改成”ppgogo”，结果取出来了7个数据。

### spring中其中事务的传播行为-在什么时候添加事务

```
1，propagation_required如果一个事务存在，则支持当前事务，如果不存在，则创建新的事务
2，propagation_supports如果一个事务存在，则支持当前事务，如果不存在，则非事务的方法运行
3，propagation_mendatory man de chui如果一个事务存在，则支持当前事务，如果存在，则抛出异常
4，propagation_requires_new总是要开启一个新的事务，如果事务存在，将该事务挂起
5，propagation_not_supported总是非事务方法运行，并挂起所有的事务
6，propagation_never总是非事务方法运行，如果事务存在则抛出异常
7，propagation_nested某一个事务存在，则运行在一个嵌套的事务中
```

### spring中事务的使用方法

使用阿里数据库链接池进行配置，这是下面样例使用的配置文件

```shell
url=jdbc:mysql://localhost:3306/ceshi
driverClassName=com.mysql.jdbc.Driver
username=root
password=14159265jkl
filters=stat
maxActive=20
initialSize=1
maxWait=60000
minIdle=10
maxIdle=15
timeBetweenEvictionRunsMillis=60000
minEvictableIdleTimeMillis=300000
validationQuery=SELECT 'x'
testWhileIdle=true
testOnBorrow=false
testOnReturn=false
maxOpenPreparedStatements=20
removeAbandoned=true
removeAbandonedTimeout=1800
logAbandoned=true
```

> 在spring框架中，事务的实现原理：首先实现一个事务的管理类  DataSourceTransactionManager  然后使用spring内置的数据库封装类进行相关的操作：JdbcTemplate，之后使用aop将事务管理直接注入到需要实现事务的操作类中，使用切面增强，当发生异常的时候，spring将会自动的将之前封装的JDBCTempate进行回滚操作

#### 使用基于配置文件的配置方法

> xml配置文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:tx="http://www.springframework.org/schema/tx"
	xmlns:aop="http://www.springframework.org/schema/aop"
	xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
		http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-4.3.xsd
		http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-4.3.xsd">
	<bean id="propertyConfigurer"
		class="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer">
		<property name="locations">
			<list>
				<value>config/dbconfig.properties</value>
			</list>
		</property>
	</bean>
	<!-- 阿里 druid 数据库连接池 -->
	<bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource"
		destroy-method="close">
		<!-- 数据库基本信息配置 -->
		<property name="url" value="${url}" />
		<property name="username" value="${username}" />
		<property name="password" value="${password}" />
		<property name="driverClassName" value="${driverClassName}" />
		<property name="filters" value="${filters}" />
		<!-- 最大并发连接数 -->
		<property name="maxActive" value="${maxActive}" />
		<!-- 初始化连接数量 -->
		<property name="initialSize" value="${initialSize}" />
		<!-- 配置获取连接等待超时的时间 -->
		<property name="maxWait" value="${maxWait}" />
		<!-- 最小空闲连接数 -->
		<property name="minIdle" value="${minIdle}" />
		<!-- 配置间隔多久才进行一次检测，检测需要关闭的空闲连接，单位是毫秒 -->
		<property name="timeBetweenEvictionRunsMillis" value="${timeBetweenEvictionRunsMillis}" />
		<!-- 配置一个连接在池中最小生存的时间，单位是毫秒 -->
		<property name="minEvictableIdleTimeMillis" value="${minEvictableIdleTimeMillis}" />
		<property name="validationQuery" value="${validationQuery}" />
		<property name="testWhileIdle" value="${testWhileIdle}" />
		<property name="testOnBorrow" value="${testOnBorrow}" />
		<property name="testOnReturn" value="${testOnReturn}" />
		<property name="maxOpenPreparedStatements" value="${maxOpenPreparedStatements}" />
		<!-- 打开 removeAbandoned 功能 -->
		<property name="removeAbandoned" value="${removeAbandoned}" />
		<!-- 1800 秒，也就是 30 分钟 -->
		<property name="removeAbandonedTimeout" value="${removeAbandonedTimeout}" />
		<!-- 关闭 abanded 连接时输出错误日志 -->
		<property name="logAbandoned" value="${logAbandoned}" />
	</bean>
	<!-- 指定spring容器进行接管的manager -->
	<bean id="transactionManager"
		class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
		<property name="dataSource" ref="dataSource"></property>
	</bean>
	<!-- 封装mysql驱动 使用spring自带的框架让这个框架接管数据库的操作 -->
	<bean id="jdbcTemplete" class="org.springframework.jdbc.core.JdbcTemplate">
		<property name="dataSource" ref="dataSource"></property>
	</bean>
	<!-- 生命将要进行使用的数据库操作类 -->
	<bean id="useDao" class="b_spring.d_spring事务.UseMysql">
		<property name="jdbcTemplate" ref="jdbcTemplete"></property>
	</bean>
	<!-- 使用声明式的事务增强方法 -->
	<tx:advice id="mytx" transaction-manager="transactionManager">
		<tx:attributes>
			<tx:method name="*" propagation="REQUIRED" isolation="DEFAULT" />
		</tx:attributes>
	</tx:advice>
	<!-- 使用aop方法进行事务注入 -->
	<aop:config>
		<aop:pointcut expression="execution(* b_spring.d_spring事务.*.up*(..))" id="cut"/>
		<aop:advisor advice-ref="mytx" pointcut-ref="cut"/>
	</aop:config>
</beans>
```

> java的数据库操作类

```java
import org.springframework.jdbc.core.JdbcTemplate;
public class UseMysql {
	private JdbcTemplate jdbcTemplate;
	public JdbcTemplate getJdbcTemplate() {
		return jdbcTemplate;
	}
	public void setJdbcTemplate(JdbcTemplate jdbcTemplate) {
		this.jdbcTemplate = jdbcTemplate;
	}
	public void upitem(int number) {
		int args=99;
		int args1=100;
		String name ="marry";
		String name1="tom";
		this.jdbcTemplate.update("update Transfer set money=? where name=?",new Object[] {args,name},new int[] {java.sql.Types.VARCHAR,java.sql.Types.VARCHAR});
		int a=1/0;
		this.jdbcTemplate.update("update Transfer set money=? where name=?",new Object[] {args1,name1},new int[] {java.sql.Types.VARCHAR,java.sql.Types.VARCHAR});
	}
}
```

> java 测试方法

```java
import static org.junit.Assert.*;
import org.junit.runner.RunWith;
import org.springframework.beans.BeansException;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import b_spring.b_spring零配置.bean.ItemService;
import b_spring.d_spring事务.UseMysql;
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = { "classpath:d_bean.xml" })
public class Test implements ApplicationContextAware{
	ApplicationContext context;
	@org.junit.Test
	public void test() {
		UseMysql useMysql =context.getBean("useDao", UseMysql.class);
		useMysql.upitem(199);
	}
	@Override
	public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
		// TODO Auto-generated method stub
		this.context=applicationContext;
	}
}
```

#### 使用spring注解的方法进行配置

> xml配置文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:tx="http://www.springframework.org/schema/tx"
	xmlns:aop="http://www.springframework.org/schema/aop"
	xmlns:context="http://www.springframework.org/schema/context"
	xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
		http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.3.xsd
		http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-4.3.xsd
		http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-4.3.xsd">
	<bean id="propertyConfigurer"
		class="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer">
		<property name="locations">
			<list>
				<value>config/dbconfig.properties</value>
			</list>
		</property>
	</bean>
	<!-- 阿里 druid 数据库连接池 -->
	<bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource"
		destroy-method="close">
		<!-- 数据库基本信息配置 -->
		<property name="url" value="${url}" />
		<property name="username" value="${username}" />
		<property name="password" value="${password}" />
		<property name="driverClassName" value="${driverClassName}" />
		<property name="filters" value="${filters}" />
		<!-- 最大并发连接数 -->
		<property name="maxActive" value="${maxActive}" />
		<!-- 初始化连接数量 -->
		<property name="initialSize" value="${initialSize}" />
		<!-- 配置获取连接等待超时的时间 -->
		<property name="maxWait" value="${maxWait}" />
		<!-- 最小空闲连接数 -->
		<property name="minIdle" value="${minIdle}" />
		<!-- 配置间隔多久才进行一次检测，检测需要关闭的空闲连接，单位是毫秒 -->
		<property name="timeBetweenEvictionRunsMillis" value="${timeBetweenEvictionRunsMillis}" />
		<!-- 配置一个连接在池中最小生存的时间，单位是毫秒 -->
		<property name="minEvictableIdleTimeMillis" value="${minEvictableIdleTimeMillis}" />
		<property name="validationQuery" value="${validationQuery}" />
		<property name="testWhileIdle" value="${testWhileIdle}" />
		<property name="testOnBorrow" value="${testOnBorrow}" />
		<property name="testOnReturn" value="${testOnReturn}" />
		<property name="maxOpenPreparedStatements" value="${maxOpenPreparedStatements}" />
		<!-- 打开 removeAbandoned 功能 -->
		<property name="removeAbandoned" value="${removeAbandoned}" />
		<!-- 1800 秒，也就是 30 分钟 -->
		<property name="removeAbandonedTimeout" value="${removeAbandonedTimeout}" />
		<!-- 关闭 abanded 连接时输出错误日志 -->
		<property name="logAbandoned" value="${logAbandoned}" />
	</bean>
	<!-- 配置 jdbcTemplate -->
	<bean id="jdbcTemplate" class="org.springframework.jdbc.core.JdbcTemplate">
		<property name="dataSource" ref="dataSource"></property>
	</bean>
	<!-- 将事务事务管理者注入到spring容器中 -->
	<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
		<property name="dataSource" ref="dataSource"></property>
	</bean>
	<context:component-scan base-package="b_spring.e_spring事务"></context:component-scan>
	<!-- 使用这个注解自动的加载一些spring的配置方法，指定事务管理者等等 -->
	<tx:annotation-driven  transaction-manager="transactionManager"/>
</beans>
```

> java数据库操作类

```java
package b_spring.e_spring事务;
import javax.annotation.Resource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Controller;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;
@Controller(value="use")
public class UseMysql {
	@Resource(name="jdbcTemplate")
	private JdbcTemplate jdbcTemplate;
	public JdbcTemplate getJdbcTemplate() {
		return jdbcTemplate;
	}
	public void setJdbcTemplate(JdbcTemplate jdbcTemplate) {
		this.jdbcTemplate = jdbcTemplate;
	}
	@Transactional(isolation=Isolation.DEFAULT,propagation=Propagation.REQUIRED)
	public void up() {
		int args=200;
		int args1=300;
		String name ="marry";
		String name1="tom";
		this.jdbcTemplate.update("update Transfer set money=? where name=?",new Object[] {args,name},new int[] {java.sql.Types.VARCHAR,java.sql.Types.VARCHAR});
		//int a=1/0;
		this.jdbcTemplate.update("update Transfer set money=? where name=?",new Object[] {args1,name1},new int[] {java.sql.Types.VARCHAR,java.sql.Types.VARCHAR});
	}
}
```

> 测试类

```java
package b_spring.d_test;
import static org.junit.Assert.*;
import org.junit.runner.RunWith;
import org.springframework.beans.BeansException;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import b_spring.e_spring事务.UseMysql;
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = { "classpath:e_bean.xml" })
public class Test implements ApplicationContextAware{
	ApplicationContext context;
	@org.junit.Test
	public void test() {
		UseMysql useMysql =context.getBean("use", UseMysql.class);
		useMysql.up();
	}
	@Override
	public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
		// TODO Auto-generated method stub
		this.context=applicationContext;
	}
}
```