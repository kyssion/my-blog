vert.x 提供了延迟函数和周期函数两种功能，本质上相当于两个定时器

在 Vert.x 中,想要延迟之后执行或定期执行操作很常见。在 Standard Verticle(之后会讨论) 中您不能直接让线程休眠以引入延迟,因为它会阻塞 Event Loop 线程

### 一次性计时器 - 只执行一次

这个方法在使用lamble的时候传入的参数是这个定时器的id，之后vertx可以使用这个id来终止定时器的调用

```java
Vertx vertx = Vertx.vertx();
long mid = vertx.setTimer(1000,id->{
    System.out.println("the time id is :"+id);
});
System.out.println("the time id in main is :"+mid);
```
### 多次调用定时器 - 这个方法vert.x 将会周期性的调用lamble中的handle

```java
long pid =  vertx.setPeriodic(1000,id->{
    System.out.println("the periodic time id is :"+id);
});
System.out.println("the main periodic time id is :"+pid);
```

### 两种计时器的取消操作

```java
vertx.cancelTimer(timerID);
```

这个方法其中的trmerId就是在声明计时器的时候产生的id编码