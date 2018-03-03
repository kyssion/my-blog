### JUnit4使用的基本注解

JUnit4基本注释，下表列出了这些注释的概括：

|  注解 | 描述  |
| ------------ | ------------ |
| @Test public void method()|  测试注释指示该公共无效方法它所附着可以作为一个测试用例。可以指定一个异常这个已成将会捕获测试会成功，还可以指定超时时间超过指定的运行时间价将会自动判断为超时 |
| @Before public void method()|  注释表示，该方法必须在类中的每个测试之前执行，以便执行测试某些必要的先决条件 |
|  @BeforeClass public static void method()|  BeforeClass注释指出这是附着在静态方法必须执行一次并在类的所有测试之前。发生这种情况时一般是测试计算共享配置方法(如连接到数据库) |
| @After public void method()| 注释指示，该方法在执行每项测试后执行(如执行每一个测试后重置某些变量，删除临时变量等)  |
| @AfterClass public static void method()|  当需要执行所有的测试在JUnit测试用例类后执行，AfterClass注解可以使用以清理建立方法，(从数据库如断开连接)。注意：附有此批注(类似于BeforeClass)的方法必须定义为静态 |
|@Ignore public static void method()| 当想暂时禁用特定的测试执行可以使用忽略注释。每个被注解为@Ignore的方法将不被执行  |

#### 一个例子

```java
import static org.junit.Assert.*;
import java.util.ArrayList;
import org.junit.*;
import a_baseForJava.a_junit4.main.ItemDemo;
public class ItemTest {
	ArrayList<String> testList;
	@BeforeClass
	public static void onceExecutedBeforeAll() {
		System.out.println("@BeforeClass: onceExecutedBeforeAll");
	}
	@Before
	public void executedBeforeEach() {
		testList = new ArrayList();
		System.out.println("@Before: executedBeforeEach");
	}
	@Test
	public void testSum() {
		ItemDemo sum = new ItemDemo();
		assertEquals(sum.sum(10, 12), 22);
	}
	@Test
	public void EmptyCollection() {
		assertTrue(testList.isEmpty());
		System.out.println("@Test: EmptyArrayList");
	}
	@Test
	public void OneItemCollection() {
		testList.add("oneItem");
		assertEquals(1, testList.size());
		System.out.println("@Test: OneItemArrayList");
	}
	@After
	public void executedAfterEach() {
		testList.clear();
		System.out.println("@After: executedAfterEach");
	}
	@AfterClass
	public static void onceExecutedAfterAll() {
		System.out.println("@AfterClass: onceExecutedAfterAll");
	}
	@Ignore
	public void executionIgnored() {
		System.out.println("@Ignore: This execution is ignored");
	}
}
```

#### 控制台输出的结结果

```java
@BeforeClass: onceExecutedBeforeAll
@Before: executedBeforeEach
@Test: testSum
@After: executedAfterEach
@Before: executedBeforeEach
@Test: EmptyArrayList
@After: executedAfterEach
@Before: executedBeforeEach
@Test: OneItemArrayList
@After: executedAfterEach
@AfterClass: onceExecutedAfterAll
```

> 总结：对于java的类来说所有BeforeClass 会在所有的测试调用前进行调用 AfterClass 将会在所有的测试使用完成后在进行调用 Before After 将会在所有的测试完成的时候进行调用

### junit断言

这些方法都受到 Assert 类扩展了java.lang.Object类并为它们提供编写测试，以便检测故障。下表中有一种最常用的断言方法的更详细的解释

