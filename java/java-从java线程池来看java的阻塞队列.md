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

```