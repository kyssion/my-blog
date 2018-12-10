**数据库连接池druid配置详解**

### druid的配置项详解 

|配置|缺省值|说明|
|--|--|--|
|name|无|配置这个属性的意义在于，如果存在多个数据源，监控的时候可以通过名字来区分开来。如果没有配置，将会生成一个名字， 格式是：”DataSource-” + System.identityHashCode(this)|
dbcUrl|无|连接数据库的url，不同数据库不一样。例如：mysql : jdbc:mysql://10.20.153.104:3306/druid2  oracle : jdbc:oracle:thin:@10.20.149.85:1521:ocnauto
username|无|连接数据库的用户名
password|无|连接数据库的密码。如果你不希望密码直接写在配置文件中，可以使用ConfigFilter。详细看这里https://github.com/alibaba/druid/wiki/%E4%BD%BF%E7%94%A8ConfigFilter
driverClassName|根据url自动识别|这一项可配可不配，如果不配置druid会根据url自动识别dbType，然后选择相应的driverClassName
initialSize|0|初始化时建立物理连接的个数。初始化发生在显示调用init方法，或者第一次getConnection时
maxActive|8|最大连接池数量
maxIdle|8|已经不再使用，配置了也没效果
minIdle|无|最小连接池数量
maxWait|无|获取连接时最大等待时间，单位毫秒。配置了maxWait之后，缺省启用公平锁,并发效率会有所下降，如果需要可以通过配置useUnfairLock属性为true使用非公平锁。
poolPreparedStatements|false|是否缓存preparedStatement，也就是PSCache。PSCache对支持游标的数据库性能提升巨大，比如说oracle。在mysql5.5以下的版本中没有PSCache功能，建议关闭掉。作者在5.5版本中使用PSCache，通过监控界面发现PSCache有缓存命中率记录，该应该是支持PSCache。
maxOpenPreparedStatements|-1|要启用PSCache，必须配置大于0，当大于0时，poolPreparedStatements自动触发修改为true。在Druid中，不会存在Oracle下PSCache占用内存过多的问题， 可以把这个数值配置大一些，比如说100
validationQuery	||用来检测连接是否有效的sql，要求是一个查询语句。 如果validationQuery为null，testOnBorrowtestOnReturn、testWhileIdle都不会其作用。
testOnBorrow|true|申请连接时执行validationQuery检测连接是否有效，做了这个配置会降低性能。
testOnReturn|false|归还连接时执行validationQuery检测连接是否有效，做了这个配置会降低性能
testWhileIdle|false|建议配置为true，不影响性能，并且保证安全性。申请连接的时候检测，如果空闲时间大于timeBetweenEvictionRunsMillis，执行validationQuery检测连接是否有效。
timeBetweenEvictionRunsMillis|无|有两个含义： 1) Destroy线程会检测连接的间隔时间 2) testWhileIdle的判断依据，详细看testWhileIdle属性的说明
numTestsPerEvictionRun|无|不再使用，一个DruidDataSource只支持一个EvictionRun
minEvictableIdleTimeMillis|无| 一个连接在池中最小的生存时间，单位是毫秒
connectionInitSqls|无|物理连接初始化的时候执行的sql
exceptionSorter|根据dbType自动识别|当数据库抛出一些不可恢复的异常时，抛弃连接
filters|无|属性类型是字符串，通过别名的方式配置扩展插件，常用的插件有：监控统计用的filter:stat,日志用的filter:log4j,防御sql注入的filter:wall
proxyFilters|无|类型是List<com.alibaba.druid.filter.Filter>， 如果同时配置了filters和proxyFilters， 是组合关系，并非替换关系

### 配置示例

在spring配置文件中加入如下的配置，进行数据库链接池的信息配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
	 <bean id = "propertyConfigurer" class ="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer" >  
       <property name = "locations" >  
           <list>  
                 <value>/WEB-INF/classes/dbconfig.properties </value>  
            </list>  
        </property>  
    </bean>
	 <!-- 阿里 druid 数据库连接池 -->
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
    </bean >
</beans>
```

dbconfig.properties 配置文件的配置

```properties
url=jdbc:mysql://localhost:3306/newm
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

web 监控页面控制， 启动spring 之后 再运行 http://ip:port/projectName/druid/index.html.即可访问监控信息

```xml

<!-- 连接池 启用 Web 监控统计功能    start-->
    <filter >
       <filter-name > DruidWebStatFilter </filter-name >
       <filter-class > com.alibaba.druid.support.http.WebStatFilter </filter-class >
       <init-param >
           <param-name > exclusions </ param-name >
           <param-value > *. js ,*. gif ,*. jpg ,*. png ,*. css ,*. ico ,/ druid /* </param-value >
       </init-param >
    </filter >
 
    <filter-mapping >
       <filter-name > DruidWebStatFilter </filter-name >
       <url-pattern > /* </url-pattern >
    </filter-mapping >
 
    <servlet >
       <servlet-name > DruidStatView </servlet-name >
       <servlet-class > com.alibaba.druid.support.http.StatViewServlet </servlet-class >
    </servlet >
 
    <servlet-mapping >
       <servlet-name > DruidStatView </servlet-name >
       <url-pattern > / druid /* </url-pattern >
    </servlet-mapping >
<!-- 连接池 启用 Web 监控统计功能    end-->
```