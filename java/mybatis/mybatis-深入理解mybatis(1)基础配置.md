---
title: 深入理解mybatis(一) 基础配置
date: 2018-10-09 15:48:08
updated: 2018-10-09 15:48:08
tags: 
    - mybatis
    - orm
categories:
- 数据库
- orm框架
- mybatis
---

## 深入理解mybatis(一) 基础配置

MyBatis 是一款优秀的持久层框架，它支持定制化 SQL、存储过程以及高级映射。MyBatis 避免了几乎所有的 JDBC 代码和手动设置参数以及获取结果集。MyBatis 可以使用简单的 XML 或注解来配置和映射原生信息，将接口和 Java 的 POJOs(Plain Old Java Objects,普通的 Java对象)映射成数据库中的记录。

### mybatis基础配置和使用

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE PUBLIC "-//mybatis.org//DTD Config 3.0//EN" "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!-- 使用配置信息可以在上下文中进行配置 这里配置的信息可以在上下中使用${xx}访问到-->
    <properties resource="jdbc.properties"><!-- 这里的第一句使用了配置文件属性这个属性会搜索一个属将配置信息传入进来效果和在文件中直接进行配置的方法是相同的 -->
        <property name="myproperty" value="123123"/>
    </properties>
    <!-- setting属性 -->
    <settings>
        <!-- 打印查询语句 -->
        <setting name="logImpl" value="STDOUT_LOGGING" />
        <!-- 只有这个最好用使用内置方法  打印SQL只需要加一个setting就可以了。 mybatis的日志打印方式比较多，SLF4J | LOG4J | LOG4J2 |
        JDK_LOGGING | COMMONS_LOGGING | STDOUT_LOGGING | NO_LOGGING，可以根据自己的需要进行配置 -->
        <!-- 开启延迟加载 只用在使用的时候才进行数据库访问-->
        <setting name="lazyLoadingEnabled" value="true"/>
        <!--
            属性true按照 层级加载（理解  就是按照第一次查询必须要出现的东西，就是第n次select可以查出的内容
            (discriminator属性和id result属性相同同)，false按照需求加载
        -->
        <setting name="aggressiveLazyloading" value="false"></setting>
        <!-- 配置全局缓存的开关 -->
        <setting name="cacheEnable" value="true"/>
        <!-- 决定框架的延迟时间 -->
        <setting name="defaultStatementTimeout" value="100"/>
        <!--     其他相关的属性
        cacheEnabled				该配置影响的所有映射器中配置的缓存的全局开关。
                                    true | false	true
        lazyLoadingEnabled			延迟加载的全局开关。当开启时，所有关联对象都会延迟加载。
                                    特定关联关系中可通过设置fetchType属性来覆盖该项的开关状态.
                                    true | false	false
        aggressiveLazyLoading		当开启时，任何方法的调用都会加载该对象的所有属性。否则，每个属性会按需加载（参考lazyLoadTriggerMethods).
        multipleResultSetsEnabled	是否允许单一语句返回多结果集（需要兼容驱动）。
                                    true | false	true
        autoMappingBehavior			指定 MyBatis 应如何自动映射列到字段或属性。
                                    NONE 表示取消自动映射；PARTIAL 只会自动映射没有定义嵌套结果集映射的结果集。 FULL 会自动映射任意复杂的结果集（无论是否嵌套）。
                                    NONE,PARTIAL,FULL	PARTIAL
        defaultExecutorType			配置默认的执行器。SIMPLE 就是普通的执行器；REUSE 执行器会重用预处理语句（prepared statements）;BATCH 执行器将重用语句并执行批量更新.
                                    SIMPLE REUSE BATCH	SIMPLE
        defaultStatementTimeout		设置超时时间，它决定驱动等待数据库响应的秒数。
                                    任意正整数	Not Set (null)
        defaultFetchSize			为驱动的结果集获取数量（fetchSize）设置一个提示值。此参数只可以在查询设置中被覆盖。
                                    任意正整数	Not Set (null)
        safeRowBoundsEnabled		允许在嵌套语句中使用分页（RowBounds）。 If allow, set the false.
                                    true | false	False
        safeResultHandlerEnabled	允许在嵌套语句中使用分页（ResultHandler）。 If allow, set the false.
                                    true | false	True
        mapUnderscoreToCamelCase	是否开启自动驼峰命名规则（camel case）映射，即从经典数据库列名 A_COLUMN 到经典 Java 属性名 aColumn 的类似映射。
                                    true | false	False
        localCacheScope	MyBatis 	利用本地缓存机制（Local Cache）防止循环引用（circular references）和加速重复嵌套查询。
                                    默认值为 SESSION，这种情况下会缓存一个会话中执行的所有查询。
                                    若设置值为 STATEMENT，本地会话仅用在语句执行上，对相同 SqlSession 的不同调用将不会共享数据。
                                    SESSION | STATEMENT	SESSION
        jdbcTypeForNull				当没有为参数提供特定的 JDBC 类型时，为空值指定 JDBC 类型。
                                    某些驱动需要指定列的 JDBC 类型，多数情况直接用一般类型即可，比如 NULL、VARCHAR 或 OTHER。
                                    JdbcType enumeration. Most common are: NULL, VARCHAR and OTHER	OTHER
        lazyLoadTriggerMethods		指定哪个对象的方法触发一次延迟加载。
                                    A method name list separated by commas	equals,clone,hashCode,toString
        defaultScriptingLanguage	指定动态 SQL 生成的默认语言。	A type alias or fully qualified class name.
                                    org.apache.ibatis.scripting.xmltags.XMLLanguageDriver
        callSettersOnNulls			指定当结果集中值为 null 的时候是否调用映射对象的 setter（map 对象时为 put）方法，
                                    这对于有 Map.keySet() 依赖或 null 值初始化的时候是有用的。注意基本类型（int、boolean等）是不能设置成 null 的。
                                    true | false	false
        logPrefix					指定 MyBatis 增加到日志名称的前缀。
                                    Any String	Not set
        logImpl						指定 MyBatis 所用日志的具体实现，未指定时将自动查找。
                                    SLF4J | LOG4J | LOG4J2 | JDK_LOGGING | COMMONS_LOGGING | STDOUT_LOGGING | NO_LOGGING	Not set
         -->
    </settings>
    <!-- 别名:在系统的其他位置上可以用这个别名进行配置文件的配置 两种方法只能用一种 原因 文件只进行扫描一遍-->
    <typeAliases>
        <!-- 1.可以使用注解方法进行配置 Alias注解方法 name为将要进行扫描的包  使用的时候自动为相关的类添加上相关的包名称，但是要注意冲突的问题 -->
        <package name="javabean"/><!-- 如果使用这个中方法将会自动将这个包下面直接的javabean 按照小写字母映射 不能和下面的方法共存 -->
        <!-- 直接在这里面进行配置type是属性的全名称 alias 是别名称 -->
        <typeAlias type="S_Mybatis.a_自定义typeHandler.自定义typeHandler" alias="mytypehandle"/>
    </typeAliases>
    <!--格式转换器 定义的转换器 可以完成java类型和jdbc类型的自动转换  一般用来自己重写数据库的映射方法-->
    <typeHandlers>
        <typeHandler handler="S_Mybatis.a_自定义typeHandler.自定义typeHandler" javaType="string" jdbcType="VARCHAR"/>
        <package name="S_Mybatis.a_自定义typeHandler"/><!-- 使用注解方法加载包 自动加入对应包中有属性的名称使用xml的定义式 -->
    </typeHandlers>
    <objectFactory type="S_Mybatis.b_自定义工厂方法.Myfactory">
        <property name="name" value="b_自定义工厂方法"/>
    </objectFactory>
    <!-- 数据库环境标签 -->
    <environments default="myenviroment"><!-- 这个属性表明在环境变量缺省的情况下启用哪个标签 -->
        <!-- 配置一个数据源的开始 -->
        <environment id="myenviroment">
            <!-- 数据库事务配置 (一般使用spring框架进行控制 之后再说)1.jdbc 2.MANAGEN(JNDI数据源中的相关事务)3.自定义 -->
            <transactionManager type="JDBC"></transactionManager>
            <!-- 配置数据连接信息1.UNPOOLED非连接池数据库2.POOLED链接池数据库3.JNDI 4.自定义  -->
            <dataSource type="UNPOOLED">
                <!-- 针对 pooled属性的：
                    poolMaximumActiveConnections 	– 在任意时间可以存在的活动（也就是正在使用）连接数量，默认值：10
                    poolMaximumIdleConnections 		– 任意时间可能存在的空闲连接数。
                    poolMaximumCheckoutTime			– 在被强制返回之前，池中连接被检出（checked out）时间，默认值：20000 毫秒（即 20 秒）
                    poolTimeToWait 					– 这是一个底层设置，如果获取连接花费的相当长的时间，
                                                    - 它会给连接池打印状态日志并重新尝试获取一个连接（避免在误配置的情况下一直安静的失败），
                                                    - 默认值：20000 毫秒（即 20 秒）。
                    poolPingQuery 					– 发送到数据库的侦测查询，用来检验连接是否处在正常工作秩序中并准备接受请求。
                                                    - 默认是“NO PING QUERY SET”，这会导致多数数据库驱动失败时带有一个恰当的错误消息。
                    poolPingEnabled 				– 是否启用侦测查询。若开启，也必须使用一个可执行的 SQL 语句设置 poolPingQuery 属性（最好是一个非常快的 SQL），
                                                    - 默认值：false。
                    poolPingConnectionsNotUsedFor 	– 配置 poolPingQuery 的使用频度。这可以被设置成匹配具体的数据库连接超时时间，来避免不必要的侦测，
                                                    - 默认值：0（即所有连接每一时刻都被侦测 — 当然仅当 poolPingEnabled 为 true 时适用）。
                 -->
                <!-- 使用 ognl表达式的${}形式加入参数 -->
                <property name="driver" value="${properties_driver}" />
                <property name="url" value="jdbc:mysql://127.0.0.1:3306/mybatis" />
                <property name="username" value="${properties_user}" />
                <property name="password" value="14159265jkl" />
            </dataSource>
            <!-- 数据库事务 -->
        </environment>
    </environments>
    <!-- mybatis数据库厂商标识 db_vendor 使用数据库默认规则-首先mybatis会将配置读入configuration中
    在连接数据库后调用getDatabaseProductName（）方法获取数据库的信息，然后配置name值去做匹配来得到databaseid  -->
    <databaseIdProvider type="DB_VENDOR">
        <property name="SQL Server" value="sqlserver"/>
        <property name="DB2" value="db2"/>
        <property name="Oracle" value="oracle" />
    </databaseIdProvider>
    <!-- 定义mybatis使用的映射文件 !!!!!注意这里非常容易出现错误 要使用的文件mapping一定要在这里面进行配置-->
    <mappers>
        <mapper resource="mapper_WaiLianJie.xml"/><!-- 使用文件进行引入 -->
        <!--<mapper class="com.dao.mapper_SqlQianTao"/>--><!-- 使用class文件进行引入 -->
        <!--貌似不能和mapper共存<package name="com.dao"/>使用报名进行引入-->
        <mapper url="file:///var/mappers/AuthorMapper.xml"/><!-- 使用url进行引用 -->
    </mappers>

