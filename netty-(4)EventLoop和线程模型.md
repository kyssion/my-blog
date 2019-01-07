### 线程池模型概述

基本的线程池化模式可以描述为：

从池的空闲线程列表中选择一个Thread，并且指派它去运行一个已提交的任务（一个Runnable的实现）；
当任务完成时，将该Thread返回给该列表，使其可被重用。
![](blogimg/netty/11.png)

### netty中线程模型(eventLoop)使用

1. EventLoop接口 

运行任务来处理在连接的生命周期内发生的事件是任何网络框架的基本功能。与之相应的编程上的构造通常被称为事件循环——一个Netty使用了interface io.netty.channel. EventLoop来适配的术语。

一段代码表示,事件循环的基本思想，其中每个任务都是一个Runnable的实例

```java
while (!terminated) {
　List<Runnable> readyEvents = blockUntilEventsReady();　  // 阻塞，直到有事件已经就绪可被运行
　 for (Runnable ev: readyEvents) {
　　　ev.run();　//   循环遍历，并处理所有的事件
　 }
}
```

> netty 中EventLoop和channel之间的交互状态的合并方式

Netty的EventLoop是协同设计的一部分，它采用了两个基本的API：并发和网络编程。首先，io.netty.util.concurrent包构建在JDK的java.util.concurrent包上，用来提供线程执行器。其次，io.netty.channel包中的类，为了与Channel的事件进行交互，扩展了这些接口/类。


![](/blogimg/netty/12.png)


在这个模型中，一个EventLoop将由一个永远都不会改变的Thread驱动，同时任务（Runnable或者Callable）可以直接提交给EventLoop实现，以立即执行或者调度执行。

根据配置和可用核心的不同，可能会创建多个EventLoop实例用以优化资源的使用，并且单个EventLoop可能会被指派用于服务多个Channel。

在Netty 4中，所有的I/O操作和事件都由已经被分配给了EventLoop的那个Thread来处理

### jdk延时任务和netty的延时任务

在执行延时任务的时候jdk的做法和netty的做法是不同的

java使用多线程机制实现延迟操作ScheduledExecutorService等java.util.concurrent.Executors 类

一个例子

```java
ScheduledExecutorService executor =
　　Executors.newScheduledThreadPool(10);   //  创建一个其线程池具有10 个线程的ScheduledExecutorService
ScheduledFuture<?> future = executor.schedule(
　　new Runnable() {　  //  创建一个R unnable，以供调度稍后执行
　　@Override
　　public void run() {
　　　　System.out.println("60 seconds later");  //  该任务要打印的消息
　　}
}, 60, TimeUnit.SECONDS);  // 调度任务在从现在开始的60 秒之后执行
...
executor.shutdown();   // 一旦调度任务执行完成，就关闭ScheduledExecutorService 以释放资源
```

在netty所有的事件本质上都是使用时间轮训的方法实现的

所以Netty通过Channel的EventLoop实现任务调度解决了这一问题

```java
hannel ch = ...
ScheduledFuture<?> future = ch.eventLoop().schedule(  //  创建一个Runnable以供调度稍后执行
　　new Runnable() { 
　　@Override
　　public void run() {  //  要执行的代码
　　　　System.out.println("60 seconds later");　
　　}
}, 60, TimeUnit.SECONDS);　 //  调度任务在从现在开始的60 秒之后执行
```
经过60秒之后，Runnable实例将由分配给Channel的EventLoop执行。如果要调度任务以每隔60秒执行一次，请使用scheduleAtFixedRate()方法

```java
Channel ch = ...
ScheduledFuture<?> future = ch.eventLoop().scheduleAtFixedRate(   // 创建一个Runnable，以供调度稍后执行 
　　new Runnable() {
　　@Override
　　public void run() {
　　　　System.out.println("Run every 60 seconds");　  // 这将一直运行，直到ScheduledFuture 被取消
　　}
}, 60, 60, TimeUnit.Seconds);　  // 调度在60 秒之后，并且以后每间隔60 秒运行
```

> 注意:Netty的EventLoop扩展了ScheduledExecutorService（见图7-2），所以它提供了使用JDK实现可用的所有方法，包括在前面的示例中使用到的schedule()和scheduleAtFixedRate()方法

要想取消或者检查（被调度任务的）执行状态，可以使用每个异步操作所返回的Scheduled- Future