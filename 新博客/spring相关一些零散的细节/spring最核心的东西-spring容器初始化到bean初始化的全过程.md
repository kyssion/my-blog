
> 引申: 其实一开始不想写这篇文章的 , 奈何发现市面上的文章大部分都是一知半解 . 索性整理一篇文章方便以后阅读查阅

这次就不一开始就长篇大论了 ,  先说一个问题 ,为啥我们要研究spring 中bean的初始化顺序

# 为啥研究spring中javabean的初始化顺序

spring 框架是个啥? -> 本质上是一个IOC框架,解决依赖问题的玩意 , 依赖问题的核心承载点是啥? 是对象\javabean , 所以如果把这一块搞明白了,其实整个spring框架已经差不多搞透彻了.

# spring中bean到底是咋初始化的啊?

其实扒开spring的外衣 , 其实最核心的东西是BeanFactory , spring自己能找到的所有的java bean 全在里面 , 这个就是整个spring的数据中心

> 如果让我说spring最大的成就是什么 , 我认为spring最大的成就就是实现整个容器中java对象逻辑的托管功能 , 也就是我认为的IOC

# spring容器初始化的开端ApplicationContext

> 这个是spring整个java对象管理运行的开端,我称它为始祖种子类

> 注意永远记住spring是一个庞大臃肿功能强大的java框架 , 所以ApplicationContext的实现类特多,挑几个重点来说

1. spring boot 中使用的ApplicationContext -> AnnotationConfigApplicationContext -> 使用java配置来实现将javabean信息注入到容器
2. spring中最常用的ApplicationContext -> ClassPathXmlApplicationContext -> 使用xml来将javabean信息注入到容器

> 这两个类都有继承自AbstractApplication 所有的spring对象初始化的时候都会调用这个通用的类 , 整个bean初始化,容器加载相关的逻辑都是在这里面的

# spring IOC过程中我们最应该关注什么问题

> 我认为整个IOC过程中最应该关注的就是这两个问题 1. bean什么时候初始化的? 怎么初始化的? 2. bean之间的依赖关系是什么时候? 是怎么解决的? 3. 特殊状态的javabean比如lookup和lazy是如何做的

## bean什么时候初始化的

spring中bean的初始化的过程 ， 我认为分为如下的几个过程

1. java bean 加载进容器 ， 并且根据类型进行一定的初始化
2. 处理 java bean的依赖关系

> 这里梳理一下他们的过程

### javabean加载进容器， 并且根据类型进行一定的初始化操作

> 这一步中 ClassPathXMLApplicationContext和 AnnotationConfigApplicationContext的操作是不同的

#### 1. ClassPathXMLApplication 

> ClassPathApplicationContext 在spring中属于元老了 ， 他的着一块的支持是在AbstractApplicationContext中的refresh()方法（下面会给出源码）中实现的

最核心的逻辑是在ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();这一行中

```java
protected ConfigurableListableBeanFactory obtainFreshBeanFactory() {
    refreshBeanFactory();
    return getBeanFactory();
}
```

这里其实知道结论就好了 ，没有必要追究细节 ， 这里spring将会通过spring的xml文件生成一系列的javabean的包装bean -> BeanDefinition , 
然后放入默认生成的DefaultListableBeanFactory之中, 注意在spring中 所有的java bean在解析的过程中都会变成 BeanDefinition(有些特殊的单例不是用BeanDefinition封装的)

#### 2. AnnotionAppicationContext

> 这个需要重点关注一下 ， 这个context和classPathXmLApplicationContext有一定的区别 , 他是继承自GenericApplicationContext , GenericApplicationContext是新一代spring使用注解进行bean配置的核心Context

> 首先注意下这个ApplicationContext的构造方法

> AnnotatedBeanDefinitionReader 和 ClassPathBeanDefinitionScanner 都是初始化用来将使用class或者basePackages名称加载的BeanDefinition注册进GenericApplicationContext的工具类

```java
//将指定的java bean的配置类对象
public AnnotationConfigApplicationContext(Class<?>... componentClasses) {
    this();
    register(componentClasses);
    refresh();
}
//将制定的包下所有的配置类对象
public AnnotationConfigApplicationContext(String... basePackages) {
    this();
    scan(basePackages);
    refresh();
}
//初始化注册BeanDefinition所需要的加载器 -> 这两个方法很重要的 , 初始化了很多process比如AutowiredAnnotationBeanPostProcessor和
// CommonAnnotationBeanPostProcessor用来处理@Autowrite注解等等
public AnnotationConfigApplicationContext() {
    this.reader = new AnnotatedBeanDefinitionReader(this);
    this.scanner = new ClassPathBeanDefinitionScanner(this);
}
```


