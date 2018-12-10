## 一.了解 强引用、软引用、弱引用、虚引用的概念

在Java中，虽然不需要程序员手动去管理对象的生命周期，但是如果希望某些对象具备一定的生命周期的话（比如内存不足时JVM就会自动回收某些对象从而避免OutOfMemory的错误）就需要用到软引用和弱引用了。

从Java SE2开始，就提供了四种类型的引用：强引用、软引用、弱引用和虚引用。Java中提供这四种引用类型主要有两个目的：第一是可以让程序员通过代码的方式决定某些对象的生命周期；第二是有利于JVM进行垃圾回收。下面来阐述一下这四种类型引用的概念：

### 1.强引用（StrongReference）

强引用就是指在程序代码之中普遍存在的，比如下面这段代码中的object和str都是强引用：

```java
Object object = new Object();
String str = "hello";
```

只要某个对象有强引用与之关联，JVM必定不会回收这个对象，即使在内存不足的情况下，JVM宁愿抛出OutOfMemory错误也不会回收这种对象。比如下面这段代码：

```java
public class Main {
    public static void main(String[] args) {
        new Main().fun1();
    }
     
    public void fun1() {
        Object object = new Object();
        Object[] objArr = new Object[1000];
    }
}
```

当运行至Object[] objArr = new Object[1000];这句时，如果内存不足，JVM会抛出OOM错误也不会回收object指向的对象。不过要注意的是，当fun1运行完之后，object和objArr都已经不存在了，所以它们指向的对象都会被JVM回收。

如果想中断强引用和某个对象之间的关联，可以显示地将引用赋值为null，这样一来的话，JVM在合适的时间就会回收该对象。

比如Vector类的clear方法中就是通过将引用赋值为null来实现清理工作的：

```java
package com.kys;

public class Refence {
    public synchronized E remove(int index) {
        modCount++;
        if (index >= elementCount)
            throw new ArrayIndexOutOfBoundsException(index);
        Object oldValue = elementData[index];

        int numMoved = elementCount - index - 1;
        if (numMoved > 0)
            System.arraycopy(elementData, index + 1, elementData, index,
                    numMoved);
        elementData[--elementCount] = null; // Let gc do its work

        return (E) oldValue;
    }
}
```

### 2.软引用（SoftReference）

软引用是用来描述一些有用但并不是必需的对象，在Java中用java.lang.ref.SoftReference类来表示。对于软引用关联着的对象，只有在内存不足的时候JVM才会回收该对象。因此，这一点可以很好地用来解决OOM的问题，并且这个特性很适合用来实现缓存：比如网页缓存、图片缓存等。

软引用可以和一个引用队列（ReferenceQueue）联合使用，如果软引用所引用的对象被JVM回收，这个软引用就会被加入到与之关联的引用队列中。下面是一个使用示例：

```java
import java.lang.ref.SoftReference;
 
public class Main {
    public static void main(String[] args) {
         
        SoftReference<String> sr = new SoftReference<String>(new String("hello"));
        System.out.println(sr.get());
    }
}
```

### 3.弱引用（WeakReference）

弱引用也是用来描述非必需对象的，当JVM进行垃圾回收时，无论内存是否充足，都会回收被弱引用关联的对象。在java中，用java.lang.ref.WeakReference类来表示。下面是使用示例：

```java
import java.lang.ref.WeakReference;
 
public class Main {
    public static void main(String[] args) {
     
        WeakReference<String> sr = new WeakReference<String>(new String("hello"));
         
        System.out.println(sr.get());
        System.gc();                //通知JVM的gc进行垃圾回收
        System.out.println(sr.get());
    }
}
```

输出结果为：

```
hello
null
```

第二个输出结果是null，这说明只要JVM进行垃圾回收，被弱引用关联的对象必定会被回收掉。不过要注意的是，这里所说的被弱引用关联的对象是指只有弱引用与之关联，如果存在强引用同时与之关联，则进行垃圾回收时也不会回收该对象（软引用也是如此）。

