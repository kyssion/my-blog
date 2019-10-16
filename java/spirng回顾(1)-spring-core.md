spring 从3.0 开始支持java配置所以这里整理一下spring 3之后重要的知识

# spring application

回顾一下application的东西，负责初始化spring bean容器的非常重要的类

# bean

在spring中所有的javabean都将会初始化为BeanDefinition对象

这个类其实承载了javabean中所有的元数据包括：

1. javabean中的各种属性，类名等
2. javabean的实例化对象
3. Bean行为配置元素，用于声明Bean在容器中的行为（作用域，生命周期回调等）
4. 对其他bean进行工作所需的引用。这些引用也称为协作者或依赖项

除了包含有关如何创建特定bean的信息的bean定义之外，通过applicationcontext方法getBeanFactory()返回的BeanFactory 实现DefaultListableBeanFactory可以实现javabean的手动注入。DefaultListableBeanFactory 通过registerSingleton(..)和 registerBeanDefinition(..)方法支持此注册。

# spring 依赖注入注意问题

