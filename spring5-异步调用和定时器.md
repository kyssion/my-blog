## spring5-异步调用和定时器

> Eable*类型的注解是和spring configurtion注解搭配使用的目的是减少配置和代码数量

### @EnableAsync 支持异步操作

> 配置类 @EnableAsync

```java

@Configuration
@ComponentScan(basePackages = {"org.bean", "org.controler"})
@PropertySource("needpro.properties")
@EnableAsync
public class SpringConfig implements AsyncConfigurer {

    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor taskExecutor = new ThreadPoolTaskExecutor();
        taskExecutor.setCorePoolSize(5);
        taskExecutor.setMaxPoolSize(10);
        taskExecutor.setQueueCapacity(25);
        taskExecutor.initialize();
        return taskExecutor;
    }
    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {

        return null;
    }
}
```

> javabean 类 @Async

```java
@Service
public class TaskExecutorConfig {
    @Async
    public void execturonRunOne(int a){
        System.out.println("test one "+a);
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
    @Async
    public void executronRunTwo(int b){
        System.out.println("test two "+b);
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

> 执行主函数

```java
public class Main {
    public static void main(String[] args) {
        ApplicationContext context =new AnnotationConfigApplicationContext(SpringConfig.class);
 
        TaskExecutorConfig taskExecutorConfig =
                context.getBean(TaskExecutorConfig.class);
        for (int a=0;a<10;a++){
            taskExecutorConfig.execturonRunOne(a);
            taskExecutorConfig.executronRunTwo(a);
        }
        System.out.println("完成");
    }
}
```

结果：

![](blogimg/spring/1.png)

结论：函数变成一部执行非阻塞型

### @EnableScheduling 允许进行定时操作

> 配置类

```java
@EnableScheduling
public class SpringConfig implements AsyncConfigurer {
}
```

> javabean类

```java
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

@Service
public class SchedyledIten {
    @Scheduled(initialDelay =2000,fixedDelay = 2000)
    public String methodOne(){
        System.out.println("one");
        return null;
    }
    @Scheduled(initialDelay =2000,fixedRate = 2000)
    public String method2(){
        System.out.println("two");
        return null;
    }
    @Scheduled(initialDelay =2000,cron = "0 0 2 1 * ?  ")
    public String method3(){
        System.out.println("two");
        return null;
    }
}
```

**注意**：除了cron标记的其他元素如果没有使用iniiaDelay参数将会执行两边（调用一边，没有进行延迟一遍） ，cron表达式只支持六个参数

> cron 表达式详解


| 符号 | Seconds | Minutes | Hours | DayofMonth | Month | DayofWeek | Year |
|------|---------|---------|-------|------------|-------|-----------|------|
| ，   | Y       | Y       | Y     | Y          | Y     | Y         | Y    |
| –    | Y       | Y       | Y     | Y          | Y     | Y         | Y    |
| *    | Y       | Y       | Y     | Y          | Y     | Y         | Y    |
| /    | Y       | Y       | Y     | Y          | Y     | Y         | Y    |
| ?    | N       | N       | N     | Y          | N     | Y         | N    |
| L    | N       | N       | N     | Y          | N     | Y         | N    |
| W    | N       | N       | N     | Y          | N     | N         | N    |
| C    | N       | N       | N     | Y          | N     | Y         | N    |
| #    | N       | N       | N     | N          | N     | Y         | N    |

1. *  ：表示匹配该域的任意值，假如在Minutes域使用*, 即表示每分钟都会触发事件。
2. ? ：只能用在DayofMonth和DayofWeek两个域。它也匹配域的任意值，但实际不会。因为3. DayofMonth和DayofWeek会相互影响。例如想在每月的20日触发调度，不管20日到底是星期几，则只能使用如下写法： 13 13 15 20 * ?, 其中最后一位只能用？，而不能使用*，如果使用*表示不管星期几都会触发，实际上并不是这样。 
4. –  :表示范围，例如在Minutes域使用5-20，表示从5分到20分钟每分钟触发一次 
5. /  ：表示起始时间开始触发，然后每隔固定时间触发一次，例如在Minutes域使用5/20,则意味着5分钟触发一次，而25，45等分别触发一次. 
6. ,  ：表示列出枚举值值。例如：在Minutes域使用5,20，则意味着在5和20分每分钟触发一次。 
7. L ：表示最后，只能出现在DayofWeek和DayofMonth域，如果在DayofWeek域使用5L,意味着在最后的一个星期四触发。 
8. W ：表示有效工作日(周一到周五),只能出现在DayofMonth域，系统将在离指定日期的最近的有效工作日触发事件。例如：在 DayofMonth使用5W，如果5日是星期六，则将在最近的工作日：星期五，即4日触发。如果5日是星期天，则在6日(周一)触发；如果5日在星期一到星期五中的一天，则就在5日触发。另外一点，W的最近寻找不会跨过月份 
9. LW ：这两个字符可以连用，表示在某个月最后一个工作日，即最后一个星期五。 
10. \# ：用于确定每个月第几个星期几，只能出现在DayofMonth域。例如在4#2，表示某月的第二个星期三。