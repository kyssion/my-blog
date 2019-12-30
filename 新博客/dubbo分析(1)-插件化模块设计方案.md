> 基于dubbo 2.7 版本

都说duboo的插件化是基于spi我并不认同着一个观点。 我认为dubbo是自己实现了一波spi类似spring boot

总结：dubbo 并没有使用java的spi而是实现了一种更加强悍的spi机制（自动类加载机制）

# 核心类ExtensionLoader

这个类在整个dubbo中算是一个硬核的类了，总计1000多行代码，看名称就能知道这个类其实承载了dubbo整个动态加载的逻辑

Extension在dubbo的使用方法一般是这样的

```java
Xxx xxx = ExtensionLoader.getExtensionLoader(Xxx.class).getAdaptiveExtension();
```

核心其实就是两个方法，getExtensionLoader和getAdaptiveExtension，前者负责实例化一个ExtensionLoader 后者进行动态加载

## getExtensionLoader

这个方法很简单，就是将类型和ExtensionLoder对象之间的映射关系一一对应，并且初始化ExtensionLoader对象中的ObjectFactory 类型对象实例化工程方法

```java
public static <T> ExtensionLoader<T> getExtensionLoader(Class<T> type) {
    //获取扩展
    ExtensionLoader<T> loader = (ExtensionLoader<T>) EXTENSION_LOADERS.get(type);
    if (loader == null) {
        //创建并且赋值 扩展加载器
        EXTENSION_LOADERS.putIfAbsent(type, new ExtensionLoader<T>(type));
        loader = (ExtensionLoader<T>) EXTENSION_LOADERS.get(type);
    }
    return loader;
}

class ExtensionLoader{
    private ExtensionLoader(Class<?> type) {
        this.type = type;
        //这里初始化 类实例化工厂方法， 默认使用ExtensionFactory实现
        objectFactory = (type == ExtensionFactory.class ? null : ExtensionLoader.getExtensionLoader(ExtensionFactory.class).getAdaptiveExtension());
    }
}
```

## getAdaptiveExtension

这个类就是非常复杂了，我逻辑简化一下，只做关键点记录

```java
public T getAdaptiveExtension() {
    //获取缓存的自适应实例 ()
    Object instance = cachedAdaptiveInstance.get();
    if (instance == null) {
        try {
            //我擦。。。竟然是在createAdaptiveExtension中进行创建的，继续跟踪
            instance = createAdaptiveExtension();
            cachedAdaptiveInstance.set(instance);
        } catch (Throwable t) {
            createAdaptiveInstanceError = t;
            throw new IllegalStateException("Failed to create adaptive instance: " + t.toString(), t);
        }
    }
    return (T) instance;
}
```

> 发现一个关键方法createAdaptiveExtension

```java
private T createAdaptiveExtension() {
    try {
        return injectExtension((T) getAdaptiveExtensionClass().newInstance());
    } catch (Exception e) {
        throw new IllegalStateException("Can't create adaptive extension " + type + ", cause: " + e.getMessage(), e);
    }
}
```

有点恶心了 先看看getAdaptiveExtensionClass方法干嘛了吧

```
```