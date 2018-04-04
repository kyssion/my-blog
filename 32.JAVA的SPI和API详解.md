api 机制 好说其实就是定义一个接口然后使用他的一个实现类去进行上转型

```java
public class Main {
    public static void main(String[] args) {
        Myinterface myinterface = new MyInterfaceImg();
        myinterface.say();
    }
}
interface Myinterface{
    public String say();
}
class MyInterfaceImg implements  Myinterface{
    public String say() {
        return "create now";
    }
}
```

但是使用spi则是另一种特殊的方法

SPI 全称为 (Service Provider Interface) ,是JDK内置的一种服务提供发现机制(使用接口发现他的实现类-ServiceLoader<Search> s = ServiceLoader.load(Search.class);)。 目前有不少框架用它来做服务的扩展发现， 简单来说，它就是一种动态替换发现的机制， 举个例子来说， 有个接口，想运行时动态的给它添加实现，你只需要添加一个实现.而后，把新加的实现，描述给JDK知道就行啦（通过改一个文本文件即可） 公司内部，目前Dubbo框架和早期的common.log使用这种方法。

使用的结构图如下:

!()[blogimg/1.jpg]

其实使用spi的核心就是这个配置文件,这个配置文件在jar包的路径如下

```
└── META-INF
    └── services
        └── com.kys.接口名称  #配置文件的路径
```

我们都知道vm使用双亲委派机制的类加载器加载各种类(ClassLoader A -> System class loader -> Extension class loader -> Bootstrap class loader)
在spi 中,SPI 接口的代码中使用线程上下文类加载器(使用 ServiceLoader<HelloInterface> loaders = ServiceLoader.load(接口名称.class);)，就可以成功的加载到 SPI 实现的类.  

具体的实现见下面的代码

```java
public static <S> ServiceLoader<S> load(Class<S> service) {
    ClassLoader cl = Thread.currentThread().getContextClassLoader();
    return ServiceLoader.load(service, cl);
}
```

看一个实例

接口:
```java
package com.liu.spi;
 
public interface IA {
    void print();
}
```
三个实现类

```java
package com.liu.spi;
 
public class AIAImpl implements IA {
 
    public void print() {
        System.out.println("AIA");
    }
}

package com.liu.spi;
 
public class BIAImpl implements IA{
 
    public void print() {
        System.out.println("BIA");
    }
}

package com.liu.spi;
 
public class CIAImpl implements IA {
 
    public void print() {
        System.out.println("CIA");
    }
}
```

META-INF/services/com.liu.spi.IA这个文件的内容(如果使用maven工程构建在 src/main/resources/META-INF/services/com.liu.spi.IA这个目录)

```
com.liu.spi.AIAImpl
com.liu.spi.BIAImpl
com.liu.spi.CIAImpl
```

运行的主函数

```java
package com.liu.spi;
import java.util.Iterator;
import java.util.ServiceLoader;
public class IATest {
    public static void main(String[] args) {
        ServiceLoader<IA> spiLoader = ServiceLoader.load(IA.class); 
        Iterator<IA> iaIterator = spiLoader.iterator(); 
        while (iaIterator.hasNext()) { 
            iaIterator.next().print(); 
        } 
    }
}
``` 
