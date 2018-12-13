## 深入理解mybatis（七）mybatis和spring结合

实现mybatis和spring的整合的时候注意spring在和mybatis整合的时候需要使用额外的依赖配置

```xml
<dependency>
  <groupId>org.mybatis</groupId>
  <artifactId>mybatis-spring</artifactId>
  <version>x.x.x</version>
</dependency>
```

### SqlSessionFactoryBean

在基本的 MyBatis 中,session 工厂可以使用 SqlSessionFactoryBuilder 来创建。而在 MyBatis-Spring 中,则使用 SqlSessionFactoryBean 来替代。

要注意这个配置文件不需要是一个完整的 MyBatis 配置。确切地说,任意环境,数据源 和 MyBatis 的事务管理器都会被忽略。SqlSessionFactoryBean 会创建它自己的,使用这些 值定制 MyBatis 的 Environment 时是需要的。

如果MyBatis映射器XML文件在和映射器类相同的路径下不存在,那么另外一个需要 配置文件的原因就是它了。使用这个配置,有两种选择。第一是手动在 MyBatis 的 XML 配 置文件中使用<mappers>部分来指定类路径。第二是使用工厂bean的mapperLocations属性。

```xml
<bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
  <property name="dataSource" ref="dataSource" />
</bean>
```

以上配置文件相当于以下java语句

> 要注意 SqlSessionFactoryBean 实现了 Spring 的 FactoryBean 接口(请参考 Spring 文 档的 3.8 章节)这就说明了由 Spring 最终创建的 bean 不是 SqlSessionFactoryBean 本身, 。 而是工厂类的 getObject()返回的方法的结果。



```java
SqlSessionFactoryBean factoryBean = new SqlSessionFactoryBean();
SqlSessionFactory sessionFactory = factoryBean.getObject();
```

### 添加事物管理

很简单只要将声明并且传入SqlSessionFactoryBean中的datasource添加上相关事务性操作的就好了 和 一般的spring事务配置相同

```xml
<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
	<property name="dataSource" ref="dataSource"></property>
</bean>
```

```xml
<tx:annotation-driven transaction-manager="transactionManager"/>
```

```java
@Component("moneyService")
public class MoneyService {
	@Resource(name="userMoney")
	public UserMoney userMoney;
	@Transactional(isolation=Isolation.DEFAULT,propagation=Propagation.REQUIRED)
	public void okStart(People from,People to) {
		userMoney.addMoney(from.getMoney(), from);
		userMoney.deductMoney(to.getMoney(), to);
	}
}
```

### 使用 SqlSessionTemplate 代替sqlSession

SqlSessionTemplate 对象可以使用 SqlSessionFactory 作为构造方法的参数来代替Sqlsession。应为它实现了Sqlsession接口`

```xml
<bean id="sqlSession" class="org.mybatis.spring.SqlSessionTemplate">
  <constructor-arg index="0" ref="sqlSessionFactory" />
</bean>
```

将SqlSession配置到bean中

```xml
<bean id="userDao" class="org.mybatis.spring.sample.dao.UserDaoImpl">
  <property name="sqlSession" ref="sqlSession" />
</bean>
```

java代码使用注入进来的SqlSession

```java
public class UserDaoImpl implements UserDao {
 
  private SqlSession sqlSession;
 
  public void setSqlSession(SqlSession sqlSession) {
    this.sqlSession = sqlSession;
  }
 
  public User getUser(String userId) {
    return (User) sqlSession.selectOne("org.mybatis.spring.sample.mapper.UserMapper.getUser", userId);
  }
}
```

SqlSessionTemplate 有一个使用 ExecutorType 作为参数的构造方法。这允许你用来 创建对象,比如,一个批量 SqlSession,但是使用了下列 Spring 配置的 XML 文件:

```xml
<bean id="sqlSession" class="org.mybatis.spring.SqlSessionTemplate">
  <constructor-arg index="0" ref="sqlSessionFactory" />
  <constructor-arg index="1" value="BATCH" />
