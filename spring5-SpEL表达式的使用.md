### SpEL 表达式的使用

SpEl 表达式主要用在bean的定义是上

基于xml的配置

```xml
<bean id="numberGuess" class="org.spring.samples.NumberGuess">
    <property name="randomNumber" value="#{ T(java.lang.Math).random() * 100.0 }"/>
    <!-- other properties -->
</bean>
```

基于注解的配置

```java
public static class FieldValueTestBean
    @Value("#{ systemProperties['user.region'] }")
    private String defaultLocale;
    @Value("#{ systemProperties['user.region'] }")
    public void setDefaultLocale(String defaultLocale) {
        this.defaultLocale = defaultLocale;
    }
    public String getDefaultLocale() {
        return this.defaultLocale;
    }
}
```

基于注解的配置在使用自动装配的方法和构造函数时使用@Value注解配套方法

```java
public class SimpleMovieLister {
    private MovieFinder movieFinder;
    private String defaultLocale;
    @Autowired
    public void configure(MovieFinder movieFinder,
            @Value("#{ systemProperties['user.region'] }") String defaultLocale) {
        this.movieFinder = movieFinder;
        this.defaultLocale = defaultLocale;
    }
}
```
### 语言参考

spring 内置了一个解析器SpelExpressionParser

#### 基本类型表达式
```java
ExpressionParser parser = new SpelExpressionParser();
// evals to "Hello World"
String helloWorld = (String) parser.parseExpression("'Hello World'").getValue();
double avogadrosNumber = (Double) parser.parseExpression("6.0221415E+23").getValue();
// evals to 2147483647
int maxValue = (Integer) parser.parseExpression("0x7FFFFFFF").getValue();
boolean trueValue = (Boolean) parser.parseExpression("true").getValue();
Object nullValue = parser.parseExpression("null").getValue();
```

#### 获取对象的属性

```java
int year = (Integer) parser.parseExpression("Birthdate.Year + 1900").getValue(context);
String city = (String) parser.parseExpression("placeOfBirth.City").getValue(context);
parser.parseExpression("Officers['advisors'][0].PlaceOfBirth.Country").setValue(
        societyContext, "Croatia");
```

#### 获取数组的属性

```java
String invention = parser.parseExpression("Members[0].Inventions[6]").getValue(
        societyContext, String.class);

//创造一个内链表

List listOfLists = (List) parser.parseExpression("{{'a','b'},{'x','y'}}").getValue(context);

//创建数组

int[][] numbers3 = (int[][]) parser.parseExpression("new int[4][5]").getValue(context);
```

#### 内联map

```java
// evaluates to a Java map containing the two entries
Map inventorInfo = (Map) parser.parseExpression("{name:'Nikola',dob:'10-July-1856'}").getValue(context);
Map mapOfMaps = (Map) parser.parseExpression("{name:{first:'Nikola',last:'Tesla'},dob:{day:10,month:'July',year:1856}}").getValue(context);
```

#### 调用方法
```java
boolean isMember = parser.parseExpression("isMember('Mihajlo Pupin')").getValue(
        societyContext, Boolean.class);
```
#### 运算符解析

```java
boolean trueValue = parser.parseExpression("'black' < 'block'").getValue(Boolean.class);

boolean falseValue = parser.parseExpression(
        "'xyz' instanceof T(Integer)").getValue(Boolean.class);

//正则支持
// evaluates to true
boolean trueValue = parser.parseExpression(
        "'5.00' matches '\^-?\\d+(\\.\\d{2})?$'").getValue(Boolean.class);

//evaluates to false
boolean falseValue = parser.parseExpression(
        "'5.0067' matches '\^-?\\d+(\\.\\d{2})?$'").getValue(Boolean.class);
```

> 注意null 在这里视为0 和 空  1> null 返回true -1>null 返回false