> 最核心的方法AbstractAplication的refresh()方法 , 这个方法完成了整个spring声明周期的初始化


```java
@Override
public void refresh() throws BeansException, IllegalStateException {
    synchronized (this.startupShutdownMonitor) {
        // 准备，记录容器的启动时间startupDate, 标记容器为激活，初始化上下文环境如文件路径信息，验证必填属性是否填写
        prepareRefresh();
        // 获取新的beanFactory，销毁原有beanFactory、为每个bean生成BeanDefinition等
        ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();
        // 初始化beanfactory的各种属性
        prepareBeanFactory(beanFactory);
        try {
            // 模板方法，此时，所有的beanDefinition已经加载，但是还没有实例化。
            //允许在子类中对beanFactory进行扩展处理。比如添加ware相关接口自动装配设置，添加后置处理器等，是子类扩展prepareBeanFactory(beanFactory)的方法
            postProcessBeanFactory(beanFactory);
            // 实例化并调用所有注册的beanFactory后置处理器（实现接口BeanFactoryPostProcessor的bean，在beanFactory标准初始化之后执行）
            invokeBeanFactoryPostProcessors(beanFactory);
            // 实例化和注册beanFactory中扩展了BeanPostProcessor的bean
            //例如：
            // AutowiredAnnotationBeanPostProcessor(处理被@Autowired注解修饰的bean并注入)
            // RequiredAnnotationBeanPostProcessor(处理被@Required注解修饰的方法)
            // CommonAnnotationBeanPostProcessor(处理@PreDestroy、@PostConstruct、@Resource等多个注解的作用)等。
            registerBeanPostProcessors(beanFactory);
            // Initialize message source for this context.
            initMessageSource();
            // Initialize event multicaster for this context.
            initApplicationEventMulticaster();
            // 模板方法，在容器刷新的时候可以自定义逻辑，不同的Spring容器做不同的事情。
            onRefresh();
            // 注册监听器，广播early application events
            registerListeners();
            // 实例化所有剩余的（非懒加载）单例
            // 比如invokeBeanFactoryPostProcessors方法中根据各种注解解析出来的类，在这个时候都会被初始化。
            // 实例化的过程各种BeanPostProcessor开始起作用。
            finishBeanFactoryInitialization(beanFactory);
            // refresh做完之后需要做的其他事情。
            // 清除上下文资源缓存（如扫描中的ASM元数据）
            // 初始化上下文的生命周期处理器，并刷新（找出Spring容器中实现了Lifecycle接口的bean并执行start()方法）。
            // 发布ContextRefreshedEvent事件告知对应的ApplicationListener进行响应的操作
            finishRefresh();
        } catch (BeansException ex) {
            if (logger.isWarnEnabled()) {
                logger.warn("Exception encountered during context initialization - " +
                        "cancelling refresh attempt: " + ex);
            }
            // Destroy already created singletons to avoid dangling resources.
            destroyBeans();
            // Reset 'active' flag.
            cancelRefresh(ex);
            // Propagate exception to caller.
            throw ex;
        } finally {
            // Reset common introspection caches in Spring's core, since we
            // might not ever need metadata for singleton beans anymore...
            resetCommonCaches();
        }
    }
}
```

> 我们只要注意这个方法 finishBeanFactoryInitialization() spring所有非内置的单例 javabean都是在这里初始化的 , 主要是下面的这一行

```java
protected void finishBeanFactoryInitialization(ConfigurableListableBeanFactory beanFactory) {
    ...

    // Instantiate all remaining (non-lazy-init) singletons.
    beanFactory.preInstantiateSingletons();
}
```

这行做了beanFactory中所有单例 javabean初始化和依赖处理的, 进入看一下

```java
@Override
public void preInstantiateSingletons() throws BeansException {
    ....
    // Trigger initialization of all non-lazy singleton beans...
    for (String beanName : beanNames) {
        RootBeanDefinition bd = getMergedLocalBeanDefinition(beanName);
        if (!bd.isAbstract() && bd.isSingleton() && !bd.isLazyInit()) {
            if (isFactoryBean(beanName)) {
                Object bean = getBean(FACTORY_BEAN_PREFIX + beanName);
                if (bean instanceof FactoryBean) {
                    final FactoryBean<?> factory = (FactoryBean<?>) bean;
                    boolean isEagerInit;
                    if (System.getSecurityManager() != null && factory instanceof SmartFactoryBean) {
                        isEagerInit = AccessController.doPrivileged((PrivilegedAction<Boolean>)
                                        ((SmartFactoryBean<?>) factory)::isEagerInit,
                                getAccessControlContext());
                    }
                    else {
                        isEagerInit = (factory instanceof SmartFactoryBean &&
                                ((SmartFactoryBean<?>) factory).isEagerInit());
                    }
                    if (isEagerInit) {
                        getBean(beanName);
                    }
                }
            }
            else {
                getBean(beanName);
            }
        }
    }
    ......
}
```