</bean>
```
现在你所有的语句可以批量操作了,下面的语句就可以在 DAO 中使用了。

```java
public void insertUsers(User[] users) {
   for (User user : users) {
     sqlSession.insert("org.mybatis.spring.sample.mapper.UserMapper.insertUser", user);
   }
 }
```

### MapperFactoryBean

为了代替手工使用 SqlSessionDaoSupport 或 SqlSessionTemplate 编写数据访问对象 (DAO)的代码,MyBatis-Spring 提供了一个动态代理的实现:MapperFactoryBean。这个类 可以让你直接注入数据映射器接口到你的 service 层 bean 中。当使用映射器时,你仅仅如调 用你的 DAO 一样调用它们就可以了,但是你不需要编写任何 DAO 实现的代码,因为 MyBatis-Spring 将会为你创建代理。

配置方法

```xml
<bean id="userMapper" class="org.mybatis.spring.mapper.MapperFactoryBean">
    <property name="mapperInterface" value="org.mybatis.spring.sample.mapper.UserMapper" />
    <property name="sqlSessionFactory" ref="sqlSessionFactory" />
    <property name="sqlSessionTemplate" ref="sqlSessionTemplate"></property>
</bean>
```

通过配置得到的bean等价于使用sqlSession.getMapper(xxx.class);方法的返回结果

> 注意：传入的接口信息，应该可以在传入的SqlSessionFactory配置的mapper映射文件中有相应的namespace

> 注意,当 MapperFactoryBean 需要 SqlSessionFactory 或 SqlSessionTemplate 时。 这些可以通过各自的 SqlSessionFactory 或 SqlSessionTemplate 属性来设置, 或者可以由 Spring 来自动装配。如果两个属性都设置了,那么 SqlSessionFactory 就会被忽略,因为 SqlSessionTemplate 是需要有一个 session 工厂的设置; 那个工厂会由 MapperFactoryBean. 来使用。

可以直接在 business/service 对象中以和注入任意 Spring bean 的相同方式直接注入映 射器:

```xml
<bean id="fooService" class="org.mybatis.spring.sample.mapper.FooServiceImpl">
  <property name="userMapper" ref="userMapper" />
</bean>
```

```java
public class FooServiceImpl implements FooService {
 
  private UserMapper userMapper;
 
  public void setUserMapper(UserMapper userMapper) {
    this.userMapper = userMapper;
  }
 
  public User doSomeBusinessStuff(String userId) {
    return this.userMapper.getUser(userId);
  }
}
```

### 使用MapperScannerConfigurer简化配置

使用mapperFactoryBean的时候感觉每一个映射接口都要进行相关的配置，所以我们需要为一个可以自动进行所有配置的整合配置方法

```xml
<bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
    <property name="basePackage" value="org.dao"></property>
    <!--<property name="sqlSessionFactoryBeanName" value="sqlSessionFactory"></property> -->
    <property name="sqlSessionTemplateBeanName" value="sqlSession"></property>
    <!-- 限定型操作，指定要进行寻找的注解名称或者接口名称 -->
    <property name="annotationClass" value="org.springframework.stereotype."></property>
    <property name="markerInterface" value="org.dao.xxxx"></property>
</bean>
```

这个注解可以替代mapperFactoryBean，而且，只要指定包名称，框架将会自动按照spring注解的命名规则将相关接口注入到spring的命名空间中（可以使用spring的自动扫描注解，指定映射名称）

> 2018年8月补充 通过阅读源代码发现 @Mapper这个注解在spring-mybatis和mybatis 本身中更本不起道任何作用，只有在spring boot中有过使用（不过大多数的都是直接使用@MapperScan）

### 一个实例

> mybatis的相关配置文件

1. mybatis-config.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE configuration PUBLIC "-//mybatis.org//DTD Config 3.0//EN" "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
	<settings>
		<setting name="logImpl" value="STDOUT_LOGGING"/>
		<setting name="mapUnderscoreToCamelCase" value="true"/>
	</settings>
	<!-- 和sping框架进行结合的时候不需要使用enviroment标签spring框架会自动的设置好 -->
	<mappers>
		<mapper resource="mymapper.xml"/>
	</mappers>
</configuration>
```

