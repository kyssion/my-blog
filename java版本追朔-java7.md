# 尝试使用资源

java7 针对资源使用的改进,通过这种方法,就不需要显示的声明文件关闭的语句了

```java
public static Object[] fromFile(String filePath) throws FileNotFoundException, IOException
{
    try (BufferedReader br = new BufferedReader(new FileReader(filePath)))
    {
        return read(br);
    } 
}
```

基本上，是上面的代码在Java 7中等同于下面的Java 6：

```java
public static Object[] fromFile(String filePath) throws FileNotFoundException, IOException
{

    BufferedReader br = null;

    try
    {
        br = new BufferedReader(new FileReader(filePath));

        return read(br);
    }
    catch (Exception ex)
    {
        throw ex;
    }
    finally
    {
        try
        {
            if (br != null) br.close();
        }
        catch(Exception ex)
        {
        }
    }

    return null;
}
```

但是还有一些不同的,就是使用java7 其实实在catch之前就关闭资源的

# java7 捕获多个异常

```java
try {

    // execute code that may throw 1 of the 3 exceptions below.

} catch(SQLException e) {
    logger.log(e);

} catch(IOException e) {
    logger.log(e);

} catch(Exception e) {
    logger.severe(e);
}
```

java7中可以简写为：

```java
try {

    // execute code that may throw 1 of the 3 exceptions below.

} catch(SQLException | IOException e) {
    logger.log(e);

} catch(Exception e) {
    logger.severe(e);
}
```

符合 可以 写多个，符合其中之一；

# java7 fork join 和nio2.0

这个说过很多了就不补充了

# 支持jvm 虚拟机中的动态类型语言

回到本文的主题，来看看Java语言、虚拟机与动态类型语言之间有什么关系。Java虚拟机毫无疑问是Java语言的运行平台，但他的使命并不仅限于此，早在1997年出版的《虚拟机规范》中就规划了这样一个愿景：“在未来，我们会对Java虚拟机进行适当的扩展，以便更好地支持其他语言运行于Java虚拟机之上”。而目前确实已经有许多动态类型语言运行于Java虚拟机之上了，如Clojure、Groovy、Jython和JRuby等，能够在同一个虚拟机上可以达到静态类型语言的严谨性与动态类型语言的灵活性，这是一件很美妙的事情。
但遗憾的是：Java虚拟机层面对动态类型语言的支持一直都有所欠缺，主要表现在方法调用方面：JDK 1.7以前的字节码指令集中，4条方法调用指令（invokevirtual、invokespecial、invokestatic、invokeinterface）的第一个参数都是被调用的方法的符号引用（CONSTANT_Methodref_info或者CONSTANT_InterfaceMethodref_info常量），前面已经提到过，方法的符号引用在编译时产生，而动态类型语言只有在运行期才能确定接收者类型。这样，在Java虚拟机上实现的动态类型语言就不得不使用其他方式（如编译时留个占位符类型，运行时动态生成字节码实现具体类型到占位符类型的适配）来实现，这样势必让动态类型语言实现的复杂度增加，也可能带来额外的性能或者内存开销。尽管可以利用一些办法（如Call Site Caching）让这些开销尽量变小，但这种底层问题终归是应当在虚拟机层面上去解决才最合适，因此在Java虚拟机层面上提供动态类型的直接支持就成为了java平台的发展趋势之一，这就是JDK1.7（JSR）中invokedynamic指令以及java.lang.invoke包出现的技术背景。

简单来说,就是方法在编译期间必须知道他所属的对象,但是针对一些弱类型语言并不需要知道所属的对象是谁,对一些jvm编程语言的开发造成了一定的困难

# java.lang.invoke包 的methodHandle支持

```java
import static java.lang.invoke.MethodHandles.lookup;
import java.lang.invoke.MethodHandle;
import java.lang.invoke.MethodType;
 
/**
 * JSR-292 Method Handle基础用法演示
 */
public class MethodHandleTest {
	static class ClassA {
		public void println(String s) {
			System.out.println(s);
		}
	}
 
	public static void main(String[] args) throws Throwable {
		Object obj = System.currentTimeMillis() % 2 == 0 ? System.out
				: new ClassA();
		// 无论obj 最终是哪个实现类，下面这句都正确调用到println方法
		getPrintlnMH(obj).invokeExact("icyfenix");
	}
 
	private static MethodHandle getPrintlnMH(Object reveiver) throws Throwable {
		/*
		 * MethodType：代表“方法类型”，包含了方法的返回值（methodType()的第一个参数）和具体参数(methodType()
		 * 第二个及以后参数)
		 */
		MethodType mt = MethodType.methodType(void.class, String.class);
		/*
		 * lookup()方法来自于MethodHandles.lookup，这句的作用是在指定类中查找符合给定的方法名称、方法类型，
		 * 并且符合调用权限的方法句柄
		 */
		/*
		 * 因为这里调用的是一个虚方法，按照Java语言的规则，方法第一个参数是隐式的，代表该方法的接收者，也即是this指向的对象，
		 * 这个参数以前是放在参数列表中进行传递的，而现在提供了bindTo()方法来完成这件事情
		 */
		return lookup().findVirtual(reveiver.getClass(), "println", mt).bindTo(
				reveiver);
	}
}
```

MethodHandle的使用方法和效果与Reflection有众多相似之处，不过，他们还是有以下这些区别：
从本质上讲，Reflection和MethodHandle机制都是在模拟方法调用，但Reflection是在模拟Java代码层次的方法调用，而MethodHandle是在模拟字节码层次的方法调用。在MethodHandles.lookup中的3个方法——findStatic()、findVirtual()、findSpecial()正是为了对应于invokestatic、invokevirtual&invokeinterface和invokespecial这几条字节码指令的执行权限校验行为，而这些底层细节在使用Reflection API时是不需要关心的。

Reflection中的java.lang.reflect.Method对象远比MethodHandle机制中的java.lang.invoke.MethodHandle对象所包含的信息多。前者是方法在Java一端的全面映像，包含了方法的签名、描述府以及方法属性表中各种属性的java端表示方式，还包含执行权限等的运行期信息。而后者仅仅包含与执行该方法相关的信息。用通俗的话来讲，Reflection是重量级，而MethodHandle是轻量级。

由于MethodHandle是对字节码的方法指令调用的模拟，所以理论上虚拟机在这方面做的各种优化（如方法内联），在MethodHandle上也应当可以采用类似思路去支持。而通过反射去调用方法则不行。
MethodHandle与Reflection除了上面列举的区别外，最关键的一点还在于去掉前面讨论施加的前提“仅站在Java语言的角度来看”：Reflection API的设计目标是只为java语言服务的，而MethodHandle则设计成可服务于所有Java虚拟机之上的语言，其中也包括Java语言。

