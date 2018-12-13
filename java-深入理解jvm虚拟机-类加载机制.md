### 类加载过程

类从被加载到虚拟机内存中开始,到卸载出内存为止,它的整个生命周期包括:**加载(Loading)、验证(Verification)、准备(Preparation)、解析(Resolution)、初始化(Initialization)、使用(Using)和卸载(Unloading)**7个阶段。其中验证、准备、解析3个部分统称为连接(Linking)

#### （1）加载阶段触发条件

> 主动引用

1. 使用new关键字实例化对象的时候、读取或设置一个类的静态字段(被final修饰、已在编译期把结果放入常量池的静态字段除外)的时候,以及调用一个类的静态方法的时候。
2. 使用java.lang.reflect包的方法对类进行反射调用的时候,如果类没有进行过初始化,则需要先触发其初始化。
3. 当初始化一个类的时候,如果发现其父类还没有进行过初始化,则需要先触发其父类的初始化。
4. 当虚拟机启动时,用户需要指定一个要执行的主类(包含main()方法的那个类),虚拟机会先初始化这个主类。
5. 当使用JDK1.7的动态语言支持时,如果一个java.lang.invoke.MethodHandle实例最后的解析结果REF_getStatic、REF_putStatic、REF_invokeStatic的方法句柄,并且这个方法句柄所对应的类没有进行过初始化,则需要先触发其初始化。

对于这5种会触发类进行初始化的场景,虚拟机规范中使用了一个很强烈的限定语:“有且只有”,这5种场景中的行为称为对一个类进行主动引用。除此之外,所有引用类的方式都不会触发初始化,称为被动引用。

> 被动引用举例

**被动使用类字段**: 通过子类引用父类的静态字段,不会导致子类初始化

```java
package test;
/**
 * 被动使用类字段演示一: 通过子类引用父类的静态字段,不会导致子类初始化
 **/
class SuperClass {
	static {
		System.out.println("SuperClass init!");
	}
	public static int value = 123;
}
class SubClass extends SuperClass {
	static {
		System.out.println("SubClass init!");
	}
}
/**
 * 非主动使用类字段演示
 **/
public class ClassLoadTest {
	public static void main(String[] args) {
		System.out.println(SubClass.value);
	}
}
```

对应上面的触发条件（1），调用了谁的static 触发谁

#### （2）类加载器

![](/blogimg/jvm/10.png)

bootstrapClassLoader：加载核心jar

Extension ClassLoader：加载lib/ext中的jar

Application ClassLoader：加载path中的jar

User ClassLoader：用户自定义的jar

java中存在这么多类加载机制的主要原因就是要保证核心类加载的过程相同，识别相同，因为java 在 判读一个类是否是相同的判断方法除了使用类名称还使用类的加载机制来进行相关的判断的

### 2.验证阶段

验证是连接阶段的第一步,这一阶段的目的是为了确保Class文件的字节流中包含的信息符合当前虚拟机的要求,并且不会危害虚拟机自身的安全

文件格式验证是否是魔数0xCAFEBABE开头
1. 元数据验证
2. 字节码验证
3. 符号引用验证

### 3.准备阶段

准备阶段是正式为类变量分配内存并设置类变量初始值的阶段,这些变量所使用的内存都将在方法区中进行分配。这个阶段中有两个容易产生混淆的概念需要强调一下,首先,这时候进行内存分配的仅包括类变量(被static修饰的变量),而不包括实例变量,实例变量将会在对象实例化时随着对象一起分配在Java堆中。

注意这里初始的是初始值

```java
public static int value=123;
```

值的初始化的时间将是在初始化阶段赋值，当前阶段只是使用默认值0

### 4.解析

解析各种类属性

### 5.初始化

最后阶段各种属性最终赋值