弱引用可以和一个引用队列（ReferenceQueue）联合使用，如果弱引用所引用的对象被JVM回收，这个软引用就会被加入到与之关联的引用队列中。

### 4.虚引用（PhantomReference）

虚引用和前面的软引用、弱引用不同，它并不影响对象的生命周期。在java中用java.lang.ref.PhantomReference类表示。如果一个对象与虚引用关联，则跟没有引用与之关联一样，在任何时候都可能被垃圾回收器回收。

要注意的是，虚引用必须和引用队列关联使用，当垃圾回收器准备回收一个对象时，如果发现它还有虚引用，就会把这个虚引用加入到与之 关联的引用队列中。程序可以通过判断引用队列中是否已经加入了虚引用，来了解被引用的对象是否将要被垃圾回收。如果程序发现某个虚引用已经被加入到引用队列，那么就可以在所引用的对象的内存被回收之前采取必要的行动。

```java
import java.lang.ref.PhantomReference;
import java.lang.ref.ReferenceQueue;
 
 
public class Main {
    public static void main(String[] args) {
        ReferenceQueue<String> queue = new ReferenceQueue<String>();
        PhantomReference<String> pr = new PhantomReference<String>(new String("hello"), queue);
        System.out.println(pr.get());
    }
}
```

## 二.进一步理解软引用和弱引用

对于强引用，我们平时在编写代码时经常会用到。而对于其他三种类型的引用，使用得最多的就是软引用和弱引用，这2种既有相似之处又有区别。它们都是用来描述非必需对象的，但是被软引用关联的对象只有在内存不足时才会被回收，而被弱引用关联的对象在JVM进行垃圾回收时总会被回收。

在SoftReference类中，有三个方法，两个构造方法和一个get方法（WekReference类似）：

两个构造方法：

```java
public SoftReference(T referent) {
    super(referent);
    this.timestamp = clock;
}

public SoftReference(T referent, ReferenceQueue<? super T> q) {
    super(referent, q);
    this.timestamp = clock;
}
```

get方法用来获取与软引用关联的对象的引用，如果该对象被回收了，则返回null。

在使用软引用和弱引用的时候，我们可以显示地通过System.gc()来通知JVM进行垃圾回收，但是要注意的是，虽然发出了通知，JVM不一定会立刻执行，也就是说这句是无法确保此时JVM一定会进行垃圾回收的。

## 三.如何利用软引用和弱引用解决OOM问题

前面讲了关于软引用和弱引用相关的基础知识，那么到底如何利用它们来优化程序性能，从而避免OOM的问题呢？

下面举个例子，假如有一个应用需要读取大量的本地图片，如果每次读取图片都从硬盘读取，则会严重影响性能，但是如果全部加载到内存当中，又有可能造成内存溢出，此时使用软引用可以解决这个问题。

设计思路是：用一个HashMap来保存图片的路径 和 相应图片对象关联的软引用之间的映射关系，在内存不足时，JVM会自动回收这些缓存图片对象所占用的空间，从而有效地避免了OOM的问题。在Android开发中对于大量图片下载会经常用到。

```java
private Map<String, SoftReference<Bitmap>> imageCache = new HashMap<String, SoftReference<Bitmap>>();
public void addBitmapToCache(String path) {
    // 强引用的Bitmap对象
    Bitmap bitmap = BitmapFactory.decodeFile(path);
    // 软引用的Bitmap对象
    SoftReference<Bitmap> softBitmap = new SoftReference<Bitmap>(bitmap);
    // 添加该对象到Map中使其缓存
    imageCache.put(path, softBitmap);
}
public Bitmap getBitmapByPath(String path) {
    // 从缓存中取软引用的Bitmap对象
    SoftReference<Bitmap> softBitmap = imageCache.get(path);
    // 判断是否存在软引用
    if (softBitmap == null) {
        return null;
    }
    // 取出Bitmap对象，如果由于内存不足Bitmap被回收，将取得空
    Bitmap bitmap = softBitmap.get();
    return bitmap;
}
```

