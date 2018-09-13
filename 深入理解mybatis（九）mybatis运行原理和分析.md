### mybatis 构建过程

#### sessionfactory 构建sqlsession

mybatis 使用sqlSession同数据库进行相关的操作所以在使用之前需要获取这个类，在mybatis 中使用sessionfactory 进行

通常情况下，mybatis使用的是SqlSessionFactoryBuilder的builder方法获取sessionfacotry ，其实这是一种封装，查看源代码可知，其实他是封装了一个DefaultSqlSessionFactory类,通过传入的Config进行初始化的

```java
public class SqlSessionFactoryBuilder {
  public SqlSessionFactory build(Reader reader) {return build(reader, null, null);}
  public SqlSessionFactory build(Reader reader, String environment) {return build(reader, environment, null);}
  public SqlSessionFactory build(Reader reader, Properties properties) {return build(reader, null, properties);}
  public SqlSessionFactory build(InputStream inputStream) {return build(inputStream, null, null);}
  public SqlSessionFactory build(InputStream inputStream, String environment) {return build(inputStream, environment, null);}
  public SqlSessionFactory build(InputStream inputStream, Properties properties) {return build(inputStream, null, properties);}
  public SqlSessionFactory build(Reader reader, String environment, Properties properties) {
    try {
      XMLConfigBuilder parser = new XMLConfigBuilder(reader, environment, properties);
      return build(parser.parse());
    } catch (Exception e) {
      throw ExceptionFactory.wrapException("Error building SqlSession.", e);
    } finally {
      ErrorContext.instance().reset();
      try {
        reader.close();
      } catch (IOException e) {
        // Intentionally ignore. Prefer previous error.
      }
    }
  }
  public SqlSessionFactory build(InputStream inputStream, String environment, Properties properties) {
    try {
      XMLConfigBuilder parser = new XMLConfigBuilder(inputStream, environment, properties);
      return build(parser.parse());
    } catch (Exception e) {
      throw ExceptionFactory.wrapException("Error building SqlSession.", e);
    } finally {
      ErrorContext.instance().reset();
      try {
        inputStream.close();
      } catch (IOException e) {
        // Intentionally ignore. Prefer previous error.
      }
    }
  } 
  public SqlSessionFactory build(Configuration config) {
    return new DefaultSqlSessionFactory(config);
  }
}
```

> 其实通过上面的分析就能知道其实在使用的Configuration类（这个类包含了mybatis几乎所有的配置），来初始化SqlSessionfacotory的

#### configuration对象

mybatis总体的配置文件包括如下的部分

- propertise：参数名称
- setting ：设置
- typeAliases：别名
- typeHandler：类型处理器
- ObjectFacotry: 返回值处理工厂对象
- plugin：插件
- enviroment：环境变量
- DataBaseIdProivder：数据库标识
- Mapper：映射器


### mybatis最核心运行过程SqlSession

首先看一下SqlSession这个接口的源代码

```java
public interface SqlSession extends Closeable {
    <T> T selectOne(String statement);
    <T> T selectOne(String statement, Object parameter);
    。。。。。
    <T> T getMapper(Class<T> type);
}
```

SqlSession定义了对数据库的基本操作，CURD操作，其中有一个方法需要注意getMapper 这个方法将会返回一个Mapper接口对象，通过这个对象的方法就可以进行增删改从而并不需要使用原来的方法进行处理,mapper此时就成为操作数据库的方法了，接下来分析一下mapper

#### 深入分析mapper初始化机制

> mybatis的mapper是在一开始的时候就通过config就生成了

留心configuration 对象中的mapperRegistry 这个属性的对象，mybatis初始化所有的mapper都储存在这个对象之中

```java
public class Configuration{
    public void addMappers(String packageName, Class<?> superType) {
        mapperRegistry.addMappers(packageName, superType);
    }
    public void addMappers(String packageName) {
        mapperRegistry.addMappers(packageName);
    }
    public <T> void addMapper(Class<T> type) {
        mapperRegistry.addMapper(type);
    }
}
```

跟进addMapper方法可以发现，这个方法的处理方式其实是让class作为健，生成一个新的代理对象MapperProxyFactory作为值值存入knownMappers这个HashMap

```java
public <T> void addMapper(Class<T> type) {
    if (type.isInterface()) {
        if (hasMapper(type)) {
            throw new BindingException("Type " + type + " is already known to the MapperRegistry.");
        }
        boolean loadCompleted = false;
        try {
            knownMappers.put(type, new MapperProxyFactory<T>(type));
            // It's important that the type is added before the parser is run
            // otherwise the binding may automatically be attempted by the
            // mapper parser. If the type is already known, it won't try.
            MapperAnnotationBuilder parser = new MapperAnnotationBuilder(config, type);
            parser.parse();
            loadCompleted = true;
        } finally {
            if (!loadCompleted) {
                knownMappers.remove(type);
            }
        }
    }
}
```

