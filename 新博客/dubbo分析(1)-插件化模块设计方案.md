> 基于dubbo 2.7 版本

都说duboo的插件化是基于spi我并不认同着一个观点。 我认为dubbo是自己实现了一波spi类似spring boot

总结：dubbo 并没有使用java的spi而是实现了一种更加强悍的spi机制（自动类加载机制）

> 核心类ExtensionLoader

# dubbo 自己实现SPI机制

其实这一块的逻辑很简单,定位到了核心类ExtensionLoader的两个方法中

```java
public T getExtension(String name) {
    if (name == null || name.length() == 0)
        throw new IllegalArgumentException("Extension name == null");
    if ("true".equals(name)) {
        // 获取默认的拓展实现类
        return getDefaultExtension();
    }
    // Holder，顾名思义，用于持有目标对象
    Holder<Object> holder = cachedInstances.get(name);
    if (holder == null) {
        cachedInstances.putIfAbsent(name, new Holder<Object>());
        holder = cachedInstances.get(name);
    }
    Object instance = holder.get();
    // 双重检查
    if (instance == null) {
        synchronized (holder) {
            instance = holder.get();
            if (instance == null) {
                // 创建拓展实例
                instance = createExtension(name);
                // 设置实例到 holder 中
                holder.set(instance);
            }
        }
    }
    return (T) instance;
}
```

第二个核心方法 createExtension 这个是真正创建类型的方法

```java
@SuppressWarnings("unchecked")
private T createExtension(String name) {
    Class<?> clazz = getExtensionClasses().get(name);
    if (clazz == null) {
        throw findException(name);
    }
    try {
        T instance = (T) EXTENSION_INSTANCES.get(clazz);
        if (instance == null) {
            EXTENSION_INSTANCES.putIfAbsent(clazz, clazz.newInstance());
            instance = (T) EXTENSION_INSTANCES.get(clazz);
        }
        injectExtension(instance);
        Set<Class<?>> wrapperClasses = cachedWrapperClasses;
        if (CollectionUtils.isNotEmpty(wrapperClasses)) {
            for (Class<?> wrapperClass : wrapperClasses) {
                instance = injectExtension((T) wrapperClass.getConstructor(type).newInstance(instance));
            }
        }
        initExtension(instance);
        return instance;
    } catch (Throwable t) {
        throw new IllegalStateException("Extension instance (name: " + name + ", class: " +
                type + ") couldn't be instantiated: " + t.getMessage(), t);
    }
}
```


# 自适应扩展

这个类在整个dubbo中算是一个硬核的类了，总计1000多行代码，看名称就能知道这个类其实承载了dubbo整个动态加载的逻辑

Extension在dubbo的使用方法一般是这样的

```java
Xxx xxx = ExtensionLoader.getExtensionLoader(Xxx.class).getAdaptiveExtension();
```

这种方法获取的是这个类的自定义扩展信息,并且带上了参数校验 , 注意必须是被spi注解标记的类才可以进行使用

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

```java
private Class<?> getAdaptiveExtensionClass() {
    getExtensionClasses();
    if (cachedAdaptiveClass != null) {
        return cachedAdaptiveClass;
    }
    return cachedAdaptiveClass = createAdaptiveExtensionClass();
}
```

> 有一个方法 getExtensionClasses ， 不过这个方法很重要 ， 下面的所有的逻辑都是为了加载扩展类的并缓存在自己的内存数组上

不看源码了 ， 直接说结论 从一个指定的文件夹中的文件中获取像下面这样文本

```
adaptive=org.apache.dubbo.common.compiler.support.AdaptiveCompiler
jdk=org.apache.dubbo.common.compiler.support.JdkCompiler
javassist=org.apache.dubbo.common.compiler.support.JavassistCompiler
```

将这个文本整合出一套k v 结构的map 注意一种注解和一种类型@Adaptive和WrapperClass（ps 以当前类型为构造函数的类）

getAdaptiveExtensionClass 方法同样包含了三个逻辑，如下：

调用 getExtensionClasses 获取所有的拓展类
检查缓存，若缓存不为空，则返回缓存
若缓存为空，则调用 createAdaptiveExtensionClass 创建自适应拓展类
这三个逻辑看起来平淡无奇，似乎没有多讲的必要。但是这些平淡无奇的代码中隐藏了着一些细节，需要说明一下。首先从第一个逻辑说起，getExtensionClasses 这个方法用于获取某个接口的所有实现类。比如该方法可以获取 Protocol 接口的 DubboProtocol、HttpProtocol、InjvmProtocol 等实现类。在获取实现类的过程中，如果某个某个实现类被 Adaptive 注解修饰了，那么该类就会被赋值给 cachedAdaptiveClass 变量。此时，上面步骤中的第二步条件成立（缓存不为空），直接返回 cachedAdaptiveClass 即可