> 注意:每个符号运算符也可以被指定为纯粹的字母等效。这避免了所使用的符号对嵌入表达式的文档类型（例如XML文档）具有特殊含义的问题。文本等价物如下所示：lt（<），gt（>），le（⇐），ge（>=），eq（==）， ne（!=），div（/），mod（%），not（!）

#### 逻辑运算符

```java
// -- AND --
// evaluates to false
boolean falseValue = parser.parseExpression("true and false").getValue(Boolean.class);
// evaluates to true
String expression = "isMember('Nikola Tesla') and isMember('Mihajlo Pupin')";
boolean trueValue = parser.parseExpression(expression).getValue(societyContext, Boolean.class);
// -- OR --
// evaluates to true
boolean trueValue = parser.parseExpression("true or false").getValue(Boolean.class);
// evaluates to true
String expression = "isMember('Nikola Tesla') or isMember('Albert Einstein')";
boolean trueValue = parser.parseExpression(expression).getValue(societyContext, Boolean.class);
// -- NOT --
// evaluates to false
boolean falseValue = parser.parseExpression("!true").getValue(Boolean.class);
// -- AND and NOT --
String expression = "isMember('Nikola Tesla') and !isMember('Mihajlo Pupin')";
boolean falseValue = parser.parseExpression(expression).getValue(societyContext, Boolean.class);
```

#### 数学运算符

```java
// Addition
int two = parser.parseExpression("1 + 1").getValue(Integer.class); // 2

String testString = parser.parseExpression(
        "'test' + ' ' + 'string'").getValue(String.class); // 'test string'

// Subtraction
int four = parser.parseExpression("1 - -3").getValue(Integer.class); // 4
double d = parser.parseExpression("1000.00 - 1e4").getValue(Double.class); // -9000
// Multiplication
int six = parser.parseExpression("-2 * -3").getValue(Integer.class); // 6
double twentyFour = parser.parseExpression("2.0 * 3e0 * 4").getValue(Double.class); // 24.0
// Division
int minusTwo = parser.parseExpression("6 / -3").getValue(Integer.class); // -2
double one = parser.parseExpression("8.0 / 4e0 / 2").getValue(Double.class); // 1.0
// Modulus
int three = parser.parseExpression("7 % 4").getValue(Integer.class); // 3
int one = parser.parseExpression("8 / 5 % 2").getValue(Integer.class); // 1
// Operator precedence
int minusTwentyOne = parser.parseExpression("1+2-3*8").getValue(Integer.class); // -21
```
#### 属性赋值

```java
String aleks = parser.parseExpression(
        "Name = 'Alexandar Seovic'").getValue(inventorContext, String.class);
```

#### 构造函数

```java
Inventor einstein = p.parseExpression(
        "new org.spring.samples.spel.inventor.Inventor('Albert Einstein', 'German')")
        .getValue(Inventor.class);
```

#### 三元运算符和猫王运算符

```java
String falseString = parser.parseExpression(
        "false ? 'trueExp' : 'falseExp'").getValue(String.class);

String name = parser.parseExpression("name?:'Unknown'").getValue(String.class);
//上面等价于

String name = parser.parseExpression("name==null?name:'Unknown'").getValue(String.class);
```

#### 集合选择

```java
List<Inventor> list = (List<Inventor>) parser.parseExpression(
        "Members.?[Nationality == 'Serbian']").getValue(societyContext);
Map newMap = parser.parseExpression("map.?[value<27]").getValue();

```

着表达式将会选择 List Menbers中 Nationality 为 Serbian的所有元素

> 引申:除了返回所有选定的元素之外，还可以检索第一个或最后一个值。要获得与选择相匹配的第一个条目，语法使用^[…​],要获取语法的最后匹配使用$[…​]。


#### 在字符串中嵌入表达式模版

```java
String randomPhrase = parser.parseExpression(
        "random number is #{T(java.lang.Math).random()}",
        new TemplateParserContext()).getValue(String.class);
```