#### 深入分析mapper的初始化调用机制

在SqlSession.getMapper获取Mapper的时候同样是通过这个方式反方向方法获取MapperProxyFactory这个对象

```java
public <T> T getMapper(Class<T> type, SqlSession sqlSession) {
    final MapperProxyFactory<T> mapperProxyFactory = (MapperProxyFactory<T>) knownMappers.get(type);
    if (mapperProxyFactory == null) {
        throw new BindingException("Type " + type + " is not known to the MapperRegistry.");
    }
    try {
        return mapperProxyFactory.newInstance(sqlSession);
    } catch (Exception e) {
        throw new BindingException("Error getting mapper instance. Cause: " + e, e);
    }
}
```

从代码中可以看看出来其实此时使用的mapper是通过proxyfactory生成的代理对象

```java
public class MapperProxyFactory<T> {
  。。。
  protected T newInstance(MapperProxy<T> mapperProxy) {
    return (T) Proxy.newProxyInstance(mapperInterface.getClassLoader(), new Class[] { mapperInterface }, mapperProxy);
  }
  public T newInstance(SqlSession sqlSession) {
    final MapperProxy<T> mapperProxy = new MapperProxy<T>(sqlSession, mapperInterface, methodCache);
    return newInstance(mapperProxy);
  }
}
```

我们都知道代理是指定invoke方法来实现回调的这里我们跟进一下看一下mapperProxy的代码

```java
public class MapperProxy<T> implements InvocationHandler, Serializable {
  @Override
  public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
    try {
      if (Object.class.equals(method.getDeclaringClass())) {
        return method.invoke(this, args);
      } else if (isDefaultMethod(method)) {
        return invokeDefaultMethod(proxy, method, args);
      }
    } catch (Throwable t) {
      throw ExceptionUtil.unwrapThrowable(t);
    }
    final MapperMethod mapperMethod = cachedMapperMethod(method);
    return mapperMethod.execute(sqlSession, args);
  }
}
```

其实跟踪到这里已经非常明确的 其实他是使用了mapperMethod.execute(sqlSession, args)来执行语句，看一下

```java
public Object execute(SqlSession sqlSession, Object[] args) {
    Object result;
    switch (command.getType()) {
      case INSERT: {
      Object param = method.convertArgsToSqlCommandParam(args);
        result = rowCountResult(sqlSession.insert(command.getName(), param));
        break;
      }
     。。。。。
    return result;
  }
```

代码逻辑非常清晰其实就是使用sqlSession的对应方法，mapper的报名加上类名构成了一开始的名称

####　分析SqlSession运行相关数据库操作的详细分析

通过源代码分析其实最终情况下sql将操作分成了两种类型 doupdate类型和query这里先看一下query

```java
public <E> List<E> query(MappedStatement ms, Object parameter, RowBounds rowBounds, ResultHandler resultHandler, CacheKey key, BoundSql boundSql) throws SQLException {
  ErrorContext.instance().resource(ms.getResource()).activity("executing a query").object(ms.getId());
//如果已经关闭，报错
  if (closed) throw new ExecutorException("Executor was closed.");
//先清局部缓存，再查询，但仅仅查询堆栈为0才清，为了处理递归调用
  if (queryStack == 0 && ms.isFlushCacheRequired()) {
    clearLocalCache();
  }
  List<E> list;
  try {
  //加一，这样递归调用到上面的时候就不会再清局部缓存了
    queryStack++;
  //根据cachekey从localCache去查
    list = resultHandler == null ? (List<E>) localCache.getObject(key) : null;
    if (list != null) {
  //如果查到localCache缓存，处理localOutputParameterCache
      handleLocallyCachedOutputParameters(ms, key, parameter, boundSql);
    } else {
  //从数据库查
      list = queryFromDatabase(ms, parameter, rowBounds, resultHandler, key, boundSql);
    }
  } finally {
  //清空堆栈
    queryStack--;
  }
  if (queryStack == 0) {
  //延迟加载队列中所有元素
    for (DeferredLoad deferredLoad : deferredLoads) {
      deferredLoad.load();
    }
  //清空延迟加载队列
    deferredLoads.clear(); // issue #601
    if (configuration.getLocalCacheScope() == LocalCacheScope.STATEMENT) {
  //如果是statement，清本地缓存
      clearLocalCache(); // issue #482
    }
  }
  return list;
}
```

真正执行相关的query操作的方法是deQuery方法(executor类的doQuery)

