### 单例模式

这个模式其实并不需要过多的阐释，重点是如何构建好一个单例模式，最基础的代码如下

```java
package org.kys.Gaf.singleton;
public class Singleton {
    private static final Singleton = new Singleton();
    private Singleton() {}
    public static getSignleton(){
        return singleton;
    }
}
```

以上的方法属于饿汉模式：一开始就生成的实例

其实单例模式还有一种懒加载模式-饿汉模式，不过这种模式有许多的坑

### 懒加载单例模式最基础样式

```java
package org.kys.Gaf.singleton;
public class Singleton {
    private static Singleton singleton = null;
    private Singleton(){}
    public static Singleton getSingleton() {
        if(singleton == null) singleton = new Singleton();
        return singleton;
    }
}
```

> 这种写法有线程安全问题，比如1线程运行到if语句中2线程也运行到if中，之后将会创建两个对象造成对象不同。

### 添加线程安全的单例模式

1. 基本思路 synchronized解决

```java
package org.kys.Gaf.singleton;

public class Singleton {
    private static Singleton singleton = null;

    private Singleton() {
    }

    public static synchronized Singleton getSingleton() {
        if (singleton == null) singleton = new Singleton();
        return singleton;
    }
}
```

> 缺点性能低下 synchronized 99% 不需要线程同步

2. synchronized代码块优化

```java
package org.kys.Gaf.singleton;

public class Singleton {
    private static Singleton singleton = null;

    private Singleton() {
    }

    public static Singleton getSingleton() {
        synchronized(Singleton.class) {
            if (singleton == null) singleton = new Singleton();
        }
        return singleton;
    }
}
```

> 没有使用全局锁但是还是有问题，代码块同样需要每次运行

3. 双重锁家线程可见

```java
package org.kys.Gaf.singleton;

public class Singleton {
    private volatile static Singleton singleton = null;

    private Singleton() {
    }

    public static Singleton getSingleton() {
        if (singleton == null) {
            synchronized (Singleton.class) {
                if (singleton == null) singleton = new Singleton();
            }
        }
        return singleton;
    }
}
```

这里使用两个if 来解决99%情况下不需要对if进行线程隔离的情况，使用volatile是为了防止指令重拍续导致的问题，分析如下：

```java
public static Singleton getSingleton() {
    if (instance == null) {                         //Single Checked
        synchronized (Singleton.class) {
            if (instance == null) {                 //Double Checked
                instance = new Singleton();
            }
        }
    }
    return instance ;
}
```

这段代码看起来很完美，很可惜，它是有问题。主要在于instance = new Singleton()这句，这并非是一个原子操作，事实上在 JVM 中这句话大概做了下面 3 件事情。

1. 给 instance 分配内存
2. 调用 Singleton 的构造函数来初始化成员变量
3. 将instance对象指向分配的内存空间（执行完这步 instance 就为非 null 了）

但是在 JVM 的即时编译器中存在指令重排序的优化。也就是说上面的第二步和第三步的顺序是不能保证的，最终的执行顺序可能是 1-2-3 也可能是 1-3-2。如果是后者，则在 3 执行完毕、2 未执行之前，被线程二抢占了，这时 instance 已经是非 null 了（但却没有初始化），所以线程二会直接返回 instance，然后使用，然后顺理成章地报错。

### 使用内部静态类

```java
public class Singleton {  
    private static class SingletonHolder {  
        private static final Singleton INSTANCE = new Singleton();  
    }  
    private Singleton (){}  
    public static final Singleton getInstance() {  
        return SingletonHolder.INSTANCE; 
    }  
}
```

这种写法仍然使用JVM本身机制保证了线程安全问题；由于 SingletonHolder 是私有的，除了 getInstance() 之外没有办法访问它，因此它是懒汉式的；同时读取实例的时候不会进行同步，没有性能缺陷；也不依赖 JDK 版本。

### 枚举 Enum

用枚举写单例实在太简单了！这也是它最大的优点。下面这段代码就是声明枚举实例的通常做法。
```java
public enum EasySingleton{
    INSTANCE;
}
```

我们可以通过EasySingleton.INSTANCE来访问实例，这比调用getInstance()方法简单多了。创建枚举默认就是线程安全的，所以不需要担心double checked locking，而且还能防止反序列化导致重新创建新的对象。但是还是很少看到有人这样写，可能是因为不太熟悉吧。

### 总结
一般来说，单例模式有五种写法：懒汉、饿汉、双重检验锁、静态内部类、枚举。上述所说都是线程安全的实现，文章开头给出的第一种方法不算正确的写法。