</configuration>
```

### 相关标签注意事项

#### typeAliases 别名配置引申

如果使用package的标签的时候将会使用将类名首字母小写和对应的对象完整类名映射，可以通过@Alias(name) 注解来更改映射的规则

#### properties标签除了使用xml进行相关属性配置，还可以使用java api的形式可以使用如下的方法进行配置

> 使用java代码动态的导入属性

```java
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

public class Mybatis {
    public static void main(String[] args) {
        InputStream inputStream=null;
        try {
            inputStream = Resources.getResourceAsStream("xxxx.xml");
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        Properties properties = new Properties();
        properties.setProperty("username", "root");
        properties.setProperty("password", "14159265jkl");
        SqlSessionFactory sessionFactory=new SqlSessionFactoryBuilder().build(inputStream, properties);
    }
}
```

如果属性在不只一个地方进行了配置，那么 MyBatis 将按照下面的顺序来加载：

1. 在 properties 元素体内指定的属性首先被读取。
2. 然后根据 properties 元素中的 resource 属性读取类路径下属性文件或根据 url 属性指定的路径读取属性文件，并覆盖已读取的同名属性。
3. 最后读取作为方法参数传递的属性，并覆盖已读取的同名属性。
- 因此，通过方法参数传递的属性具有最高优先级，resource/url 属性中指定的配置文件次之，最低优先级的是 properties 属性中指定的属性。


> 使用输入流进行构建

```java
import java.io.IOException;
import java.io.InputStream;

import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

public class Mybatis {
    public static void main(String[] args) {
        String resource = "mybatis-config.xml";
        InputStream inputStream=null;
        try {
            inputStream = Resources.getResourceAsStream(resource);
        } catch (IOException e) {
            e.printStackTrace();
        }
        SqlSessionFactory sessionFactory =new SqlSessionFactoryBuilder().build(inputStream);
    }
}
```

#### typeHandlers-重写类型处理器或创建你自己的类型处理器来处理不支持的或非标准的类型

具体做法为：实现 org.apache.ibatis.type.TypeHandler 接口， 或继承一个很便利的类 org.apache.ibatis.type.BaseTypeHandler， 然后可以选择性地将它映射到一个 JDBC 类型。

```java
import java.sql.CallableStatement;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import org.apache.ibatis.type.BaseTypeHandler;
import org.apache.ibatis.type.JdbcType;
import org.apache.ibatis.type.MappedJdbcTypes;
import org.apache.ibatis.type.MappedTypes;
import org.apache.ibatis.type.TypeHandler;
//!--注意若果使用了注解就可以在配置文件中使用pagexx的属性而不用使用typeHandler属性
@MappedTypes({ String.class }) // 定义数据库映射的的java属性 指定那些类型将会被拦截
@MappedJdbcTypes(JdbcType.VARCHAR) // 定义数据库映射数据库的类型
// 当使用自定义typeHandle的时候需要实现这个接口
// !---在mapping文件中需要显示的注册使用的tylehandle 并且在mybatis的配置文件(和mapping文集不同)文件中个必须进行注册
//注意 MappedJdbcTypes这个注解还有一个属性 includeNullJdbcType=true 默认值为false 表示当在只使用时-
//-只指定了javaType类型但是没有指定 jdbctype的时候同样可以使用这个映射
public class 自定义typeHandler implements TypeHandler<String> {
    public String getResult(ResultSet arg0, String columeName) throws SQLException {
        return null;
    }