```java
@Override
public <E> List<E> doQuery(MappedStatement ms, Object parameter, RowBounds rowBounds, ResultHandler resultHandler, BoundSql boundSql) throws SQLException {
  Statement stmt = null;
  try {
    Configuration configuration = ms.getConfiguration();
    StatementHandler handler = configuration.newStatementHandler(wrapper, ms, parameter, rowBounds, resultHandler, boundSql);
    stmt = prepareStatement(handler, ms.getStatementLog());
    return handler.<E>query(stmt, resultHandler);
  } finally {
    closeStatement(stmt);
  }
}
```

从上面的方法中我们可以看见一个方法叫MappedStatement,观察一下他的产生

#### MappedStatement 产生过程

通过获取方法可以判断出,这个类其实是一开就在configration配置成功的

```java
MappedStatement ms = configuration.getMappedStatement(statement);
```

如果跟踪一开始初始化的状态需要跟踪到SqlSessionFactoryBuilder类中,一开始mybatiss将所有状态初始化的过程

SqlSessionFactoryBuilder在默认情况下会使用XMLConfigBuilder来生成configration

```java
public SqlSessionFactory build(Reader reader, String environment, Properties properties) {
  XMLConfigBuilder parser = new XMLConfigBuilder(reader, environment, properties);
  return build(parser.parse());
}
```

接下来跟踪进去发现了初始化一个类XPathParser,并且使用嵌套构造函数的方法进行方法嵌套使用

```java
public XMLConfigBuilder(Reader reader, String environment, Properties props) {
  this(new XPathParser(reader, true, props, new XMLMapperEntityResolver()), environment, props);
}

private XMLConfigBuilder(XPathParser parser, String environment, Properties props) {
  super(new Configuration());
  ErrorContext.instance().resource("SQL Mapper Configuration");
  this.configuration.setVariables(props);
  this.parsed = false;
  this.environment = environment;
  this.parser = parser;
}
```

> 这个类其实就是将xml文件整理成node节点的形式方便之后的调用,其实是一个解析用的工具

然后上调用者(sqlSessionFactoryBuilder)将会调用XMLConfigBuilder的parse方法进行生产configration对象这里才是整个mybatis配置真正产生的地方


```java
public Configuration parse() {
  if (parsed) {
    throw new BuilderException("Each XMLConfigBuilder can only be used once.");
  }
  parsed = true;
  parseConfiguration(parser.evalNode("/configuration"));
  return configuration;
}
//所有的配置都是在这里生成的
private void parseConfiguration(XNode root) {
  try {
    //issue #117 read properties first
    propertiesElement(root.evalNode("properties"));
    Properties settings = settingsAsProperties(root.evalNode("settings"));
    loadCustomVfs(settings);
    typeAliasesElement(root.evalNode("typeAliases"));
    pluginElement(root.evalNode("plugins"));
    objectFactoryElement(root.evalNode("objectFactory"));
    objectWrapperFactoryElement(root.evalNode("objectWrapperFactory"));
    reflectorFactoryElement(root.evalNode("reflectorFactory"));
    settingsElement(settings);
    // read it after objectFactory and objectWrapperFactory issue #631
    environmentsElement(root.evalNode("environments"));
    databaseIdProviderElement(root.evalNode("databaseIdProvider"));
    typeHandlerElement(root.evalNode("typeHandlers"));
    mapperElement(root.evalNode("mappers"));
  } catch (Exception e) {
    throw new BuilderException("Error parsing SQL Mapper Configuration. Cause: " + e, e);
  }
}
```

终于到了关键的地方MappedStatement的生成部分,MappedStatement由名称就能知道是从mapperElement()方法中产生的

在XMLConfigBuilder中定义的这个方法

```java
private void mapperElement(XNode parent) throws Exception {
  if (parent != null) {
    for (XNode child : parent.getChildren()) {
      if ("package".equals(child.getName())) {
        String mapperPackage = child.getStringAttribute("name");
        configuration.addMappers(mapperPackage);
      }
  }
}
```

我截取了一段代码这段代码是处理使用包名扫描mapper的代码,进入到其中的configuration.addMappers(mapperPackage);方法,发现这里使用了configration中的addMappers方法,进入到mapperRegistry类的这个方法中

```java
public void addMappers(String packageName) {
  mapperRegistry.addMappers(packageName);
}
```

跟踪到这里其实思路比较清晰了,这里就是初始化一个mapper和mapper中各种mathod的地方（MapperRegistry）

> 注意到MapperStatues和Method是一一对应的

```java
public <T> void addMapper(Class<T> type) {
  if (type.isInterface()) {
    if (hasMapper(type)) {
      throw new BindingException("Type " + type + " is already known to the MapperRegistry.");
    }
    boolean loadCompleted = false;
    try {
      knownMappers.put(type, new MapperProxyFactory<T>(type));
      MapperAnnotationBuilder parser = new MapperAnnotationBuilder(config, type);
      parser.parse();
      loadCompleted = true;
    } finally {
      if (!loadCompleted) {
        knownMappers.remove(type);
      }
    }
  }
}
```