2. mymapper.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="org.dao.UserMoney">
	<resultMap type="org.user.People" id="people">
		<id column="name" jdbcType="VARBINARY" javaType="string"/>
		<result column="money" jdbcType="INTEGER" javaType="int"/>
	</resultMap>
	<update id="addMoney" parameterType="org.user.People" statementType="PREPARED">
		update user set money=#{money} where name= #{people.name}
	</update>
	<update id="deductMoney" parameterType="org.user.People" statementType="PREPARED">
		update user set money=#{money} where name= #{people.name}
	</update>
	<select id="showMoney" resultMap="people">
		select * from user;
	</select>
</mapper>
```

> bean相关配置文件和数据库连接池相关配置

1. datasource.properties

```
url=jdbc:mysql://localhost:3306/demo
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

2. bean.xml

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
    <context:component-scan base-package="org.dao"></context:component-scan>
    <context:component-scan base-package="org.user"></context:component-scan>
    <context:component-scan base-package="org.Service"></context:component-scan>
    <!-- 启用配置文件设置方法 -->
    <bean id="propertyConfigurer" class="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer">
        <property name="locations">
            <list value-type="java.lang.String">
                <value>classpath:datasource.properties</value>
            </list>
        </property>
    </bean>
    <!-- 配置数据源 使用阿里巴巴数据库连接池 -->
    <bean id = "dataSource" class = "com.alibaba.druid.pool.DruidDataSource" destroy-method = "close" >
        <!-- 数据库基本信息配置 -->
        <property name = "url" value = "${url}" />
        <property name = "username" value = "${username}" />
        <property name = "password" value = "${password}" />
        <property name = "driverClassName" value = "${driverClassName}" />
        <property name = "filters" value = "${filters}" />
        <!-- 最大并发连接数 -->
        <property name = "maxActive" value = "${maxActive}" />
        <!-- 初始化连接数量 -->
        <property name = "initialSize" value = "${initialSize}" />
        <!-- 配置获取连接等待超时的时间 -->
        <property name = "maxWait" value = "${maxWait}" />
        <!-- 最小空闲连接数 -->
        <property name = "minIdle" value = "${minIdle}" />
        <!-- 配置间隔多久才进行一次检测，检测需要关闭的空闲连接，单位是毫秒 -->
        <property name = "timeBetweenEvictionRunsMillis" value ="${timeBetweenEvictionRunsMillis}" />
        <!-- 配置一个连接在池中最小生存的时间，单位是毫秒 -->
        <property name = "minEvictableIdleTimeMillis" value ="${minEvictableIdleTimeMillis}" />
        <property name = "validationQuery" value = "${validationQuery}" />
        <property name = "testWhileIdle" value = "${testWhileIdle}" />
        <property name = "testOnBorrow" value = "${testOnBorrow}" />
        <property name = "testOnReturn" value = "${testOnReturn}" />
        <property name = "maxOpenPreparedStatements" value ="${maxOpenPreparedStatements}" />
        <!-- 打开 removeAbandoned 功能 -->
        <property name = "removeAbandoned" value = "${removeAbandoned}" />
        <!-- 1800 秒，也就是 30 分钟 -->
        <property name = "removeAbandonedTimeout" value ="${removeAbandonedTimeout}" />
        <!-- 关闭 abanded 连接时输出错误日志 -->
        <property name = "logAbandoned" value = "${logAbandoned}" />
    </bean>
    <!-- 配置spring和mybatis 整合部分 -->
    <!-- 生成 sqlsessionFactory -->
    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
        <property name="dataSource" ref="dataSource"></property>
        <property name="configLocation" value="classpath:mybatis-config.xml"></property>
        <!--
        <property name="mapperLocations" value="classpath:xxx/*xml"></property>
         -->
        <!-- 指定某个路径下所有的配置文件使用通配符号 -->
    </bean>
    <!-- 开起spring 事务 -->
    <bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="dataSource"></property>
    </bean>
    <tx:annotation-driven transaction-manager="transactionManager"/>
    <!-- 使用SqlSessionTemplate  -->
    <bean id="sqlSession" class="org.mybatis.spring.SqlSessionTemplate">
        <constructor-arg index="0" ref="sqlSessionFactory"></constructor-arg>
        <!-- 使用配置类型  ExecutorType  -->
        <!-- <constructor-arg index="1" value="BATCH"></constructor-arg>-->
    </bean>
    <bean id="userMoney" class="org.mybatis.spring.mapper.MapperFactoryBean">
        <property name="mapperInterface" value="org.dao.UserMoney"></property>
        <property name="sqlSessionTemplate" ref="sqlSession"></property>
    </bean>
