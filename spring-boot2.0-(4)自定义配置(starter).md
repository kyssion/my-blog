spring boot 提供了非常方便的方法可以自动配置javabean

# spring boot自动的配置的核心

## 一个基本注解@Configuration和条件注解@Conditional

spring的自动配置是使用上面的两个bean提供功能的

- @Configuration 标记这个类是一个config配置类
- @Conditional 这个是控制自动配置条件的类

## spring boot spi 

spring boot自己实现了一套spi机制, spring boot 要求在META-INF中生成一个配置文件