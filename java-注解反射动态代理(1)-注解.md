## java注解，@，注解有什么用

@是java注解，即annotation。

1. 可以理解为插件，是代码级别的插件，在类的方法上写：@XXX，就是在代码上插入了一个插件。

2. Java注解是附加在代码中的一些元信息，用于一些工具在编译、运行时进行解析和使用，起到说明、配置的功能。
注解不会也不能影响代码的实际逻辑，仅仅起到辅助性的作用


## 元注解和自定义注解

java中有很多的注解比如@Override等等，这些注解其实是jdk内部自己声明的注解，而这些注解的声明就依赖于注解的注解的元注解

### 元注解类型

1. @target 声明注解的对象范围

```java
@Target({ElementType.FIELD,ElementType.LOCAL_VARIABLE})
```

注解类型包括

类型名称|限制范围
---|---
construction|构造函数 
FIeld|变量域
LOCAL_VARIABLE|用于描述局部变量
METHOD|用于描述方法
PACKAGE|用于描述包
PARAMETER|用于描述参数
TYPE|用于描述类、接口(包括注解类型) 或enum声明

2. @Retention声明注解的保留范围

类型|保留范围
---|---
SOURCE|在源文件中有效（即源文件保留）
CLASS|在class文件中有效（即class保留）
RUNTIME|在运行时有效（即运行时保留）

3. @Documented注解的文档的化 

- 用于描述其它类型的annotation应该被作为被标注的程序成员的公共API，因此可以被例如javadoc此类的工具文档化。Documented是一个标记注解，没有成员。

4. @Inherited --注解的继承化   

元注解是一个标记注解，@Inherited阐述了某个被标注的类型是被继承的。如果一个使用了@Inherited修饰的annotation类型被用于一个class，则这个annotation将被用于该class的子类。

> 注意：@Inherited annotation类型是被标注过的class的子类所继承。类并不从它所实现的接口继承annotation，方法并不从它所重载的方法继承annotation。

> 注意：当@Inherited annotation类型标注的annotation的Retention是RetentionPolicy.RUNTIME，则反射API增强了这种继承性。如果我们使用java.lang.reflect去查询一个@Inherited annotation类型的annotation时，反射代码检查将展开工作：检查class和其父类，直到发现指定的annotation类型被发现，或者到达类继承结构的顶层。