</beans>
```

> 使用mapperconfig进行配置

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
    <context:component-scan base-package="org.dao"></context:component-scan>
    <context:component-scan base-package="org.user"></context:component-scan>
    <context:component-scan base-package="org.Service"></context:component-scan>
    <!-- 启用配置文件设置方法 -->
    <bean id="propertyConfigurer" class="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer">
        <property name="locations">
            <list value-type="java.lang.String">
                <value>classpath:datasource.properties</value>
            </list>
        </property>
    </bean>
    <!-- 配置数据源 使用阿里巴巴数据库连接池 -->
    <bean id = "dataSource" class = "com.alibaba.druid.pool.DruidDataSource" destroy-method = "close" >
        <!-- 数据库基本信息配置 -->
        <property name = "url" value = "${url}" />
        <property name = "username" value = "${username}" />
        <property name = "password" value = "${password}" />
        <property name = "driverClassName" value = "${driverClassName}" />
        <property name = "filters" value = "${filters}" />
        <!-- 最大并发连接数 -->
        <property name = "maxActive" value = "${maxActive}" />
        <!-- 初始化连接数量 -->
        <property name = "initialSize" value = "${initialSize}" />
        <!-- 配置获取连接等待超时的时间 -->
        <property name = "maxWait" value = "${maxWait}" />
        <!-- 最小空闲连接数 -->
        <property name = "minIdle" value = "${minIdle}" />
        <!-- 配置间隔多久才进行一次检测，检测需要关闭的空闲连接，单位是毫秒 -->
        <property name = "timeBetweenEvictionRunsMillis" value ="${timeBetweenEvictionRunsMillis}" />
        <!-- 配置一个连接在池中最小生存的时间，单位是毫秒 -->
        <property name = "minEvictableIdleTimeMillis" value ="${minEvictableIdleTimeMillis}" />
        <property name = "validationQuery" value = "${validationQuery}" />
        <property name = "testWhileIdle" value = "${testWhileIdle}" />
        <property name = "testOnBorrow" value = "${testOnBorrow}" />
        <property name = "testOnReturn" value = "${testOnReturn}" />
        <property name = "maxOpenPreparedStatements" value ="${maxOpenPreparedStatements}" />
        <!-- 打开 removeAbandoned 功能 -->
        <property name = "removeAbandoned" value = "${removeAbandoned}" />
        <!-- 1800 秒，也就是 30 分钟 -->
        <property name = "removeAbandonedTimeout" value ="${removeAbandonedTimeout}" />
        <!-- 关闭 abanded 连接时输出错误日志 -->
        <property name = "logAbandoned" value = "${logAbandoned}" />
    </bean>
    <!-- 配置spring和mybatis 整合部分 -->
    <!-- 生成 sqlsessionFactory -->
    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
        <property name="dataSource" ref="dataSource"></property>
        <property name="configLocation" value="classpath:mybatis-config.xml"></property>
        <!--
        <property name="mapperLocations" value="classpath:xxx/*xml"></property>
         -->
        <!-- 指定某个路径下所有的配置文件使用通配符号 -->
    </bean>
    <!-- 开起spring 事务 -->
    <bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="dataSource"></property>
    </bean>
    <tx:annotation-driven transaction-manager="transactionManager"/>
    <!-- 使用SqlSessionTemplate  -->
    <bean id="sqlSession" class="org.mybatis.spring.SqlSessionTemplate">
        <constructor-arg index="0" ref="sqlSessionFactory"></constructor-arg>
        <!-- 使用配置类型  ExecutorType  -->
        <!-- <constructor-arg index="1" value="BATCH"></constructor-arg>-->
    </bean>
    <!-- 
    <bean id="userMoney" class="org.mybatis.spring.mapper.MapperFactoryBean">
            <property name="mapperInterface" value="org.dao.UserMoney"></property>
            <property name="sqlSessionTemplate" ref="sqlSession"></property>
    </bean>
     -->
    <bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
        <property name="basePackage" value="org.dao"></property>
        <!--<property name="sqlSessionFactoryBeanName" value="sqlSessionFactory"></property> -->
        <property name="sqlSessionTemplateBeanName" value="sqlSession"></property>
        <!-- 限定型操作，指定要进行寻找的注解名称或者接口名称 -->
        <property name="annotationClass" value="org.springframework.stereotype."></property>
        <property name="markerInterface" value="org.dao.xxxx"></property>
    </bean>
</beans>
```

