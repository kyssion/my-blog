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

> 我认为整个IOC过程中最应该关注的就是这两个问题 1. bean什么时候初始化的? 怎么初始化的? 2. bean之间的依赖关系是什么时候? 是怎么解决的?

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

这里其实知道结论就好了 ，没有必要追究细节 ， 这里spring将会通过spring的xml文件生成一系列的javabean的包装bean -> BeanDefinition , 然后放入默认生成的DefaultListableBeanFactory之中

#### 2. AnnotionAppicationContext

> 这个需要重点关注一下 ， 这个地方石


```java
@Override
public void refresh() throws BeansException, IllegalStateException {
    synchronized (this.startupShutdownMonitor) {
        // Prepare this context for refreshing.
        prepareRefresh();
        // Tell the subclass to refresh the internal bean factory.
        ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();
        // Prepare the bean factory for use in this context.
        prepareBeanFactory(beanFactory);
        try {
            // Allows post-processing of the bean factory in context subclasses.
            postProcessBeanFactory(beanFactory);
            // Invoke factory processors registered as beans in the context.
            invokeBeanFactoryPostProcessors(beanFactory);
            // Register bean processors that intercept bean creation.
            registerBeanPostProcessors(beanFactory);
            // Initialize message source for this context.
            initMessageSource();
            // Initialize event multicaster for this context.
            initApplicationEventMulticaster();
            // Initialize other special beans in specific context subclasses.
            onRefresh();
            // Check for listener beans and register them.
            registerListeners();
            // Instantiate all remaining (non-lazy-init) singletons.
            finishBeanFactoryInitialization(beanFactory);
            // Last step: publish corresponding event.
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
