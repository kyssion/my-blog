> 最用在企业中进行实习使用了junit4进行单元测试这里进行一下相关的知识点的总结

### JUnit是什么

JUnit是用于编写和运行可重复的自动化测试的开源测试框架， 这样可以保证我们的代码按预期工作。JUnit可广泛用于工业和作为支架(从命令行)或IDE(如Eclipse)内单独的Java程序。

#### JUnit的提供

- 断言测试预期结果。
- 测试功能共享通用的测试数据。
- 测试套件轻松地组织和运行测试。
- 图形和文本测试运行。

#### JUnit用于测试

- 整个对象
- 对象的一部分 – 交互的方法或一些方法
- 几个对象之间的互动(交互)

#### JUnit的特点

- JUnit是用于编写和运行测试的开源框架。
- 提供了注释，以确定测试方法。
- 提供断言测试预期结果。
- 提供了测试运行的运行测试。
- JUnit测试让您可以更快地编写代码，提高质量
- JUnit是优雅简洁。它是不那么复杂以及不需要花费太多的时间。
- JUnit测试可以自动运行，检查自己的结果，并提供即时反馈。没有必要通过测试结果报告来手动梳理。
- JUnit测试可以组织成测试套件包含测试案例，甚至其他测试套件。
- Junit显示测试进度的，如果测试是没有问题条形是绿色的，测试失败则会变成红色。

#### junit4简单例子

1. 新建一个测试类

```java
public class ItemDemo {
	public int sum(int a,int b) {
		return a+b;
	}
}
```

2. 创建一个测试类

> 过程：指定一个测试用的工具包右键>>new>>other>>搜索junit>>选择 Junit Test Case

![](blogimg/junit/1.png)

![](blogimg/junit/2.png)

创建后的类

```java
import static org.junit.Assert.*;
import org.junit.Test;
import a_baseForJava.a_junit4.main.ItemDemo;
public class ItemTest { <span> </span>@Test <span> </span>public void testSum() { <span> </span>ItemDemo sum = new ItemDemo(); <span> </span>assertEquals(sum.sum(10,12), 22); <span> </span>}
}
```

3. 进行测试

> 右键>>run as Test

![](blogimg/junit/3.png)




