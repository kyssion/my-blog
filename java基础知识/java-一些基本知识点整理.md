> 学习java一定的时间了，这里一些知识点的整理

## 变量必须是字母,下划线或者$符开头不能是 java 关键字变量命名规范 驼峰写法,类首字母大写驼峰写法
```java
int $a = 123;
int _b = 123;
```
## 基本数据类型 
```java
//变量的形成分为两个步骤声明和初始化
变量只是一个声明的存储单元而已
int aa, bbb, ccc;
//
1.byte 1字节 short
2字节 int 4字节 long
8字节 float
double boolean char
Integer.toBinaryString($a);// 转化为二进制字符串
long c = 1234L;// 显示声明长整型
// 进转化问题
int d = 0123;// 使用 8进制
d = 0x1234;// 使用16进制
d = 0b1000_0000;//
j7新特心直接进行
二进制编写
```
## java 运算符
**赋值运算符** : =
**关系运算符** : > , < , >= , <= , == , != , instanceof
**逻辑运算符** : && , || , ! 
**位运算符** : & , | , ^异或 , ~非 , >> , << , >>>
**条件运算符**: ? : 
**扩展赋值运算符** : += , -= , *= , /=

# 流程控制语句
```java
if (true) {
 
} else if (true) {
 
} else {
 
}
while (true) {
break;
}
// 先运行在判断---这个方法相当于给代码块进行命名而已
hhe: do {
break hhe;
// continue hhe;//表示跳出一定的循环结构
} while (true);
// jdk7 增强型switch控制语句 可用int 枚举类型和字符串
String string = "sdf";//如果不添加break switch会将之后所有的对象都当成自己代码快中的东西会忽略case 一直执行下去
switch (string) {
case "ggg":
System.out.println("One.main()");
break;
default:
break;
}
while (true) {
break;
}
```
## 基础方法 scanner
```java
@SuppressWarnings("resource")
Scanner scanner = new Scanner(System.in);// 传入一个输入流
// 引申可以从字符串（Readable）、输入流、文件等等来直接构建Scanner对象，有了Scanner了，
// 就可以逐段（根据正则分隔式）来扫描整个文本，并对扫描后的结果做想要的处理。
String line = scanner.nextLine(); // 获得控制台输入的下一行
scanner.useDelimiter("|,|\\."); //以指定的字符记性分割字符串
scanner.delimiter(); //返回此 Scanner 当前正在用于匹配分隔符的 Pattern。
scanner.hasNext() ; //判断扫描器中当前扫描位置后是否还存在下一段。（原APIDoc的注释很扯淡）
scanner.hasNextLine(); //如果在此扫描器的输入中存在另一行，则返回 true。
scanner.next(); //查找并返回来自此扫描器的下一个完整标记。
scanner.nextLine(); //此扫描器执行当前行，并返回跳过的输入信息。
//java 比较运算符 -- 只能用来比较有继承关系的类
Integer bb=12;
//这个是对象比较符
if (bb instanceof Integer) {
}
//使用类名称比较符
Integer.class.isInstance(bb);
```

## 枚举类型 简单枚举类型
```java
public enum Color {
RED, GREEN, BLANK, YELLOW
}
// 可以在内部声明方法
public enum Light {
// 利用构造函数传参---枚举类型中每一个参数就相当于一个枚举类型
RED(1), GREEN(3), YELLOW(2);
// 定义私有变量
private int nCode;
// 构造函数，枚举类型只能为私有
private Light(int _nCode) {
this.nCode = _nCode;
}
@Override
public String toString() {
return String.valueOf(this.nCode);
}
}
```

## Java包注释
```java
@author 作者
@version 版本
@param 参数
@return 返回值
@throws 异常
@deprecated 废弃
```