> 还有一个方法 createAdaptiveExtensionClass 这个方法非常特殊 , 是自动化生成扩展类的参数校验类...

```java
private Class<?> createAdaptiveExtensionClass() {
    //这里为什么用代码生成器来实现呢 type 是默认的接口 ,  通过一些逻辑动态的生成代码 , 以后再看
    String code = new AdaptiveClassCodeGenerator(type, cachedDefaultName).generate();
    ClassLoader classLoader = findClassLoader();
    org.apache.dubbo.common.compiler.Compiler compiler = ExtensionLoader.getExtensionLoader(org.apache.dubbo.common.compiler.Compiler.class).getAdaptiveExtension();
    return compiler.compile(code, classLoader);
}
```

> 注意这里的一端代码---自动生成Adaptive方法String code = new AdaptiveClassCodeGenerator(type, cachedDefaultName).generate();,其中的generate这一块应该是整个dubbo最难理解的地方了

```java
public String generate() {
    // no need to generate adaptive class since there's no adaptive method found.
    //必须使用使用还有Adaptive注解包括的类才能实现
    if (!hasAdaptiveMethod()) {
        throw new IllegalStateException("No adaptive method exist on extension " + type.getName() + ", refuse to create the adaptive class!");
    }

    StringBuilder code = new StringBuilder();
    code.append(generatePackageInfo());
    code.append(generateImports());
    code.append(generateClassDeclaration());

    Method[] methods = type.getMethods();
    for (Method method : methods) {
        code.append(generateMethod(method));
    }
    code.append("}");

    if (logger.isDebugEnabled()) {
        logger.debug(code.toString());
    }
    return code.toString();
}
```

spi这里其实写的并不是很合理，存在大量的问题，其实本质上dubbo在生成自适应类的时候，一个核心就是使用url作为参数，各种数据其实都是在url中获取的， 然后遍历

看一个编译之后的代码

```java
package org.apache.dubbo.rpc;

import org.apache.dubbo.common.extension.ExtensionLoader;


public class Protocol$Adaptive implements org.apache.dubbo.rpc.Protocol {
    public org.apache.dubbo.rpc.Exporter export(
        org.apache.dubbo.rpc.Invoker arg0)
        throws org.apache.dubbo.rpc.RpcException {
        if (arg0 == null) {
            throw new IllegalArgumentException(
                "org.apache.dubbo.rpc.Invoker argument == null");
        }

        if (arg0.getUrl() == null) {
            throw new IllegalArgumentException(
                "org.apache.dubbo.rpc.Invoker argument getUrl() == null");
        }

        org.apache.dubbo.common.URL url = arg0.getUrl();
        String extName = ((url.getProtocol() == null) ? "dubbo"
                                                      : url.getProtocol());

        if (extName == null) {
            throw new IllegalStateException(
                "Failed to get extension (org.apache.dubbo.rpc.Protocol) name from url (" +
                url.toString() + ") use keys([protocol])");
        }

        org.apache.dubbo.rpc.Protocol extension = (org.apache.dubbo.rpc.Protocol) ExtensionLoader.getExtensionLoader(org.apache.dubbo.rpc.Protocol.class)
                                                                                                 .getExtension(extName);

        return extension.export(arg0);
    }

    public java.util.List getServers() {
        throw new UnsupportedOperationException(
            "The method public default java.util.List org.apache.dubbo.rpc.Protocol.getServers() of interface org.apache.dubbo.rpc.Protocol is not adaptive method!");
    }

    public org.apache.dubbo.rpc.Invoker refer(java.lang.Class arg0,
        org.apache.dubbo.common.URL arg1)
        throws org.apache.dubbo.rpc.RpcException {
        if (arg1 == null) {
            throw new IllegalArgumentException("url == null");
        }
        org.apache.dubbo.common.URL url = arg1;
        String extName = ((url.getProtocol() == null) ? "dubbo"
                                                      : url.getProtocol());

        if (extName == null) {
            throw new IllegalStateException(
                "Failed to get extension (org.apache.dubbo.rpc.Protocol) name from url (" +
                url.toString() + ") use keys([protocol])");
        }

        org.apache.dubbo.rpc.Protocol extension = (org.apache.dubbo.rpc.Protocol) ExtensionLoader.getExtensionLoader(org.apache.dubbo.rpc.Protocol.class)
                                                                                                 .getExtension(extName);

        return extension.refer(arg0, arg1);
    }
    public void destroy() {
        throw new UnsupportedOperationException(
            "The method public abstract void org.apache.dubbo.rpc.Protocol.destroy() of interface org.apache.dubbo.rpc.Protocol is not adaptive method!");
    }
    public int getDefaultPort() {
        throw new UnsupportedOperationException(
            "The method public abstract int org.apache.dubbo.rpc.Protocol.getDefaultPort() of interface org.apache.dubbo.rpc.Protocol is not adaptive method!");
    }
}
```