> javabean–org.user包

```java
package org.user;
 
import org.springframework.stereotype.Component;
 
@Component("people")
public class People {
	private String name;
	private int money;
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public int getMoney() {
		return money;
	}
	public void setMoney(int money) {
		this.money = money;
	}
	
}
 
package org.user;
 
import org.springframework.stereotype.Component;
 
@Component("jack")
public class Jack extends People{
	public Jack() {
		// TODO Auto-generated constructor stub
		this.setName("Jack");
	}
}
 
package org.user;
 
import org.springframework.stereotype.Component;
 
@Component("Tom")
public class Tom extends People {
	public Tom() {
		// TODO Auto-generated constructor stub
		this.setName("Tom");
	}
}
```

> mybatis映射接口-org.dao包

```java
package org.dao;
 
import java.util.List;
 
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;
import org.user.People;
 
@Repository("userMoney")
public interface UserMoney {
	public int deductMoney(@Param("money")int money,@Param("people")People people);
	public int addMoney(@Param("money")int money,@Param("people")People people);
	public List<People> showMoney();
}
```

这里要注意：mybatis参数传递的规则，默认只能传入一个类，如果是基本类型 使用#{xxx}(xxx为任意字段)就可以进行导入，如果是一个类#{xxx}(xxx为类中的任意属性)，当使用@Param注解时候，使用的时候必须相对应的名称（底层mybatis 把他参数变成map类型了）

> 数据库应用服务类-org.service

```java
package org.Service;
 
 
import javax.annotation.Resource;
 
import org.dao.UserMoney;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Isolation;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;
import org.user.People;
@Component("moneyService")
public class MoneyService {
	@Resource(name="userMoney")
	public UserMoney userMoney;
	@Transactional(isolation=Isolation.DEFAULT,propagation=Propagation.REQUIRED)
	public void okStart(People from,People to) {
		userMoney.addMoney(from.getMoney(), from);
		userMoney.deductMoney(to.getMoney(), to);
	}
}
```

> main函数

```java
package org;
 
import org.Service.MoneyService;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.user.Jack;
import org.user.Tom;
 
public class Main {
	public static void main(String[] args) {
		// TODO Auto-generated constructor stub
		ApplicationContext context=new ClassPathXmlApplicationContext("bean.xml");
		MoneyService service = context.getBean("moneyService",MoneyService.class);
		Tom tom = new Tom();
		tom.setMoney(1000);
		Jack jack = new Jack();
		jack.setMoney(1000);
		service.okStart(tom, jack);
	}
}
```