    public String getResult(ResultSet arg0, int index) throws SQLException {
        return null;
    }

    public String getResult(CallableStatement arg0, int arg1) throws SQLException {
        return null;
    }

    public void setParameter(PreparedStatement arg0, int arg1, String arg2, JdbcType arg3) throws SQLException {
    }
}
//还可以使用相关的抽象类进行实现
class MytypeHandler2 extends BaseTypeHandler<String>{
    @Override
    public String getNullableResult(ResultSet arg0, String arg1) throws SQLException {
        return null;
    }
    @Override
    public String getNullableResult(ResultSet arg0, int arg1) throws SQLException {
        return null;
    }
    @Override
    public String getNullableResult(CallableStatement arg0, int arg1) throws SQLException {
        return null;
    }

    @Override
    public void setNonNullParameter(PreparedStatement arg0, int arg1, String arg2, JdbcType arg3) throws SQLException {
    }

}
```

**mybatis在使用自定义的type的时候，需要在结果属性（resultMap中的property或者id属性中）使用javatype和JDBCtype属性进行相关联，或者直接指定typehandler**

#### 枚举类型的特殊处理

若想映射枚举类型 Enum，则需要从 EnumTypeHandler 或者 EnumOrdinalTypeHandler 中选一个来使用。默认情况下，MyBatis 会利用 EnumTypeHandler 来把 Enum 值转换成对应的名字。

> 注意 EnumTypeHandler 在某种意义上来说是比较特别的，其他的处理器只针对某个特定的类，而它不同，它会处理任意继承了 Enum 的类。

自动映射器（auto-mapper）会自动地选用 EnumOrdinalTypeHandler 来处理， 所以如果我们想用普通的 EnumTypeHandler，就必须要显式地为那些 SQL 语句设置要使用的类型处理器。

```xml
<resultMap type="org.apache.ibatis.submitted.rounding.User" id="usermap2">
	<id column="id" property="id"/>
	<result column="name" property="name"/>
	<result column="funkyNumber" property="funkyNumber"/>
	<result column="roundingMode" property="roundingMode" typeHandler="org.apache.ibatis.type.EnumTypeHandler"/>
</resultMap>
<select id="getUser2" resultMap="usermap2">
	select * from users2
</select>
<insert id="insert2">
    insert into users2 (id, name, funkyNumber, roundingMode) values (
    	#{id}, #{name}, #{funkyNumber}, #{roundingMode, typeHandler=org.apache.ibatis.type.EnumTypeHandler}
    )
</insert>
```

#### objectFactory-覆盖对象工厂的默认行为，创建自己的对象工厂。

MyBatis 每次创建结果对象的新实例时，它都会使用一个对象工厂（ObjectFactory）实例来完成。 

```java
import java.util.List;
import java.util.Properties;

import org.apache.ibatis.reflection.factory.DefaultObjectFactory;

public class Myfactory extends DefaultObjectFactory{
    private static final long serialVersionUID = 1L;
    public <T> T create(Class<T> type, List<Class<?>> constructorArgTypes, List<Object> constructorArgs) {
        return super.create(type, constructorArgTypes, constructorArgs);
    }
    public <T> T create(Class<T> type) {
        return super.create(type);
    }
    public <T> boolean isCollection(Class<T> type) {
        return super.isCollection(type);
    }
    protected Class<?> resolveInterface(Class<?> arg0) {
        return super.resolveInterface(arg0);
    }
    public void setProperties(Properties properties) {
        super.setProperties(properties);
    }
}
```

#### plugins-MyBatis 允许你在已映射语句执行过程中的某一点进行拦截调用

默认情况下，MyBatis 允许使用插件来拦截的方法调用包括（格式：类名称（类下的方法））：

- Executor (update, query, flushStatements, commit, rollback, getTransaction, close, isClosed)
- ParameterHandler (getParameterObject, setParameters)
- ResultSetHandler (handleResultSets, handleOutputParameters)
- StatementHandler (prepare, parameterize, batch, update, query)

通过 MyBatis 提供的强大机制，使用插件是非常简单的，只需实现 Interceptor 接口，并指定了想要拦截的方法签名即可

> 下面的插件将会拦截在 Executor 实例中所有的 “update” 方法调用， 这里的 Executor 是负责执行低层映射语句的内部对象。**注意@Intercepts注解**

```java
import java.util.Properties;
import org.apache.ibatis.executor.Executor;
import org.apache.ibatis.mapping.MappedStatement;
import org.apache.ibatis.plugin.Interceptor;
import org.apache.ibatis.plugin.Intercepts;
import org.apache.ibatis.plugin.Invocation;
import org.apache.ibatis.plugin.Signature;
@Intercepts({@Signature(
        type= Executor.class,
        method = "update",
        args = {MappedStatement.class,Object.class})})
public class ExamplePlugin implements Interceptor{
    @Override
    public Object intercept(Invocation arg0) throws Throwable {
        // TODO Auto-generated method stub
        return null;
    }
    @Override
    public Object plugin(Object arg0) {
        // TODO Auto-generated method stub
        return null;
    }
    @Override
    public void setProperties(Properties arg0) {
        // TODO Auto-generated method stub

    }
}
```

#### environments-MyBatis可以通过这个配置项配置成适应多种环境

这种机制有助于将 SQL 映射应用于多种数据库之中， 现实情况下有多种理由需要这么做。例如，开发、测试和生产环境需要有不同的配置；或者共享相同 Schema 的多个生产数据库， 想使用相同的 SQL 映射。许多类似的用例。
> 不过要记住：尽管可以配置多个环境，每个 SqlSessionFactory 实例只能选择其一。为了指定创建哪种环境，只要将它作为可选的参数传递给 SqlSessionFactoryBuilder 即可

```java
SqlSessionFactory sessionFactory=new SqlSessionFactoryBuilder().build(inputStream,"envoirment");
SqlSessionFactory factory = new SqlSessionFactoryBuilder().build(reader, environment);
SqlSessionFactory factory = new SqlSessionFactoryBuilder().build(reader, environment,properties);
```
在环境配置中有两个重要的配置一个是事务管理器transactionManager，另一个是数据源dataSource （具体的配置信息可以参考之前使用的xml 配置方法）

> transactionManager事务管理器
```java
public interface TransactionFactory {
  void setProperties(Properties props);  
  Transaction newTransaction(Connection conn);
  Transaction newTransaction(DataSource dataSource, TransactionIsolationLevel level, boolean autoCommit);  
}
```
任何在 XML 中配置的属性在实例化之后将会被传递给 setProperties() 方法。你也需要创建一个 Transaction 接口的实现类，这个接口也很简单：
```java
public interface Transaction {
  Connection getConnection() throws SQLException;
  void commit() throws SQLException;
  void rollback() throws SQLException;
  void close() throws SQLException;
  Integer getTimeout() throws SQLException;
}
```


#### databaseIdProvider

MyBatis 可以根据不同的数据库厂商执行不同的语句，这种多厂商的支持是基于映射语句中的 databaseId 属性。 MyBatis 会加载不带 databaseId 属性和带有匹配当前数据库 databaseId 属性的所有语句。 如果同时找到带有 databaseId 和不带 databaseId 的相同语句，则后者会被舍弃。 

#### mappers表示映射器

注意：一个config文件可以导入多个配置文件   可以使用url地址或者resource 引入配置文件或者 使用包名称或者class文件

```xml
<mappers>
    <mapper resource="mapper_WaiLianJie.xml"/><!-- 使用文件进行引入 -->
    <!--<mapper class="com.dao.mapper_SqlQianTao"/>--><!-- 使用class文件进行引入 -->
    <!--貌似不能和mapper共存<package name="com.dao"/>使用报名进行引入-->
    <mapper url="file:///var/mappers/AuthorMapper.xml"/><!-- 使用url进行引用 -->
</mappers>
```