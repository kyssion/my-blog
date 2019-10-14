## 深入理解mybatis（五）java api

### SqlSessionFactoryBuilder、SqlSessionFactory、SqlSession

可以说每个MyBatis都是以一个SqlSessionFactory实例为中心的。SqlSessionFactory实例可以通过SqlSessionFactoryBuilder来构建。一是可以通过XML配置文件的方式来构建SqlSessionFactory，二是可以通过Java API的方式来构建。但不管通过什么方式都有一个Configuration贯穿始终，各种配置正是通过Configuration实例来完成实现。

#### sqlSessionfactoryBuiler生成SqlSessionFactory的方法

1. 使用java类配置实现(SqlSessionFactoryBuilder)

```java
// 配置数据库链接池
PooledDataSource pooledDataSource = new PooledDataSource();
pooledDataSource.setDriver("com.mysql.jdbc.Driver");
pooledDataSource.setUrl("jdbc:mysql://127.0.0.1:3306/mybatis");
pooledDataSource.setUsername("kys");
pooledDataSource.setPassword("password");
//构建数据库事物方式
TransactionFactory transactionFactory = new JdbcTransactionFactory();
//创建数据库运行环境
Environment environment = new Environment("development", transactionFactory, pooledDataSource);
//构建configuration对象
Configuration configuration = new Configuration(environment);
//注册别名
configuration.getTypeAliasRegistry().registerAlias("xxx", xxx.class);
//添加映射文件等
configuration.addMapper(xxx.class);
//等等。。。。
SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(configuration);
```

2. 使用xml文档 输入流实现

```java
String resource = "org/mybatis/builder/mybatis-config.xml";
InputStream inputStream = Resources.getResourceAsStream(resource);
SqlSessionFactoryBuilder builder = new SqlSessionFactoryBuilder();
SqlSessionFactory factory = builder.build(inputStream);
```

####  SqlSessionFactory 创建SqlSession实例

```java
SqlSession openSession()
SqlSession openSession(boolean autoCommit)  //是否自动提交
SqlSession openSession(Connection connection) 
SqlSession openSession(TransactionIsolationLevel level)  //事物隔离级别
SqlSession openSession(ExecutorType execType,TransactionIsolationLevel level)
SqlSession openSession(ExecutorType execType)  // 预处理问题
SqlSession openSession(ExecutorType execType, boolean autoCommit)
SqlSession openSession(ExecutorType execType, Connection connection)
Configuration getConfiguration();
```

**相关参数配置：**

1. 事物隔离级别

NONE(无),READ_UNCOMMITTED(读未提交),READ_COMMITTED(读已提交),REPEA TABLE_READ(可重复阅读),SERIALIZA BLE(序列化)

2. ExecutorType(执行方式)

- ExecutorType.SIMPLE: 这个执行器类型不做特殊的事情。它为每个语句的执行创建一个新的预处理语句。
- ExecutorType.REUSE: 这个执行器类型会复用预处理语句。
- ExecutorType.BATCH: 这个执行器会批量执行所有更新语句,如果 - - SELECT 在它们中间执行还会标定它们是 必须的,来保证一个简单并易于理解的行为。

#### SqlSession 最核心的会话操作类

1. 语句执行方法

这些方法被用来执行定义在 SQL 映射的 XML 文件中的 SELECT,INSERT,UPDA E T 和 DELETE 语句。它们都会自行解释,每一句都使用语句的 ID 属性和参数对象,参数可以 是原生类型(自动装箱或包装类) ,JavaBean,POJO 或 Map。

```java
<T> T selectOne(String statement, Object parameter)
<E> List<E> selectList(String statement, Object parameter)
<K,V> Map<K,V> selectMap(String statement, Object parameter, String mapKey)
int insert(String statement, Object parameter)
int update(String statement, Object parameter)
int delete(String statement, Object parameter)
```

