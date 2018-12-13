## java-jdbc驱动使用详解（一）基本使用方法

大多数时候我都都是使用mybatis 或者数据库链接池这样的框架，渐渐对底层jdbc驱动缺少研究这里一下整理

### 驱动驱动加载

```java
Class.forName("com.mysql.jdbc.Driver");
```

jvm在运行的时候，必须手动加载jdbc的驱动程序，因为jvm不会自动导入驱动，导致DriverManager无法使用

### Connection 链接

> 建立和数据库的链接（java程序一般使用数据链接池，这里只是做一些基本的介绍）

> 链接方法：直接设置或者使用Property

1. 创建方法

```java
Properties properties= new Properties();
properties.setProperty("xxx", "xxx");
Connection connection =DriverManager.getConnection("xxx",properties);
Connection connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/mysql", "root","****");
```

2. 链接控制

```java
connection.getClientInfo("root");//获得数据连接中的指定参数比如上面的
connection.setClientInfo(new Properties());
connection.setReadOnly(true);//设置数据库只读
connection.setAutoCommit(false);//关闭自动提交
connection.commit();//提交事物
connection.rollback();//事物回滚
connection.close();//关闭数据库
```

3. 链接状态检测

```java
connection.isReadOnly();//是否只读
connection.isClosed();//判断对象是否关闭了
```

### 数据库交互 statement

jdbc中有三种交互方法

- Statement 使用通用访问数据库。当在运行时使用静态SQL语句。 Statement接口不能接受的参数。
- PreparedStatement 当计划多次使用SQL语句。 那么可以PreparedStatement接口接收在运行时输入参数。
- CallableStatement 当要访问数据库中的存储过程中使用。 CallableStatement对象的接口还可以接受运行时输入参数

1. statement对象，一般不使用，一般做心跳检测的时候使用


```java
Statement statement = connection.createStatement();
statement.execute("");//执行任何语句判断是否有result结果集有就返回投入哦否则返回false
statement.executeUpdate("sdfasfd");//传入sql语句并且返回返回收到影响的行数
statement.executeQuery("sdf");//传入结果集并且返回resultset结果集对象
```

2. PreparedStatement — statement升级版可以使用占位符 和进行批处理操作

```java
preparedStatement.setString(0, "sdf");
preparedStatement.setString(2, "sdf");
preparedStatement.setString(0, "sdf");
preparedStatement.setString(0, "sdf");
preparedStatement.addBatch();
preparedStatement.executeBatch();//提交批量操作
```

### jdbc结果集操作

1. 声明结果集的类型  在statement的生成方法可以进行很多的配置参数 Rstyoe RsConcurrency都是ResultSet中指定的类型

```java
createStatement(int RSType, int RSConcurrency);
prepareStatement(String SQL, int RSType, int RSConcurrency);
prepareCall(String sql, int RSType, int RSConcurrency);
```

2. ResultSet的类型 RSType

可能的RSType如下，如果不指定ResultSet类型，将自动获得一个是TYPE_FORWARD_ONLY。

Type 描述:

- ResultSet.TYPE_FORWARD_ONLY 游标只能向前移动的结果集。
- ResultSet.TYPE_SCROLL_INSENSITIVE 游标可以向前和向后滚动，结果集不是别人向创建结果集后发生的数据库更改敏感。
- ResultSet.TYPE_SCROLL_SENSITIVE. 游标可以向前和向后滚动，结果集是别人向创建结果集后发生的数据库更改敏感。

3. 并发性的ResultSe RSConcurrencyt

可能的RSConcurrency如下，如果不指定任何并发类型，将自动获得一个为CONCUR_READ_ONLY。

并发 描述:
- ResultSet.CONCUR_READ_ONLY 创建结果集只读。这是默认的
- ResultSet.CONCUR_UPDATABLE 创建一个可更新的结果集。

结果集相关方法:

```java
ResultSet resultSet = preparedStatement.executeQuery("asdasd");
```

1. 使用可滚动结果集相关属性 需要指定 Resultset相关配置

```java
resultSet.absolute(10);//游标定位到指定的位置
resultSet.relative(-10);//游标向前向后移动指定的行
resultSet.previous();
resultSet.next();
resultSet.getRow();//获得行号
```

2. 并发性（可修改结果集相关配置）

```java
//更行数据库中的数据---在可进行更新的结果集中进行的修改
resultSet.updateInt("s", 0);//-----进行修改---参数有很多updateString  第一个参数列名称 第二个参数 数值
resultSet.updateRow();//提交updatexx事物
resultSet.deleteRow();//删除数据库中的当前行---刷新后生效
resultSet.insertRow();//提交updatexx事物----使用插入方法
resultSet.refreshRow();//刷新
resultSet.cancelRowUpdates();//取消
```

3. 结果集通用方法

```java
//指定结果集所在的位置
resultSet.beforeFirst();
resultSet.afterLast();
resultSet.first();
resultSet.last();
//获得结果集中的数据
resultSet.getInt("sdfsdf");
resultSet.getInt(0);
//结果集状态
resultSet.isAfterLast();
resultSet.isBeforeFirst();
resultSet.isClosed();
resultSet.isFirst();
resultSet.isClosed();
```

