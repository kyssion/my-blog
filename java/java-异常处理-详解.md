## 异常的体系结构

Java把异常当作对象来处理，并定义一个基类java.lang.Throwable作为所有异常的超类。

在Java API中已经定义了许多异常类，这些异常类分为两大类，错误Error和异常Exception。

Java异常层次结构图如下图所示：

![](blogimg/java/11.png)

从图中可以看出所有异常类型都是内置类Throwable的子类，因而Throwable在异常类的层次结构的顶层。

接下来Throwable分成了两个不同的分支，一个分支是Error，它表示不希望被程序捕获或者是程序无法处理的错误。另一个分支是Exception，它表示用户程序可能捕捉的异常情况或者说是程序可以处理的异常。其中异常类Exception又分为运行时异常(RuntimeException)和非运行时异常。

Java异常又可以分为不受检查异常（Unchecked Exception）和检查异常（Checked Exception）。

下面将详细讲述这些异常之间的区别与联系：

- Error：Error类对象由 Java 虚拟机生成并抛出，大多数错误与代码编写者所执行的操作无关。如Java虚拟机运行错误（Virtual MachineError），内存不足错误OutOfMemoryError。这些异常发生时，Java虚拟机（JVM）一般会选择线程终止；还有发生在虚拟机试图执行应用时，如类定义错误（NoClassDefFoundError）、链接错误（LinkageError）。这些错误是不可查的，因为它们在应用程序的控制和处理能力之外，而且绝大多数是程序运行时不允许出现的状况。对于设计合理的应用程序来说，即使确实发生了错误，本质上也不应该试图去处理它所引起的异常状况。在Java中，错误通常是使用Error的子类描述。
- Exception：在Exception分支中有一个重要的子类RuntimeException（运行时异常），该类型的异常自动为你所编写的程序定义ArrayIndexOutOfBoundsException（数组下标越界）、NullPointerException（空指针异常）、ArithmeticException（算术异常）、MissingResourceException（丢失资源）、ClassNotFoundException（找不到类）等异常，这些异常是不检查异常，程序中可以选择捕获处理，也可以不处理。这些异常一般是由程序逻辑错误引起的，程序应该从逻辑角度尽可能避免这类异常的发生；而RuntimeException之外的异常我们统称为非运行时异常，类型上属于Exception类及其子类，从程序语法角度讲是必须进行处理的异常，如果不处理，程序就不能编译通过。如IOException、SQLException等以及用户自定义的Exception异常，一般情况下不自定义检查异常。

> 注意：Error和Exception的区别：Error通常是灾难性的致命的错误，是程序无法控制和处理的，当出现这些异常时，Java虚拟机（JVM）一般会选择终止线程；Exception通常情况下是可以被程序处理的，并且在程序中应该尽可能的去处理这些异常。

> 除了RuntimeException及其子类以外，其他的Exception类及其子类都属于检查异常，当程序中可能出现这类异常，要么使用try-catch语句进行捕获，要么用throws子句抛出，否则编译无法通过。

> 不受检查异常：包括RuntimeException及其子类和Error。

## 异常抑制(看下面这段代码)

```java
public static void main(String[] args) {
    try {
        FileInputStream inputStream = new FileInputStream(new File("test"));
        Throwable var2 = null;

        try {
            System.out.println(inputStream.read());
        } catch (Throwable var12) {
            var2 = var12;
            throw var12;
        } finally {
            if (inputStream != null) {
                if (var2 != null) {
                    try {
                        inputStream.close();
                    } catch (Throwable var11) {
                        var2.addSuppressed(var11);
                    }
                } else {
                    inputStream.close();
                }
            }

        }

    } catch (IOException var14) {
        throw new RuntimeException(var14.getMessage(), var14);
    }
}
```

大家可能注意到代码中有一处对异常的特殊处理：

```java
var2.addSuppressed(var11);
```

这是try-with-resource语法涉及的另外一个知识点，叫做异常抑制。当对外部资源进行处理（例如读或写）时，如果遭遇了异常，且在随后的关闭外部资源过程中，又遭遇了异常，那么你catch到的将会是对外部资源进行处理时遭遇的异常，关闭资源时遭遇的异常将被“抑制”但不是丢弃，通过异常的getSuppressed方法，可以提取出被抑制的异常。

## java try catch finally 基本异常模型

```java
try {
	System.out.println("商=" + n.shang(1, -3));
} catch (ChushulingException yc) {
	System.out.println(yc.getMessage());
	yc.printStackTrace();
} catch (ChushufuException yx) {//出现错误的时候执行的语句
	System.out.println(yx.getMessage());
	yx.printStackTrace();
} catch (Exception y) {
	System.out.println(y.getMessage());
	y.printStackTrace();
}
finally {
	System.out.println("finally!");
} //// finally不管发没发生异常都会被执行
```

## finally 中如果有return 将会发生什么

程序将返回finally中的返回值，如果存在finally代码块，try中的return语句不会立马返回调用者，而是记录下返回值待finally代码块执行完毕之后再向调用者返回其值，然后如果在finally中修改了返回值，就会返回修改后的值。

