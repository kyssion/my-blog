java 在多线线程编程中有个许许多多的优势,其中一个就是java的基于CAS理论而创建的锁ReentrantLock,这里主要是回顾一下CAS是如何实现线程安全的

## CAS简介

> 其实cas 很简单 ,使用的是"比较交换算法", 核心体现在AtomicReference.compareAndSet(xx,xx2) 上 , 这个函数将会比较传入的xx 和 AtomicReference 中存过的值是否发生变化如果没有发生变化,将会将xx2 的值赋给xx,否则这个函数将会返回false

通过AtomicReference.compareAndSet(xx,xx2) 这种特性我们可是设计一种回滚策略来将实现并发时,公共属性征用的问题

## 用java 栈来举一个简单的例子

- 首先定义一个新的java栈对象

```java
class Stack<E> {

    private Node<E> head;

    private static class Node<E> {
        public final E item;

        public Node<E> next;

        public Node(E item) {
            this.item = item;
        }
    }

    public void push(E item) {
        Node<E> eNode = new Node<E>(item);
        eNode.next = head;
        head = eNode;
    }

    public E pop() {
        if (head != null) {
            E need = head.item;
            head = head.next;
            return need;
        }
        return null;
    }
}
```
-  接下来编写java的main方法,这里采用的多线的方法,每个线程处理一个变量并且将这个变量加入到公共的列表中

```java
public class Main {
    public static void main(String[] args) {
        hasThread();
    }

    public static void NoThread() {
        Stack<Integer> stack = new Stack<>();
        for (int a = 0; a < 10; a++) {
            stack.push(a);
        }
        for (int a = 0; a < 10; a++) {
            System.out.println(stack.pop());
        }
    }
    //使用多线程的方法进行处理
    public static void hasThread() {
        Stack<Integer> stack = new Stack<>();
        int max = 100;
        Thread[] threads = new Thread[max];
        for (int i = 0; i < max; i++) {
            int temp = i;
            //入栈1、2、3
            Thread thread = new Thread(() -> stack.push(temp + 1));
            thread.start();
            threads[temp] = thread;
        }
        //等待所有线程完成。
        for (int i = 0; i < max; i++) {
            try {
                threads[i].join();
            } catch (InterruptedException e) {
            }
        }

        for (int i = 0; i < max; i++) {
            if(stack.pop()==null){
                System.out.println("ok");
            }
        }
    }
}
```

大多数情况下会产生的结果和下面的相同

```
2
1
0
```

但是在特殊的情况下会出现多线程的问题

我没修改push方法的这里

```java
public void push(E item) {
    Node<E> eNode = new Node<E>(item);
    eNode.next = head;
    Thread.yield();
    head = eNode;
}
```

这里会出现空指针的问题

```
3
1
null
```

这里分析一下这种方法的运行过程

| 执行顺序 | thread-0                            | thread-1                            | thread-2                            |
|----------|-------------------------------------|-------------------------------------|-------------------------------------|
| 1        | Node<E> newHead = new Node<>(item); | --                                  | --                                  |
| 2        | head=newHead;                       | --                                  | --                                  |
| 3        | (Resume)                            | --                                  | --                                  |
| 4        | --                                  | Node<E> newHead = new Node<>(item); | --                                  |
| 5        | --                                  | --                                  | Node<E> newHead = new Node<>(item); |
| 6        | --                                  | newHead.next = head;                | --                                  |
| 7        | --                                  | --                                  | newHead.next = head;                |
| 8        | --                                  | head=newHead;                       | --                                  |
| 9        | --                                  | --                                  | head=newHead;                       |
| 10       | --                                  | (Resume)                            |                                     |
| 11       | --                                  | --                                  | (Resume)                            |


> 异常结果是如何产生的？

- 当thread-0执行到顺序3时，head表示的链表为node(1)。
- 当thread-1执行到顺序10时，head表示的链表为node(2)->node(1)。
- 当thread-2执行到顺序11时，head表示的链表为node(3)->node(1)。
- 当三个线程都执行完毕之后，head的最终表示为node(3)->node(1)，也就是说thread-2将thread-1的执行结果覆盖了。

### 解决办法

> 1. synchronized 关键字或者 ReentrantLock 线程锁

```java
public synchronized void push(E item) {
    Node<E> eNode = new Node<E>(item);
    eNode.next = head;
    Thread.yield();
    head = eNode;
}

//这里使用ReentrantLock类似
public void push(E item) {
    Node<E> eNode = new Node<E>(item);
    synchronized (this) {
        eNode.next = head;
        Thread.yield();
    }
    head = eNode;
}
```

这种加锁的方法很简单不多说了, 主要讲讲第二种CAS原子性操作的做法, 上代码

```java
class CASStack<E> {

    private AtomicReference<Node<E>> cas = new AtomicReference<>();

    private static class Node<E> {
        public final E item;

        public Node<E> next;

        public Node(E item) {
            this.item = item;
        }
    }

    public void push(E item){
        Node<E> eNode = new Node<E>(item);
        Node<E> old;
        do{
            old = cas.get();
            eNode.next = old;
        }while (!cas.compareAndSet(old, eNode));
    }

    public E pop(){
        E item = null;
        Node<E> now;
        do{
            now = cas.get();
            if(now==null){
                return null;
            }
            item = now.item;
        }while(!cas.compareAndSet(now,now.next));
        return item;
    }

    public void pushError(E item) {
        Node<E> eNode = new Node<E>(item);
        do {
            eNode.next = cas.get();
        } while (!cas.compareAndSet(cas.get(), eNode));
    }

    public E popError() {
        E item = null;
        if (cas.get() != null) {
            do {
                item = cas.get().item;
            } while (!cas.compareAndSet(cas.get(), cas.get().next));
        }
        return item;
    }
}
```

> 其实就像我开篇说的一样其实核心就是compareAndSet方法校验在争用环境下,我自己获取的值是否发生过修改,如果发生过修改就进行回滚的操作

> 其实上面的例子中还要注意一个地方就是两个error 错误点就是用cas.get()方法来尽心获取,这样并不可取因为,操作compareAndSet会导致cas.get()方法中的数据发生改变,从而导致线程安全失败