**注意**：selectOne 和 selectList 的不同仅仅是 selectOne 必须返回一个对象。 如果多余一个, 或者 没有返回 (或返回了 null) 那么就会抛出异常。 , 如果你不知道需要多少对象, 使用 selectList。

最后,还有查询方法的三个高级版本,它们允许你限制返回行数的范围,或者提供自定 义结果控制逻辑,这通常用于大量的数据集合。

```java
<E> List<E> selectList (String statement, Object parameter, RowBounds rowBounds)
<K,V> Map<K,V> selectMap(String statement, Object parameter, String mapKey, RowBounds rowbounds)
void select (String statement, Object parameter, ResultHandler<T> handler)
void select (String statement, Object parameter, RowBounds rowBounds, ResultHandler<T> handler)
```

> RowBounds 参数会告诉 MyBatis 略过指定数量的记录,还有限制返回结果的数量。 

```java
int offset = 100;  //返回结果集的数量
int limit = 25;    //忽略掉的行数
RowBounds rowBounds = new RowBounds(offset, limit);
```

> ResultHandler 参数允许你按你喜欢的方式处理每一行。

它的接口很简单。
```java
package org.apache.ibatis.session;
public interface ResultHandler<T> {
  void handleResult(ResultContext<? extends T> context);
}
```

ResultContext 参数允许你访问结果对象本身、被创建的对象数目、以及返回值为 Boolean 的 stop 方法，你可以使用此 stop 方法来停止 MyBatis 加载更多的结果。
使用 ResultHandler 的时候需要注意以下两种限制：

- 从被 ResultHandler 调用的方法返回的数据不会被缓存。
- 当使用结果映射集（resultMap）时，MyBatis 大多数情况下需要数行结果来构造外键对象。如果你正在使用 ResultHandler，你可以给出外键（association）或者集合（collection）尚未赋值的对象。

2. 批量立即更新方法(Flush Method)

有一个方法可以刷新（执行）存储在JDBC驱动类中的批量更新语句。当你将ExecutorType.BATCH作为ExecutorType使用时可以采用此方法。

```java
List<BatchResult> flushStatements() 
```

3. 事务控制方法

**注意**：如果你已经选择了自动提交或你正在使用外部事务管理器,这就没有任何效果了

```java
void commit()
void commit(boolean force)
void rollback()
void rollback(boolean force)
```

4. 清理Session级的缓存

```java
List<BatchResult> void clearCache() 
```

SqlSession 实例有一个本地缓存在执行 update,commit,rollback 和 close 时被清理。要 明确地关闭它(获取打算做更多的工作) ,你可以调用 clearCache()。

5. 确保 SqlSession 被关闭