> 其实他的核心逻辑就是在这里,通过使用getBean方法来尽心初始化的-> 而这个方法同样也是我们每次使用ApplicationContext获取对象的时候所需要调用的类

> 这个getBean方法非常长,其实本质上就是尝试获取一个javabean,内部实现了bean的创建,依赖管理等等的逻辑,贴一个单例模式的核心代码吧

```java
@SuppressWarnings("unchecked")
protected <T> T doGetBean(final String name, @Nullable final Class<T> requiredType,
        @Nullable final Object[] args, boolean typeCheckOnly) throws BeansException {
    ....
    // Create bean instance.
    if (mbd.isSingleton()) {
        sharedInstance = getSingleton(beanName, () -> {
            try {
                return createBean(beanName, mbd, args);
            }
            catch (BeansException ex) {
                // Explicitly remove instance from singleton cache: It might have been put there
                // eagerly by the creation process, to allow for circular reference resolution.
                // Also remove any beans that received a temporary reference to the bean.
                destroySingleton(beanName);
                throw ex;
            }
        });
        bean = getObjectForBeanInstance(sharedInstance, name, beanName, mbd);
    }
    ....
}
```

外层的getSingleton 方法自然就是获取单例而其中的会掉就是当单例不存在的时候,进行创建的逻辑,进入一下这个createBean

> 这里代码依然很多但是这个类最终依赖得了doCreateBean方法,所以直接看doCreateBean方法里有啥,但是这里执行了一个前置处理逻辑(postProcessBeforeInstantiation)方法来超前处理bean初始化

```java
try {
    // Give BeanPostProcessors a chance to return a proxy instead of the target bean instance.
    Object bean = resolveBeforeInstantiation(beanName, mbdToUse);
    if (bean != null) {
        return bean;
    }
}
catch (Throwable ex) {
    throw new BeanCreationException(mbdToUse.getResourceDescription(), beanName,
            "BeanPostProcessor before instantiation of bean failed", ex);
}
try {
    Object beanInstance = doCreateBean(beanName, mbdToUse, args);
    if (logger.isTraceEnabled()) {
        logger.trace("Finished creating instance of bean '" + beanName + "'");
    }
    return beanInstance;
}
```

> 接下来就是重点了doCreateBean方法,解决了循环引用问题和实现提早曝光的逻辑都是在这里

```java
protected Object doCreateBean(final String beanName, final RootBeanDefinition mbd, final @Nullable Object[] args)
        throws BeanCreationException {
            ......
    // Eagerly cache singletons to be able to resolve circular references
    // even when triggered by lifecycle interfaces like BeanFactoryAware.
    boolean earlySingletonExposure = (mbd.isSingleton() && this.allowCircularReferences &&
            isSingletonCurrentlyInCreation(beanName));
    if (earlySingletonExposure) {
        if (logger.isTraceEnabled()) {
            logger.trace("Eagerly caching bean '" + beanName +
                    "' to allow for resolving potential circular references");
        }
        addSingletonFactory(beanName, () -> getEarlyBeanReference(beanName, mbd, bean));
    }

    // Initialize the bean instance.
    Object exposedObject = bean;
    try {
        populateBean(beanName, mbd, instanceWrapper);
        exposedObject = initializeBean(beanName, exposedObject, mbd);
    }
    catch (Throwable ex) {
        if (ex instanceof BeanCreationException && beanName.equals(((BeanCreationException) ex).getBeanName())) {
            throw (BeanCreationException) ex;
        }
        else {
            throw new BeanCreationException(
                    mbd.getResourceDescription(), beanName, "Initialization of bean failed", ex);
        }
    }

    if (earlySingletonExposure) {
        Object earlySingletonReference = getSingleton(beanName, false);
        if (earlySingletonReference != null) {
            if (exposedObject == bean) {
                exposedObject = earlySingletonReference;
            }
            else if (!this.allowRawInjectionDespiteWrapping && hasDependentBean(beanName)) {
                String[] dependentBeans = getDependentBeans(beanName);
                Set<String> actualDependentBeans = new LinkedHashSet<>(dependentBeans.length);
                for (String dependentBean : dependentBeans) {
                    if (!removeSingletonIfCreatedForTypeCheckOnly(dependentBean)) {
                        actualDependentBeans.add(dependentBean);
                    }
                }
                if (!actualDependentBeans.isEmpty()) {
                    throw new BeanCurrentlyInCreationException(beanName,
                            "Bean with name '" + beanName + "' has been injected into other beans [" +
                            StringUtils.collectionToCommaDelimitedString(actualDependentBeans) +
                            "] in its raw version as part of a circular reference, but has eventually been " +
                            "wrapped. This means that said other beans do not use the final version of the " +
                            "bean. This is often the result of over-eager type matching - consider using " +
                            "'getBeanNamesOfType' with the 'allowEagerInit' flag turned off, for example.");
                }
            }
        }
    }
    // Register bean as disposable.
    try {
        registerDisposableBeanIfNecessary(beanName, bean, mbd);
    }
    catch (BeanDefinitionValidationException ex) {
        throw new BeanCreationException(
                mbd.getResourceDescription(), beanName, "Invalid destruction signature", ex);
    }

    return exposedObject;
}
```
> 这里有几个重点


