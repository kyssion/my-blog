### JdbcTemplate spring 数据库操作基础类

这个类是spring进行jdbc操作的核心，通过这个方法将节省数据库操作，和避免一些低级错误，比如资源没哟释放等等

#### select 操作

```java
//指定返回数据的类型
int rowCount = this.jdbcTemplate.queryForObject("select count(*) from t_actor", Integer.class);
//传入参数 和指定返回的类型   注意 最后一个参数是数组
int countOfActorsNamedJoe = this.jdbcTemplate.queryForObject(
        "select count(*) from t_actor where first_name = ?", Integer.class, "Joe");
//另一种写法  中间的数组是
String lastName = this.jdbcTemplate.queryForObject(
        "select last_name from t_actor where id = ?",
        new Object[]{1212L}, String.class);
// 使用 RowMapper 接口处理返回的数据 (或者使用ResultSetExtractor)
Actor actor = this.jdbcTemplate.queryForObject(
        "select first_name, last_name from t_actor where id = ?",
        new Object[]{1212L},
        new RowMapper<Actor>() {
            public Actor mapRow(ResultSet rs, int rowNum) throws SQLException {
                Actor actor = new Actor();
                actor.setFirstName(rs.getString("first_name"));
                actor.setLastName(rs.getString("last_name"));
                return actor;
            }
        });
```

#### update delete insert操作

```java
jdbcTemplate.update(
        "insert into t_actor (first_name, last_name) values (?, ?)",
        "Leonor", "Watling");
jdbcTemplate.update(
        "update t_actor set last_name = ? where id = ?",
        "Banjo", 5276L);
jdbcTemplate.update(
        "delete from actor where id = ?",
        Long.valueOf(actorId));
jdbcTemplate.update(
        "delete from actor where id = ?",
        new Object["sdfsdf"],);    
jdbcTemplate.update("udpate TABLE set NAME = ?"
        ,new Object[]{"tom"},new int[]{Types.VARCHAR});
```

#### 使用数据操作语句进行操作的通用方法

这个方法可以执行任何语句

```java
jdbcTemplate.execute("create table mytable (id integer, name varchar(100))");
```

#### jdbcTemple 初始化

传入一个数据库链接的相关信息和是否使用延迟加载的方法

```java
JdbcTemplate template = new JdbcTemplate(database,lazyinit);
```

### NamedParameterJdbcTemplate

这个接口是一个特殊的存在，底层使用JDBCTemplate同时将之前使用适配符的？进行了替换

这个接口的一个高级应用就是使用 SqlParameterSource 进行分装 ， spring 官方文档中主要提供了如下的三种方法进行相关的操作

```java
private NamedParameterJdbcTemplate namedParameterJdbcTemplate;
public void setDataSource(DataSource dataSource) {
    this.namedParameterJdbcTemplate = new NamedParameterJdbcTemplate(dataSource);
}
//使用类似hashmap的方法进行相关的操作
public int countOfActorsByFirstName(String firstName) {
    String sql = "select count(*) from T_ACTOR where first_name = :first_name";
    SqlParameterSource namedParameters = new MapSqlParameterSource("first_name", firstName);
    return this.namedParameterJdbcTemplate.queryForObject(sql, namedParameters, Integer.class);
}

// 使用最一般的map进行操作
public int countOfActorsByFirstName(String firstName) {
    String sql = "select count(*) from T_ACTOR where first_name = :first_name";
    Map<String, String> namedParameters = Collections.singletonMap("first_name", firstName);
    return this.namedParameterJdbcTemplate.queryForObject(sql, namedParameters,  Integer.class);
}

// 直接封装相关的各
public int countOfActors(Actor exampleActor) {
    // notice how the named parameters match the properties of the above 'Actor' class
    String sql = "select count(*) from T_ACTOR where first_name = :firstName and last_name = :lastName";
    SqlParameterSource namedParameters = new BeanPropertySqlParameterSource(exampleActor);
    return this.namedParameterJdbcTemplate.queryForObject(sql, namedParameters, Integer.class);
}
```

### DriverManagerDataSource spring 内置数据库的实现

```java
DriverManagerDataSource dataSource = new DriverManagerDataSource();
dataSource.setDriverClassName("org.hsqldb.jdbcDriver");
dataSource.setUrl("jdbc:hsqldb:hsql://localhost:");
dataSource.setUsername("sa");
dataSource.setPassword("");
```



### spring 进行批处理

使用JDBCTemplete进行批处理

```java
public class JdbcActorDao implements ActorDao {
    private JdbcTemplate jdbcTemplate;
    public void setDataSource(DataSource dataSource) {
        this.jdbcTemplate = new JdbcTemplate(dataSource);
    }
    public int[] batchUpdate(final List<Actor> actors) {
        return this.jdbcTemplate.batchUpdate(
                "update t_actor set first_name = ?, last_name = ? where id = ?",
                new BatchPreparedStatementSetter() {
                    public void setValues(PreparedStatement ps, int i) throws SQLException {
                        ps.setString(1, actors.get(i).getFirstName());
                        ps.setString(2, actors.get(i).getLastName());
                        ps.setLong(3, actors.get(i).getId().longValue());
                    }
                    public int getBatchSize() {
                        return actors.size();
                    }
                });
    }
    // ... additional methods
}
```

使用namedParameterJdbcTemplate 进行批处理

```java
public class JdbcActorDao implements ActorDao {
    private NamedParameterTemplate namedParameterJdbcTemplate
    public void setDataSource(DataSource dataSource) {
        this.namedParameterJdbcTemplate = new NamedParameterJdbcTemplate(dataSource);
    }
    public int[] batchUpdate(List<Actor> actors) {
        return this.namedParameterJdbcTemplate.batchUpdate(
                "update t_actor set first_name = :firstName, last_name = :lastName where id = :id",
                SqlParameterSourceUtils.createBatch(actors));
    }
    // ... additional methods
}
```

> 结语： 这里的这些特性其实就是在使用相关的技术的时候感兴趣才看的，真正在生产环境下使用 mybatis这种持久层框架比较多
