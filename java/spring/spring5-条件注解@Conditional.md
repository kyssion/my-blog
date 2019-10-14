## spring5-条件注解@Conditional

@Conditional将会按照条件自动的创建相关的javabean类型

### 继承Condition接口创建条件判断类

```java
public class LinuxCondition implements Condition{
    @Override
    public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
        //context是构建的上下文属性
        return context.getEnvironment().getProperty("os.name").contains("Linux");
    }
}
```

### 一个bean类型

```java
@Component("book")
public class Book {
    @Value("mybook")
    private String name;
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
}
```

### 配置类

```java
@Configuration
@ComponentScan(basePackages = {"org.bean", "org.controler"})
public class SpringConfig implements AsyncConfigurer {
    @Bean("theBook")
    @Scope()
    @Conditional(LinuxCondition.class)
    public Book getBook(){
        return new Book();
    }
}
```

配置类将会通过Condition返回是否是true进行相关判断如果返回的结果是true将会自动的载入相关的配置