| 断言  |  描述 |
| ------------ | ------------ |
|void assertEquals([String message], expected value, actual value)|断言两个值相等。值可能是类型有 int, short, long, byte, char or java.lang.Object. 第一个参数是一个可选的字符串消息|
|void assertTrue([String message], boolean condition)|断言一个条件为真|
|void assertFalse([String message],boolean condition)|断言一个条件为假|
|void assertNotNull([String message], java.lang.Object object)|断言一个对象不为空(null)|
|void assertNull([String message], java.lang.Object object)|断言一个对象为空(null)|
|void assertSame([String message], java.lang.Object expected, java.lang.Object actual)|断言，两个对象引用相同的对象|
|void assertNotSame([String message], java.lang.Object unexpected, java.lang.Object actual)|断言，两个对象不是引用同一个对象|
|void assertArrayEquals([String message], expectedArray, resultArray)|断言预期数组和结果数组相等。数组的类型可能是 int, long, short, char, byte or java.lang.Object.|


在以上类中我们可以看到，这些断言方法是可以工作的。

- assertEquals() 如果比较的两个对象是相等的，此方法将正常返回；否则失败显示在JUnit的窗口测试将中止。
- assertSame() 和 assertNotSame() 方法测试两个对象引用指向完全相同的对象。
- assertNull() 和 assertNotNull() 方法测试一个变量是否为空或不为空(null)。
- assertTrue() 和 assertFalse() 方法测试if条件或变量是true还是false。
- assertArrayEquals() 将比较两个数组，如果它们相等，则该方法将继续进行不会发出错误。否则失败将显示在JUnit窗口和中止测试。

#### JUnit4套件测试

测试套件是一些测试不同类用例，可以使用@RunWith和@Suite注解运行所有东西在一起。如果有很多测试类，想让它们都运行在同一时间，而不是单一地运行每个测试，这是非常有用的。

当一个类被注解为**@RunWith**， JUnit 将调用被在其中注解，以便运行测试类，而不使用内置的 JUnit 运行方法。

> 快速生成：包右键>>new>>JUnit test Suite>>finish

指定套件类

```java
import static org.junit.Assert.*;
import org.junit.runner.RunWith;
import org.junit.runners.Suite;
@RunWith(Suite.class)
@Suite.SuiteClasses(value= {TestOne.class,TestTwo.class})
public class ItemTest {
}
```

两个测试类

```java
import org.junit.Test;
public class TestOne {
	@Test
	public void Test() {
		System.out.println("this is my test 1");
	}
}
import org.junit.Test;
public class TestTwo {
	@Test
	public void Test() {
		System.out.println("this is my test 2");
	}
}
```

输出结果

```java
this is my test 1
this is my test 2
```

### java参数化自动测试

一个测试类也可以被看作是一个参数化测试类要满足下列所有要求：

- 该类被注解为 @RunWith(Parameterized.class).
- 如前一节中所说明的, @RunWith 注解让JUnit来调用其中的注释来运行测试类，代替使用内置的JUnit运行器，Parameterized 是一个在JUnit内的运行器将运行相同的测试用例组在不同的输入。
- 这个类有一个构造函数，存储测试数据。
- 这个类有一个静态方法生成并返回测试数据，并注明@Parameters注解。
- 这个类有一个测试，它需要注解@Test到方法。

> Junit底层通过多次生成新的类进行多次测试

```java
import static org.junit.Assert.*;
import java.util.Arrays;
import java.util.Collection;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import a_baseForJava.a_junit4.main.ItemDemo;
@RunWith(Parameterized.class)
public class ItemTest {
	private int expected;
	private int first;
	private int second;
	public ItemTest(int expectedResult, int firstNumber, int secondNumber) {
		this.expected = expectedResult;
		this.first = firstNumber;
		this.second = secondNumber;
	}
	@Parameters
	public static Collection addedNumbers() {
		return Arrays.asList(new Integer[][] { { 3, 1, 2 }, { 5, 2, 3 }, { 7, 3, 4 }, { 9, 4, 5 }, });
	}
	@Test
	public void sum() {
		ItemDemo add = new ItemDemo();
		System.out.println("Addition with parameters : " + first + " and " + second);
		assertEquals(expected, add.sum(first, second));
	}
}
```

测试结果

```java
Addition with parameters : 1 and 2
Addition with parameters : 2 and 3
Addition with parameters : 3 and 4
Addition with parameters : 4 and 5
```