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

RowBounds 参数会告诉 MyBatis 略过指定数量的记录,还有限制返回结果的数量。 

```java
int offset = 100;  //返回结果集的数量
int limit = 25;    //忽略掉的行数
RowBounds rowBounds = new RowBounds(offset, limit);
```

2. 批量立即更新方法(Flush Method)

有一个方法可以刷新（执行）存储在JDBC驱动类中的批量更新语句。当你将ExecutorType.BATCH作为ExecutorType使用时可以采用此方法。

```java
List<BatchResult> flushStatements() 
```

3. 事务控制方法

**注意**：如果你已经选择了自动提交或你正在使用外部事务管 理器,这就没有任何效果了

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

|||||
---|---|---|---
@Param|Parameter|N/A|如果你的映射器的方法需要多个参数, 这个注解可以被应用于映射器的方法 参数来给每个参数一个名字。否则,多 参数将会以它们的顺序位置来被命名 (不包括任何 RowBounds 参数) 比如。 #{param1} , #{param2} 等 , 这 是 默 认 的 。 使 用 @Param(“person”),参数应该被命名为 #{person}。