```java
List<BatchResult> void close() 
````

```java
SqlSession session = sqlSessionFactory.openSession();
try {
    // following 3 lines pseudocod for "doing some work"
    session.insert(...);
    session.update(...);
    session.delete(...);
    session.commit();
} finally {
    session.close();
}
//java7以上使用try-with-resources语句
try (SqlSession session = sqlSessionFactory.openSession()) {
    // following 3 lines pseudocode for "doing some work"
    session.insert(...);
    session.update(...);
    session.delete(...);
    session.commit();
}
```

6. 高级应用 使用映射器 和常用注释操作

type是mybatis的映射器类，是一个java接口，可以将接口类比成mybatis的map文件，包名称相当于xml中的namespace，而 select delete insert update 中的id属性 对应的 接口中的方法

最常用注解，用来进行动态的注入属性

|注解|使用对象|相对应的XML|描述|
|---|---|---|---|
|@CacheNamespace|类|&lt;cache&gt;|为给定的命名空间（比如类）配置缓存。属性有：implemetation,eviction,flushInterval,size,readWrite,blocking和properties。|
|@Property|N/A|&lt;property&gt;|指定参数值或占位值（placeholder）（能被mybatis-config.xml内的配置属性覆盖）。属性有：name,value。（仅在MyBatis3.4.2以上版本生效）|
|@CacheNamespaceRef|类|&lt;cacheRef&gt;|参照另外一个命名空间的缓存来使用。属性有：value,name。如果你使用了这个注解，你应设置value或者name属性的其中一个。value属性用于指定Java类型而指定命名空间（命名空间名就是指定的Java类型的全限定名），name属性（这个属性仅在MyBatis3.4.2以上版本生效）直接指定了命名空间的名字。|
|@ConstructorArgs|方法|&lt;constructor&gt;|收集一组结果传递给一个结果对象的构造方法。属性有：value，它是形式参数数组。|
|@Arg|N/A|&lt;arg&gt;|单参数构造方法，是ConstructorArgs集合的一部分。属性有：id,column,javaType,jdbcType,typeHandler,select和resultMap。id属性是布尔值，来标识用于比较的属性，和&lt;idArg&gt;XML元素相似。|
|&lt;idArg&gt;||||
|@TypeDiscriminator|方法|&lt;discriminator&gt;|一组实例值被用来决定结果映射的表现。属性有：column,javaType,jdbcType,typeHandler和cases。cases属性是实例数组。|
|@Case|N/A|&lt;case&gt;|单独实例的值和它对应的映射。属性有：value,type,results。results属性是结果数组，因此这个注解和实际的ResultMap很相似，由下面的Results注解指定。|
|@Results|方法|&lt;resultMap&gt;|结果映射的列表，包含了一个特别结果列如何被映射到属性或字段的详情。属性有：value,id。value属性是Result注解的数组。这个id的属性是结果映射的名称。|
|@Result|N/A|&lt;result&gt;|在列和属性或字段之间的单独结果映射。属性有：id,column,javaType,jdbcType,typeHandler,one,many。id属性是一个布尔值，来标识应该被用于比较（和在XML映射中的&lt;id&gt;相似）的属性。one属性是单独的联系，和&lt;association&gt;相似，而many属性是对集合而言的，和&lt;collection&gt;相似。它们这样命名是为了避免名称冲突。|
|&lt;id&gt;||||
|@One|N/A|&lt;association&gt;|复杂类型的单独属性值映射。属性有：select，已映射语句（也就是映射器方法）的全限定名，它可以加载合适类型的实例。fetchType会覆盖全局的配置参数lazyLoadingEnabled。注意联合映射在注解API中是不支持的。这是因为Java注解的限制,不允许循环引用。|
|@Many|N/A|&lt;collection&gt;|映射到复杂类型的集合属性。属性有：select，已映射语句（也就是映射器方法）的全限定名，它可以加载合适类型的实例的集合，fetchType会覆盖全局的配置参数lazyLoadingEnabled。注意联合映射在注解API中是不支持的。这是因为Java注解的限制，不允许循环引用|
|@MapKey|方法||这是一个用在返回值为Map的方法上的注解。它能够将存放对象的List转化为key值为对象的某一属性的Map。属性有：value，填入的是对象的属性名，作为Map的key值。|
|@Options|方法|映射语句的属性|这个注解提供访问大范围的交换和配置选项的入口，它们通常在映射语句上作为属性出现。Options注解提供了通俗易懂的方式来访问它们，而不是让每条语句注解变复杂。属性有：useCache=true,flushCache=FlushCachePolicy.DEFAULT,resultSetType=FORWARD_ONLY,statementType=PREPARED,fetchSize=-1,timeout=-1,useGeneratedKeys=false,keyProperty="id",keyColumn="",resultSets=""。值得一提的是，Java注解无法指定null值。因此，一旦你使用了Options注解，你的语句就会被上述属性的默认值所影响。要注意避免默认值带来的预期以外的行为。|
|||||
|注意：keyColumn属性只在某些数据库中有效（如Oracle、PostgreSQL等）。请在插入语句一节查看更多关于keyColumn和keyProperty两者的有效值详情。||||
|@Insert|方法|&lt;insert&gt;|这四个注解分别代表将会被执行的SQL语句。它们用字符串数组（或单个字符串）作为参数。如果传递的是字符串数组，字符串之间先会被填充一个空格再连接成单个完整的字符串。这有效避免了以Java代码构建SQL语句时的“丢失空格”的问题。然而，你也可以提前手动连接好字符串。属性有：value，填入的值是用来组成单个SQL语句的字符串数组。|
|@Update|&lt;update&gt;|||
|@Delete|&lt;delete&gt;|||
|@Select|&lt;select&gt;|||
|@InsertProvider|方法|&lt;insert&gt;|允许构建动态SQL。这些备选的SQL注解允许你指定类名和返回在运行时执行的SQL语句的方法。（自从MyBatis3.4.6开始，你可以用CharSequence代替String来返回类型返回值了。）当执行映射语句的时候，MyBatis会实例化类并执行方法，类和方法就是填入了注解的值。你可以把已经传递给映射方法了的对象作为参数，"Mapperinterfacetype"和"Mappermethod"会经过ProviderContext（仅在MyBatis3.4.5及以上支持）作为参数值。（MyBatis3.4及以上的版本，支持多参数传入）属性有：type,method。type属性需填入类。method需填入该类定义了的方法名。注意接下来的小节将会讨论类，能帮助你更轻松地构建动态SQL。|
|@UpdateProvider|&lt;update&gt;|||
|@DeleteProvider|&lt;delete&gt;|||
|@SelectProvider|&lt;select&gt;|||
|@Param|参数|N/A|如果你的映射方法的形参有多个，这个注解使用在映射方法的参数上就能为它们取自定义名字。若不给出自定义名字，多参数（不包括RowBounds参数）则先以"param"作前缀，再加上它们的参数位置作为参数别名。例如#{param1},#{param2}，这个是默认值。如果注解是@Param("person")，那么参数就会被命名为#{person}。|
|@SelectKey|方法|&lt;selectKey&gt;|这个注解的功能与&lt;selectKey&gt;标签完全一致，用在已经被@Insert或@InsertProvider或@Update或@UpdateProvider注解了的方法上。若在未被上述四个注解的方法上作@SelectKey注解则视为无效。如果你指定了@SelectKey注解，那么MyBatis就会忽略掉由@Options注解所设置的生成主键或设置（configuration）属性。属性有：statement填入将会被执行的SQL字符串数组，keyProperty填入将会被更新的参数对象的属性的值，before填入true或false以指明SQL语句应被在插入语句的之前还是之后执行。resultType填入keyProperty的Java类型和用Statement、PreparedStatement和CallableStatement中的STATEMENT、PREPARED或CALLABLE中任一值填入statementType。默认值是PREPARED。|
|@ResultMap|方法|N/A|这个注解给@Select或者@SelectProvider提供在XML映射中的&lt;resultMap&gt;的id。这使得注解的select可以复用那些定义在XML中的ResultMap。如果同一select注解中还存在@Results或者@ConstructorArgs，那么这两个注解将被此注解覆盖。|
|@ResultType|方法|N/A|此注解在使用了结果处理器的情况下使用。在这种情况下，返回类型为void，所以Mybatis必须有一种方式决定对象的类型，用于构造每行数据。如果有XML的结果映射，请使用@ResultMap注解。如果结果类型在XML的&lt;select&gt;节点中指定了，就不需要其他的注解了。其他情况下则使用此注解。比如，如果@Select注解在一个将使用结果处理器的方法上，那么返回类型必须是void并且这个注解（或者@ResultMap）必选。这个注解仅在方法返回类型是void的情况下生效。|
|@Flush|方法|N/A|如果使用了这个注解，定义在Mapper接口中的方法能够调用SqlSession#flushStatements()方法。（Mybatis3.3及以上）|