> 1. 我们的javabean属性注入是在 populateBean方法中实现的,他的内部逻辑是使用了递归来循环的填冲属性. 这里也处理了构造函数等等依赖关系.

> 这里要插一句AutoWriterAnnotionBeanPostProcessor

> AutoWriterAnnotionBeanPostProcessor , 在这里有一个特殊的处理逻辑可以借鉴一下

```java
private InjectionMetadata findAutowiringMetadata(String beanName, Class<?> clazz, @Nullable PropertyValues pvs) {
    // Fall back to class name as cache key, for backwards compatibility with custom callers.
    String cacheKey = (StringUtils.hasLength(beanName) ? beanName : clazz.getName());
    // Quick check on the concurrent map first, with minimal locking.
    InjectionMetadata metadata = this.injectionMetadataCache.get(cacheKey);
    if (InjectionMetadata.needsRefresh(metadata, clazz)) {
        synchronized (this.injectionMetadataCache) {
            metadata = this.injectionMetadataCache.get(cacheKey);
            if (InjectionMetadata.needsRefresh(metadata, clazz)) {
                if (metadata != null) {
                    metadata.clear(pvs);
                }
                metadata = buildAutowiringMetadata(clazz);
                this.injectionMetadataCache.put(cacheKey, metadata);
            }
        }
    }
    return metadata;
}
```

> AutoWriterAnnotionBeanPostProcessor 将需要的属性,使用反射并将反射缓存了一下(injectionMetadataCache) , 来加快性能

> 2. 依赖关系处理

其实看上面doCreate的逻辑有一个earlySingletonExposure变量, spring在执行到这里的时候将会自动的将这个还没有进行初始化的类(也就是当bean为单例 && 容器配置允许循环依赖 && bean正在创建)的时候,将会在BeanFactory中设置第三级缓存, key是当前的bean的名称,value是一个工厂方法 , 很简单就是返回当前的类

```java
protected Object getEarlyBeanReference(String beanName, RootBeanDefinition mbd, Object bean) {
    Object exposedObject = bean;
    if (!mbd.isSynthetic() && hasInstantiationAwareBeanPostProcessors()) {
        for (BeanPostProcessor bp : getBeanPostProcessors()) {
            if (bp instanceof SmartInstantiationAwareBeanPostProcessor) {
                SmartInstantiationAwareBeanPostProcessor ibp = (SmartInstantiationAwareBeanPostProcessor) bp;
                exposedObject = ibp.getEarlyBeanReference(exposedObject, beanName);
            }
        }
    }
    return exposedObject;
}
```

> ps: spring 如何解决循环引用的?

这个可以看一下spring的getBean的逻辑 , 其中有一段这样的代码

```java
protected Object getSingleton(String beanName, boolean allowEarlyReference) {
    Object singletonObject = this.singletonObjects.get(beanName);
    if (singletonObject == null && isSingletonCurrentlyInCreation(beanName)) {
        synchronized (this.singletonObjects) {
            singletonObject = this.earlySingletonObjects.get(beanName);
            if (singletonObject == null && allowEarlyReference) {
                ObjectFactory<?> singletonFactory = this.singletonFactories.get(beanName);
                if (singletonFactory != null) {
                    singletonObject = singletonFactory.getObject();
                    this.earlySingletonObjects.put(beanName, singletonObject);
                    this.singletonFactories.remove(beanName);
                }
            }
        }
    }
    return singletonObject;
}
```

如果第一层缓存没有找到,就从早起类里找如果早期类里还没有,就使用工厂方法获取

> 聊一下这三层缓存都干了啥

第一层: 所有的初始化完成的单例bean
早期的bean: 被循环引用触发了,并且还没有初始化完成的bean
第三层: 正在被初始化的bean

> 如何解决循环引用就很简单了 , 如果A依赖了B 并且B依赖了A , 当A初始化了B的时候, B初始化时将会从第三层引用中获取当前的提早曝光的类,从而实现了解决循环引用,并且spring的实现,还实现了多线程模式下也可以进行循环应用的逻辑

> 还没完,整个生命周期还没有彻底搞懂