注意上面的逻辑重点其实是 extName这个方法 ，  这个方法使用自动生成逻辑中的generateExtNameAssignment生成的

```java
private String generateExtNameAssignment(String[] value, boolean hasInvocation) {
    // TODO: refactor it
    String getNameCode = null;
    for (int i = value.length - 1; i >= 0; --i) {
        if (i == value.length - 1) {
            if (null != defaultExtName) {
                if (!"protocol".equals(value[i])) {
                    if (hasInvocation) {
                        getNameCode = String.format("url.getMethodParameter(methodName, \"%s\", \"%s\")", value[i], defaultExtName);
                    } else {
                        getNameCode = String.format("url.getParameter(\"%s\", \"%s\")", value[i], defaultExtName);
                    }
                } else {
                    getNameCode = String.format("( url.getProtocol() == null ? \"%s\" : url.getProtocol() )", defaultExtName);
                }
            } else {
                if (!"protocol".equals(value[i])) {
                    if (hasInvocation) {
                        getNameCode = String.format("url.getMethodParameter(methodName, \"%s\", \"%s\")", value[i], defaultExtName);
                    } else {
                        getNameCode = String.format("url.getParameter(\"%s\")", value[i]);
                    }
                } else {
                    getNameCode = "url.getProtocol()";
                }
            }
        } else {
            if (!"protocol".equals(value[i])) {
                if (hasInvocation) {
                    getNameCode = String.format("url.getMethodParameter(methodName, \"%s\", \"%s\")", value[i], defaultExtName);
                } else {
                    getNameCode = String.format("url.getParameter(\"%s\", %s)", value[i], getNameCode);
                }
            } else {
                getNameCode = String.format("url.getProtocol() == null ? (%s) : url.getProtocol()", getNameCode);
            }
        }
    }

    return String.format(CODE_EXT_NAME_ASSIGNMENT, getNameCode);
}

/**
    * @return
    */
private String generateExtensionAssignment() {
    return String.format(CODE_EXTENSION_ASSIGNMENT, type.getName(), ExtensionLoader.class.getSimpleName(), type.getName());
}
```

其中value是在Adaptive注解中标记的名称，dubbo将会对这些名称在url中进行自动化获取，如果是protocal类型将会直接从url协议参数中获取

>ps 注意，dubbo在这里做的其实并不好 ，  逻辑非常的混乱 ， 其中有一个非常重要的参数就是ExtName , 他的默认值是从AdaptiveClassCodeGenerator的构造函数中传入的，并且
调用这个构造函数的ExtendLoad是在初始化ExtendLoad class 的时候，解析SPI注解中的参数进行默认注入的 。。。 其实注意，这里本质上就是封装一层从url中获取参数然后给SPI实现类调用的逻辑

> 其他重要方法injectExtension获取这个类依赖的spi扩展属性 , 使用set注入到这个类中

```java
private T injectExtension(T instance) {

    if (objectFactory == null) {
        return instance;
    }

    try {
        for (Method method : instance.getClass().getMethods()) {
            if (!isSetter(method)) {
                continue;
            }
            /**
                * Check {@link DisableInject} to see if we need auto injection for this property
                */
            if (method.getAnnotation(DisableInject.class) != null) {
                continue;
            }
            Class<?> pt = method.getParameterTypes()[0];
            if (ReflectUtils.isPrimitives(pt)) {
                continue;
            }

            try {
                String property = getSetterProperty(method);
                Object object = objectFactory.getExtension(pt, property);
                if (object != null) {
                    method.invoke(instance, object);
                }
            } catch (Exception e) {
                logger.error("Failed to inject via method " + method.getName()
                        + " of interface " + type.getName() + ": " + e.getMessage(), e);
            }

        }
    } catch (Exception e) {
        logger.error(e.getMessage(), e);
    }
    return instance;
}
```

> 注意这个方法，dubbo的默认objectFactory使用的是ExtendsObjectFactory 所以，只能加载SPI的类型



