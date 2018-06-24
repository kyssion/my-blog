## 深入springBoot-@Enable***注解和@import注解解惑

spring boot的自动配置功能相当强悍，其强悍的更本在于提供了Eable*** 这种自动化配置，之前的博客，简要分析如何自定义starter，这里对他进行一下补充

### 首先我们观察@SpringBoot注解

这个注解是一个组合注解，她提供自动化配置的注解是@EableAutoConfiguration注解

```java
@SuppressWarnings("deprecation")
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@AutoConfigurationPackage
@Import(EnableAutoConfigurationImportSelector.class)
public @interface EnableAutoConfiguration {
    String ENABLED_OVERRIDE_PROPERTY = "spring.boot.enableautoconfiguration";
    Class<?>[] exclude() default {};
    String[] excludeName() default {};
}
```

类似EableAutoConfiguration这样的@Eable***注解，都会使用@Import注解导入一写自动化配置bean，讲一些自动化配置类进行自动导入

#### @Import注解导入配置方式的三种类型

1. 第一类：直接导入配置类

```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Import({SchedulingConfiguration.class})
@Documented
public @interface EnableScheduling {
}
```

```java
@Configuration
@Role(BeanDefinition.ROLE_INFRASTRUCTURE)
public class SchedulingConfiguration {
 
	@Bean(name = TaskManagementConfigUtils.SCHEDULED_ANNOTATION_PROCESSOR_BEAN_NAME)
	@Role(BeanDefinition.ROLE_INFRASTRUCTURE)
	public ScheduledAnnotationBeanPostProcessor scheduledAnnotationProcessor() {
		return new ScheduledAnnotationBeanPostProcessor();
	}
 
}
```

直接导入配置类SchedulingConfiguration，这个类注解了@Configuration，且注册了一个scheduledAnnotationProcessor的Bean

2. 第二类：依据条件选择配置类

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Import(AsyncConfigurationSelector.class)
public @interface EnableAsync {
    Class<? extends Annotation> annotation() default Annotation.class;
    boolean proxyTargetClass() default false;
    AdviceMode mode() default AdviceMode.PROXY;
    int order() default Ordered.LOWEST_PRECEDENCE;
 
}
```

```java 
public class AsyncConfigurationSelector extends AdviceModeImportSelector<EnableAsync> {
	private static final String ASYNC_EXECUTION_ASPECT_CONFIGURATION_CLASS_NAME =
			"org.springframework.scheduling.aspectj.AspectJAsyncConfiguration";
	@Override
	public String[] selectImports(AdviceMode adviceMode) {
		switch (adviceMode) {
			case PROXY:
				return new String[] { ProxyAsyncConfiguration.class.getName() };
			case ASPECTJ:
				return new String[] { ASYNC_EXECUTION_ASPECT_CONFIGURATION_CLASS_NAME };
			default:
				return null;
		}
	}
}
```

- AsyncConfigurationSelector通过条件来选择需要导入的配置类，
- AsyncConfigurationSelector的根接口为ImportSelector，这个接口需要重写selectImports方法，在此方法内进行事先条件判断。 AdviceMode adviceMode 就是 调用注解中的AdivceMode
- 若adviceMode为PORXY，则返回ProxyAsyncConfiguration这个配置类。
- 若activeMode为ASPECTJ，则返回AspectJAsyncConfiguration配置类。

3. 第三类：动态注册Bean

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Import(AspectJAutoProxyRegistrar.class)
public @interface EnableAspectJAutoProxy {
    boolean proxyTargetClass() default false;
}
```

```java
class AspectJAutoProxyRegistrar implements ImportBeanDefinitionRegistrar {
    @Override
    public void registerBeanDefinitions(
            AnnotationMetadata importingClassMetadata, BeanDefinitionRegistry registry) {
        AopConfigUtils.registerAspectJAnnotationAutoProxyCreatorIfNecessary(registry);
        AnnotationAttributes enableAspectJAutoProxy =
                AnnotationConfigUtils.attributesFor(importingClassMetadata, EnableAspectJAutoProxy.class);
        if (enableAspectJAutoProxy.getBoolean("proxyTargetClass")) {
            AopConfigUtils.forceAutoProxyCreatorToUseClassProxying(registry);
        }
        if (enableAspectJAutoProxy.getBoolean("exposeProxy")) {
            AopConfigUtils.forceAutoProxyCreatorToExposeProxy(registry);
        }
    }

}
```

AspectJAutoProxyRegistrar 实现了ImportBeanDefinitionRegistrar接口，ImportBeanDefinitionRegistrar的作用是在运行时自动添加Bean到已有的配置类，通过重写方法：

```java
@Override
public void registerBeanDefinitions(AnnotationMetadata importingClassMetadata, BeanDefinitionRegistry registry)
```

其中，AnnotationMetadata参数用来获得当前配置类上的注解；BeanDefinittionRegistry参数用来注册Bean。