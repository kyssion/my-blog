## 传统的资源关闭方式
为了确保外部资源一定要被关闭，通常关闭代码被写入finally代码块中，当然我们还必须注意到关闭资源时可能抛出的异常，于是变有了下面的经典代码：

```java
public static void main(String[] args) {
    FileInputStream inputStream = null;
    try {
        inputStream = new FileInputStream(new File("test"));
        System.out.println(inputStream.read());
    } catch (IOException e) {
        throw new RuntimeException(e.getMessage(), e);
    } finally {
        if (inputStream != null) {
            try {
                inputStream.close();
            } catch (IOException e) {
                throw new RuntimeException(e.getMessage(), e);
            }
        }
    }
}
```

这种方法提供统一的入口将相关的资源关闭功能如c++的析构函数等，不符合面向对象编程的方法

## JDK7及其之后的资源关闭方式

> try-with-resource语法

确实，在JDK7以前，Java没有自动关闭外部资源的语法特性，直到JDK7中新增了try-with-resource语法，才实现了这一功能,就是当一个外部资源的句柄对象（比如FileInputStream对象）实现了AutoCloseable接口，那么就可以将上面的板式代码简化为如下形式：

```java
public static void main(String[] args) {
	try (FileInputStream inputStream = new FileInputStream(new File("test"))) {
		System.out.println(inputStream.read());
	} catch (IOException e) {
		throw new RuntimeException(e.getMessage(), e);
	}
}
```

将外部资源的句柄对象的创建放在try关键字后面的括号中，当这个try-catch代码块执行完毕后，Java会确保外部资源的close方法被调用。代码是不是瞬间简洁许多！

## 实现原理

try-with-resource并不是JVM虚拟机的新增功能，只是JDK实现了一个语法糖，当你将上面代码反编译后会发现，其实对JVM虚拟机而言，它看到的依然是之前的写法：

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

> 引申: 异常抑制

通过反编译的代码，大家可能注意到代码中有一处对异常的特殊处理：

```java
var2.addSuppressed(var11);
```

这是try-with-resource语法涉及的另外一个知识点，叫做异常抑制。当对外部资源进行处理（例如读或写）时，如果遭遇了异常，且在随后的关闭外部资源过程中，又遭遇了异常，那么你catch到的将会是对外部资源进行处理时遭遇的异常，关闭资源时遭遇的异常将被“抑制”但不是丢弃，通过异常的getSuppressed方法，可以提取出被抑制的异常。

## 总结

1. 当一个外部资源的句柄对象实现了AutoCloseable接口，JDK7中便可以利用try-with-resource语法更优雅的关闭资源，消除板式代码。

2. try-with-resource时，如果对外部资源的处理和对外部资源的关闭均遭遇了异常，“关闭异常”将被抑制，“处理异常”将被抛出，但“关闭异常”并没有丢失，而是存放在“处理异常”的被抑制的异常列表中。