## 深入springBoot-Mybatis整合和分析

之前做过springBoot框架的自定义starter配置，这次通过配置springboot和Mybatis，深入源码在解析一下

### spring和mybatis  整合所需要的相关的各种类

- SqlSessionFactoryBean
- SqlSessionFactory
- sqlSessionTemplate
- MapperFactoryBean
- MapperScannerConfigurer

> 现在查看一些spring-mybatis的starer相关的config

```java
@Configuration
@ConditionalOnClass({SqlSessionFactory.class, SqlSessionFactoryBean.class})
@ConditionalOnBean({DataSource.class})
@EnableConfigurationProperties({MybatisProperties.class})
@AutoConfigureAfter({DataSourceAutoConfiguration.class})
public class MybatisAutoConfiguration {
    private static final Logger logger = LoggerFactory.getLogger(MybatisAutoConfiguration.class);
    private final MybatisProperties properties;
    private final Interceptor[] interceptors;
    private final ResourceLoader resourceLoader;
    private final DatabaseIdProvider databaseIdProvider;
    private final List<ConfigurationCustomizer> configurationCustomizers;
      。。。。。。。。。。
```

总结：发现相关的关键类都被自动加载了

查看mybatis Properties 参数配置类

```java

@ConfigurationProperties(
    prefix = "mybatis"
)
public class MybatisProperties {
    public static final String MYBATIS_PREFIX = "mybatis";
    private String configLocation;  //指定配置文件的相关地址
    private String[] mapperLocations;  // 指定mapper配置文件相关地址
    private String typeAliasesPackage;
    private String typeHandlersPackage;
    private boolean checkConfigLocation = false;
    private ExecutorType executorType;  
    private Properties configurationProperties;
。。。。。。。。。。。。。。。。
```

**总结**：传入的参数就使用xml文件需要传入的参数，只不过在使用sporingboot的时候使用soring.yml配置文件的明明方式发生改变

### 整合实例

1. 运行类

```java
@SpringBootApplication
@MapperScan({"com.example.springbootmybatis.dao"})
@EnableTransactionManagement
public class SpringbootmybatisApplication implements CommandLineRunner {
    @Autowired
    Userservice userservice;
    public static void main(String[] args) {
        try{
            SpringApplication.run(SpringbootmybatisApplication.class, args);
        }catch (Exception e){
            e.printStackTrace();
        }
    }
    @Override
    public void run(String... args) throws Exception {
        userservice.zhuan(new User("tom"),new User("jack"));
    }
}
```

2. service dao 和 bean 类

```java
@Service
public class Userservice {
    @Resource(name="userImp")
    public UserImp userImp;
    @Transactional
    public boolean zhuan(User from,User to){
        from.setMoney(-100);
        to.setMoney(100);
        userImp.updateUser(from);
        int a=1/0;
        userImp.updateUser(to);
        return true;
    }
}

@Controller("userImp")
public interface UserImp {
    public int insertUser(User user);
    public User selectUser(User user);
    public int updateUser(User user);
}
public class User {
    private String name;
    private int money;
    public User(){
        super();
    }
    public User(String name){
        this.name=name;
    }
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
```

3. pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>springbootmybatis</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <packaging>jar</packaging>
    <name>springbootmybatis</name>
    <description>Demo project for Spring Boot</description>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.5.8.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>

    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <java.version>1.8</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-jdbc</artifactId>
        </dependency>
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>1.3.1</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid</artifactId>
            <version>1.1.4</version>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```
4. mybatis config和mappper

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE configuration PUBLIC "-//mybatis.org//DTD Config 3.0//EN" "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <settings>
        <setting name="logImpl" value="STDOUT_LOGGING"/>
        <setting name="mapUnderscoreToCamelCase" value="true"/>
    </settings>
    <!-- 和sping框架进行结合的时候不需要使用enviroment标签spring框架会自动的设置好 -->
</configuration>
<!--mapper-->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.example.springbootmybatis.dao.UserImp">
    <resultMap  type="com.example.springbootmybatis.been.User" id="users">
        <id property="name" column="name" jdbcType="VARBINARY" javaType="string"/>
        <result property="money" column="money" jdbcType="INTEGER" javaType="int"/>
    </resultMap>
    <select id="selectUser" parameterType="com.example.springbootmybatis.been.User" resultMap="users">
        select * from user where name=#{name}
    </select>
    <insert id="insertUser" parameterType="com.example.springbootmybatis.been.User">
        insert into user(name,money) value(#{name},#{money})
    </insert>
    <update id="updateUser" parameterType="com.example.springbootmybatis.been.User">
        <selectKey keyProperty="money" resultType="int" order="BEFORE">
            select money from user where name = #{name}
        </selectKey>
        UPDATE user SET money=#{money} WHERE name=#{name}
    </update>
</mapper>
```

5. yaml文件

```
mybatis:
  config-location: classpath:mybatis-config.xml
  mapper-locations: classpath:mapper/*.xml
 
spring:
    datasource:
        url: jdbc:mysql://127.0.0.1:3306/demo
        username: root
        password: 14159265jkl
        # 使用druid数据源
        type: com.alibaba.druid.pool.DruidDataSource
        driver-class-name: com.mysql.jdbc.Driver
        filters: stat
        maxActive: 20
        initialSize: 1
        maxWait: 60000
        minIdle: 1
        timeBetweenEvictionRunsMillis: 60000
        minEvictableIdleTimeMillis: 300000
        validationQuery: select 'x'
        testWhileIdle: true
        testOnBorrow: false
        testOnReturn: false
        poolPreparedStatements: true
        maxOpenPreparedStatements: 20
        name: test
```

> 引申，也可以使用spring的原生bean进行相关的配置  只需要在注解上加上@ImportResource  ，并在其中引入自己需要的xml文件就行

```java
@SpringBootApplication
@MapperScan({"com.example.springbootmybatis.dao"})
@ImportResource({"classpath:bean.xml"})
public class SpringbootmybatisApplication implements CommandLineRunner {
    @Autowired
    Userservice userservice;
    public static void main(String[] args) {
        try{
            SpringApplication.run(SpringbootmybatisApplication.class, args);
        }catch (Exception e){
            e.printStackTrace();
        }
    }
    @Override
    public void run(String... args) throws Exception {
        userservice.zhuan(new User("tom"),new User("jack"));
    }
}
```

6. bean.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:tx="http://www.springframework.org/schema/tx"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.2.xsd
		http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.3.xsd
		http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-4.3.xsd">

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
    <bean id="myTransactionMamager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="dataSource"></property>
    </bean>
    <tx:annotation-driven transaction-manager="myTransactionMamager"/>
</beans>
```

7. 数据库配置文件

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