而MappedStatement的初始化就在这个MapperAnnotationBuilder.parse()

```java
public void parse() {
  String resource = type.toString();
  if (!configuration.isResourceLoaded(resource)) {
    loadXmlResource();
    configuration.addLoadedResource(resource);
    assistant.setCurrentNamespace(type.getName());
    parseCache();
    parseCacheRef();
    Method[] methods = type.getMethods();
    for (Method method : methods) {
      try {
        // issue #237
        if (!method.isBridge()) {
          parseStatement(method);
        }
      } catch (IncompleteElementException e) {
        configuration.addIncompleteMethod(new MethodResolver(this, method));
      }
    }
  }
  parsePendingMethods();
}
```

```java
void parseStatement(Method method) {
  Class<?> parameterTypeClass = getParameterType(method);
  LanguageDriver languageDriver = getLanguageDriver(method);
  SqlSource sqlSource = getSqlSourceFromAnnotations(method, parameterTypeClass, languageDriver);
  if (sqlSource != null) {
    Options options = method.getAnnotation(Options.class);
    final String mappedStatementId = type.getName() + "." + method.getName();
    Integer fetchSize = null;
    Integer timeout = null;
    StatementType statementType = StatementType.PREPARED;
    ResultSetType resultSetType = ResultSetType.FORWARD_ONLY;
    SqlCommandType sqlCommandType = getSqlCommandType(method);
    boolean isSelect = sqlCommandType == SqlCommandType.SELECT;
    boolean flushCache = !isSelect;
    boolean useCache = isSelect;
    KeyGenerator keyGenerator;
    String keyProperty = "id";
    String keyColumn = null;
    if (SqlCommandType.INSERT.equals(sqlCommandType) || SqlCommandType.UPDATE.equals(sqlCommandType)) {
      // first check for SelectKey annotation - that overrides everything else
      SelectKey selectKey = method.getAnnotation(SelectKey.class);
      if (selectKey != null) {
        keyGenerator = handleSelectKeyAnnotation(selectKey, mappedStatementId, getParameterType(method), languageDriver);
        keyProperty = selectKey.keyProperty();
      } else if (options == null) {
        keyGenerator = configuration.isUseGeneratedKeys() ? Jdbc3KeyGenerator.INSTANCE : NoKeyGenerator.INSTANCE;
      } else {
        keyGenerator = options.useGeneratedKeys() ? Jdbc3KeyGenerator.INSTANCE : NoKeyGenerator.INSTANCE;
        keyProperty = options.keyProperty();
        keyColumn = options.keyColumn();
      }
    } else {
      keyGenerator = NoKeyGenerator.INSTANCE;
    }
    if (options != null) {
      if (FlushCachePolicy.TRUE.equals(options.flushCache())) {
        flushCache = true;
      } else if (FlushCachePolicy.FALSE.equals(options.flushCache())) {
        flushCache = false;
      }
      useCache = options.useCache();
      fetchSize = options.fetchSize() > -1 || options.fetchSize() == Integer.MIN_VALUE ? options.fetchSize() : null; //issue #348
      timeout = options.timeout() > -1 ? options.timeout() : null;
      statementType = options.statementType();
      resultSetType = options.resultSetType();
    }
    String resultMapId = null;
    ResultMap resultMapAnnotation = method.getAnnotation(ResultMap.class);
    if (resultMapAnnotation != null) {
      String[] resultMaps = resultMapAnnotation.value();
      StringBuilder sb = new StringBuilder();
      for (String resultMap : resultMaps) {
        if (sb.length() > 0) {
          sb.append(",");
        }
        sb.append(resultMap);
      }
      resultMapId = sb.toString();
    } else if (isSelect) {
      resultMapId = parseResultMap(method);
    }
    assistant.addMappedStatement(
        mappedStatementId,
        sqlSource,
        statementType,
        sqlCommandType,
        fetchSize,
        timeout,
        // ParameterMapID
        null,
        parameterTypeClass,
        resultMapId,
        getReturnType(method),
        resultSetType,
        flushCache,
        useCache,
        // TODO gcode issue #577
        false,
        keyGenerator,
        keyProperty,
        keyColumn,
        // DatabaseID
        null,
        languageDriver,
        // ResultSets
        options != null ? nullOrEmpty(options.resultSets()) : null);
  }
}
```

从上面我们就可以得出MapperStatement的作用就是配置一个sql的各种信息，比如操作方法（select|upadte等），配置的sql ， sql的id ，缓存信息，resultMap，parameterType，resultType，languageDriver，等