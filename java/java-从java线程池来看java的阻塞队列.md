一说到java的阻塞队列，我们就会想到在java的jdk中的那么多的类

1.ArrayDeque, （数组双端队列） 
2.PriorityQueue, （优先级队列） 
3.ConcurrentLinkedQueue, （基于链表的并发队列） 
4.DelayQueue, （延期阻塞队列）（阻塞队列实现了BlockingQueue接口） 
5.ArrayBlockingQueue, （基于数组的并发阻塞队列） 
6.LinkedBlockingQueue, （基于链表的FIFO阻塞队列） 
7.LinkedBlockingDeque, （基于链表的FIFO双端阻塞队列） 
8.PriorityBlockingQueue, （带优先级的无界阻塞队列） 
9.SynchronousQueue （并发同步阻塞队列）

这里不去细说的这些东西，而是从线程池的一个异常来聊聊这个事情

# 构造一个线程池异常 - 线程池过载异常

```java
public class ThreadPoolTest {
    public static void main(String[] args) {
        ThreadPoolExecutor executor = new ThreadPoolExecutor(2,2,10000, TimeUnit.DAYS,
                new LinkedBlockingDeque<>(2));//这里如果指定了固定的长度就表示是有界队列了
        List<Future<?>> futures = new ArrayList<>();
        for (int a=0;a<1000;a++){
            futures.add(executor.submit(()->{
                System.out.println("thread start : "+Thread.currentThread().getName());
                try {
                    Thread.sleep(10000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("thread end : "+Thread.currentThread().getName());
            }));
        }
        for (Future<?> future: futures){
            try {
                future.get();
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
        }
    }
}
```

这段代码如果直接运行将会抛出异常

```
OpenJDK 64-Bit Server VM warning: Sharing is only supported for boot loader classes because bootstrap classpath has been appended
Exception in thread "main" java.util.concurrent.RejectedExecutionException: Task java.util.concurrent.FutureTask@7a07c5b4[Not completed, task = java.util.concurrent.Executors$RunnableAdapter@3d646c37[Wrapped task = org.java.deme.ThreadPoolTest$$Lambda$14/0x0000000840067840@41cf53f9]] rejected from java.util.concurrent.ThreadPoolExecutor@5a10411[Running, pool size = 2, active threads = 2, queued tasks = 2, completed tasks = 0]
	at java.base/java.util.concurrent.ThreadPoolExecutor$AbortPolicy.rejectedExecution(ThreadPoolExecutor.java:2055)
	at java.base/java.util.concurrent.ThreadPoolExecutor.reject(ThreadPoolExecutor.java:825)
	at java.base/java.util.concurrent.ThreadPoolExecutor.execute(ThreadPoolExecutor.java:1355)
	at java.base/java.util.concurrent.AbstractExecutorService.submit(AbstractExecutorService.java:118)
	at org.java.deme.ThreadPoolTest.main(ThreadPoolTest.java:13)
```

总结一下： 其实这个问题是加入的线程数量已经超过了整个线程池能负载的最大数量了（新建线程池的时候使用了有界队列），所以抛出了了异常

# 避免线程池溢出异常 - 使用无界队列和有界队列

1. BlockingQueue

这个是为了解决java并发同步问题的，本质上是解决线程间消息同步而设计的

有一下几个类：

1.DelayQueue, （延期阻塞队列）（阻塞队列实现了BlockingQueue接口） 这个队列是无界的，并且没有指定长度的构造方法
2.ArrayBlockingQueue, （基于数组的并发阻塞队列） 必须设置长度
3.LinkedBlockingQueue, （基于链表的FIFO阻塞队列） 没有指定长度就是有界的反之是有界的
4.LinkedBlockingDeque, （基于链表的FIFO双端阻塞队列） 没有指定长度就是有界的反之是有界的
5.PriorityBlockingQueue, （带优先级的无界阻塞队列） 这个只能传入Comperable接口的类新，不是有界的
6.SynchronousQueue （并发同步阻塞队列）不能指定长度，只能传入一个值，有界

回过来看看上面的源码，其实线程池在加入线程时候的逻辑是这样的

构建常驻线程coreNum指定，如果超过，建立临时线程maxNum , 还不够，增加到队列中

线程池判断能不能增加仅对列是使用的队列的offset方法

```java
public void execute(Runnable command) {
    if (command == null)
        throw new NullPointerException();
    int c = ctl.get();
    if (workerCountOf(c) < corePoolSize) {
        if (addWorker(command, true))
            return;
        c = ctl.get();
    }
    if (isRunning(c) && workQueue.offer(command)) {
        int recheck = ctl.get();
        if (! isRunning(recheck) && remove(command))
            reject(command);
        else if (workerCountOf(recheck) == 0)
            addWorker(null, false);
    }
    else if (!addWorker(command, false))
        reject(command);
}
```

如果是有界的队列党对列满了自然返回false，因为添加不进去了，然后就会抛出异常

# 总结一下

我们在使用java线程池的时候需要做好容量规划，如果无法确定是否超出了指定的线程数量，可以使用无界队列，但是要注意到防止内存泄漏



