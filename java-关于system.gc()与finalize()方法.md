
### 1. finalize的作用

- finalize()是Object的protected方法，子类可以覆盖该方法以实现资源清理工作，GC在回收对象之前调用该方法。

- finalize()与C++中的析构函数不是对应的。C++中的析构函数调用的时机是确定的（对象离开作用域或delete掉），但Java中的finalize的调用具有不确定性

- 不建议用finalize方法完成“非内存资源”的清理工作，但建议用于：① 清理本地对象(通过JNI创建的对象)；② 作为确保某些非内存资源(如Socket、文件等)释放的一个补充：在finalize方法中显式调用其他资源释放方法。其原因可见下文[finalize的问题]
### 2. finalize的问题

1. 一些与finalize相关的方法，由于一些致命的缺陷，已经被废弃了，如System.runFinalizersOnExit()方法、Runtime.runFinalizersOnExit()方法
System.gc()与System.runFinalization()方法增加了finalize方法执行的机会，但不可盲目依赖它们

2. Java语言规范并不保证finalize方法会被及时地执行、而且根本不会保证它们会被执行
finalize方法可能会带来性能问题。因为JVM通常在单独的低优先级线程中完成finalize的执行
对象再生问题：finalize方法中，可将待回收对象赋值给GC Roots可达的对象引用，从而达到对象再生的目的

3. finalize方法至多由GC执行一次且只执行一次(用户当然可以手动调用对象的finalize方法，但并不影响GC对finalize的行为)
### 3. finalize的执行过程(生命周期)

描述一下finalize流程：

1. 当对象变成(GC Roots)不可达时，GC会判断该对象是否覆盖了finalize方法，若未覆盖，则直接将其回收。否则，若对象未执行过finalize方法，将其放入F-Queue队列，由一低优先级线程执行该队列中对象的finalize方法。

2. 执行finalize方法完毕后，GC会再次判断该对象是否可达，若不可达，则进行回收，否则，对象“复活”。

具体的finalize流程： 

对象可由**两种状态控制**，涉及到两类状态空间，一是终结状态空间 F = {unfinalized, finalizable, finalized}；二是可达状态空间 R = {reachable, finalizer-reachable, unreachable}。

各状态含义如下： 

- unfinalized: 新建对象会先进入此状态，GC并未准备执行其finalize方法，因为该对象是可达的
- finalizable: 表示GC可对该对象执行finalize方法，GC已检测到该对象不可达。正如前面所述，GC通过F-Queue队列和一专用线程完成finalize的执行
- finalized: 表示GC已经对该对象执行过finalize方法
- reachable: 表示GC Roots引用可达
- finalizer-reachable(f-reachable)：表示不是reachable，但可通过某个finalizable对象可达

- unreachable：对象不可通过上面两种途径可达

> 状态变迁图：

![](blogimg/java/10.png)

> 变迁说明： 

1. 新建对象首先处于[reachable, unfinalized]状态(A) 
2. 随着程序的运行，一些引用关系会消失，导致状态变迁，从reachable状态变迁到f-reachable(B, C, D)或unreachable(E, F)状态 
3. 若JVM检测到处于unfinalized状态的对象变成f-reachable或unreachable，JVM会将其标记为finalizable状态(G,H)。若对象原处于[unreachable, unfinalized]状态，则同时将其标记为f-reachable(H)。 
4. 在某个时刻，JVM取出某个finalizable对象，将其标记为finalized并在某个线程中执行其finalize方法。由于是在活动线程中引用了该对象，该对象将变迁到(reachable, finalized)状态(K或J)。该动作将影响某些其他对象从f-reachable状态重新回到reachable状态(L, M, N) 
5. 处于finalizable状态的对象不能同时是unreachable的，由第4点可知，将对象finalizable对象标记为finalized时会由某个线程执行该对象的finalize方法，致使其变成reachable。这也是图中只有八个状态点的原因 
6. 程序员手动调用finalize方法并不会影响到上述内部标记的变化，因此JVM只会至多调用finalize一次，即使该对象“复活”也是如此。程序员手动调用多少次不影响JVM的行为 
7. 若JVM检测到finalized状态的对象变成unreachable，回收其内存(I) 
8. 若对象并未覆盖finalize方法，JVM会进行优化，直接回收对象（O） 
9. 注：System.runFinalizersOnExit()等方法可以使对象即使处于reachable状态，JVM仍对其执行finalize方法

> 意思的示例代码

1. 对象复活

```java
package com.kys;

public class GC {

    public static GC SAVE_HOOK = null;

    public static void main(String[] args) throws InterruptedException {
        SAVE_HOOK = new GC();
        SAVE_HOOK = null;
        System.gc();
        Thread.sleep(500);
        if (null != SAVE_HOOK) { //此时对象应该处于(reachable, finalized)状态
            System.out.println("Yes , I am still alive"+":"+SAVE_HOOK);
        } else {
            System.out.println("No , I am dead");
        }
        SAVE_HOOK = null;
        System.gc();
        Thread.sleep(500);
        if (null != SAVE_HOOK) {
            System.out.println("Yes , I am still alive");
        } else {
            System.out.println("No , I am dead");
        }
    }

    protected void finalize() throws Throwable {
        super.finalize();
        System.out.println("execute method finalize()");
        SAVE_HOOK = this;//让一次gc复活
    }
}
```

注意：之所以只能进行一次的原因是对象的两个状态已经改变了不能改变回来了

2. jdk内部一些包就是使用这中方法进行资源的释放的

> 覆盖finalize方法以确保资源释放

作为一个补充操作，以防用户忘记“关闭“资源，JDK中FileInputStream、FileOutputStream、Connection类均用了此”技术“，下面代码摘自FileInputStream类

```java
/**
 * Ensures that the <code>close</code> method of this file input stream is
 * called when there are no more references to it.
 *
 * @exception  IOException  if an I/O error occurs.
 * @see        java.io.FileInputStream#close()
 */
protected void finalize() throws IOException {
    if ((fd != null) &&  (fd != FileDescriptor.in)) {

        /*
         * Finalizer should not release the FileDescriptor if another
         * stream is still using it. If the user directly invokes
         * close() then the FileDescriptor is also released.
         */
        runningFinalize.set(Boolean.TRUE);
        try {
            close();
        } finally {
            runningFinalize.set(Boolean.FALSE);
        }
    }
}
```