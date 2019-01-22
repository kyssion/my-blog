首先我们先聊一聊java的lamble表达式

这里给出一个简单的例子

```java
public class JavaLamble {
    public Function function = null;
    public void run(Function function){
        this.function=function;
    }
    public static void main(String[] args) {
        JavaLamble javaLamble = new JavaLamble();
        javaLamble.run(write ->{
            System.out.println(""+write);
        });
        javaLamble.function.showWrite("item");
    }
}
interface Function{
    void showWrite(String write);
}
```

> 注意:lamble的new的对象必须为接口，并且接口中必须只有一个函数,但是可以有默认实现函数,比如下面这样

```java
interface Function{
    void showWrite(String write);
    default void Strr(String a,String b){
        System.out.println("sf");
    }
}
```

### java中lamble表达式的写法

1. 最基本写法(只有一个参数和一行代码的时候)

lamble接口类

```java
interface Function{
    void showWrite(String write);
}
interface Function2(){
    void shwoWrite2();
}
```

使用样例

```java
Function f1 = write -> System.out.println(write);
//其实lamble就是下面这种基本写法的简化版
Function f11 = new Function() {
    @Override
    public void showWrite(String write) {   
        System.out.println(write);     
    }
}

Function2 f2 = ()->System.out.println("hello world");
//其实lamble就是下面这种基本写法的简化版
Function f22 = new Function() {
    @Override
    public void showWrite() {
        System.out.println("hello world");  
    }
}
```

2. lamble的其他形式

```java
Function f1 = ()->{//多行代码解释
    String a= " !";
    System.out.println("hello world"+a);
}
Function f1 = (write)->{//java 编译器会自动的识别write的类型
    System.out.println(write);
}
Function f1 = (String write) -> {//指定参数
     System.out.println(write);
}
Function f1 = (write,one)->{//多参数
    System.out.println(write);
}
Function f1 = (String write,Integer one) -> {//多参数
     System.out.println(write);
}
```

### lamble 表达式常用的一些接口

  ![](/blogimg/java/stream_lamble/3.png)

### lamble表达式的作用域

lamble表达式将会使用作用域的引用,比如下面的例子

```java
public class JavaLamble {
    public Function function = null;
    public void run(Function function){
        this.function=function;
    }
    public static void main(String[] args) {
        final String item = "hello world";//注意内部引用的各种变量必须为final 不可修改的变量否则会报错
        JavaLamble javaLamble = new JavaLamble();
        javaLamble.run((write) ->{
            System.out.println(""+item);
        });
        javaLamble.function.showWrite("item");
    }
}
interface Function{
    void showWrite(String write);
}

```
java的实际输出结果是 item对应的值

> 注意在使用lamble表达式的时候,传入给内部的变量必须是不可变化的变量(使用final修饰符)

### lamble 其他需要注意的地方

1. 当右侧具有返回值的时候

一个lamble接口:

```java
interface  FunctionReturn{
    boolean returnItem(int a);
}
FunctionReturn functionReturn = (number)->number>10;
FunctionReturn functionReturn = (number)->{
    return number>10;
}
```

> 当lamble表达式具有返回值的时候,应保证右侧的表达式或者代码快能返回函数中定义的变量

2. 但使用范型的时候

```java
interface  FunctionReturnF<T,R>{
    R getReturn(T t);
}
FunctionReturnF functionReturnF = (kkk)->{
    return new Object();
};
FunctionReturnF<String,Integer> functionReturnF1= (kkk)->Integer.valueOf(kkk);
```

> 注意当使用的是范型的时候,要注意lamble表达式的各种属性应该满足范型定义的各种类型(声明时T,R的类型)

3. 注意三，使用lamble可能有函数签名不一致的问题

> 这个问题的本质是应为lamble表达式只是关心接口中函数的形式而这个函数所在的接口其实lamble并不关心
> 在java内部的虚拟机实现这个方法的时候本质上是寻找有没有一个接口能够读应这个表达式,从而通过这种方法找到对应的接口

例子：

```java
//两个lamble接口
interface IntPred{
    boolean Test(Integer integer);
}
interface IntPred2{
    boolean Test2(Integer integer);
}

//一个可以运行的测试类
public class JavaLamble {
    boolean check(IntPred2 predicate){
        return predicate.Test2(123);
    }
    boolean check2(IntPred intPred){
        return intPred.Test(123);
    }
    //这个函数的声明并没有错误但是会导致lamble表达式不知道对应哪一个函数
    boolean check(IntPred intPred){
        return intPred.Test(123);
    }
    public static void main(String[] args) {
        JavaLamble javaLamble = new JavaLamble();
        //这里会报错，应为java底层在通过check方法中的表达式可以找到两个多态的方法java 不知到匹配哪一个
        javaLamble.check((x)->x>10);//通过这个可以看到lamble表达式隐藏了接口的类名,本质上是通过这个函数去对应的接口
        javaLamble.check2((x)->x>10);
    }
}
```

不过由于这种重载导致的问题可以使用强制转换解决,如果参数的数量相同但是类型不同，可以使用有类型的lamble表达式

```java
javaLamble.check((IntPred2)(x)->x>10);
```

总结:

Lambda 表达式作为参数时， 其类型由它的目标类型推导得出， 推导过程遵循
如下规则：
- 如果只有一个可能的目标类型， 由相应函数接口里的参数类型推导得出；
- 如果有多个可能的目标类型， 由最具体的类型推导得出；
- 如果有多个可能的目标类型且最具体的类型不明确， 则需人为指定类型。

ps ： 最后一点java中没有null这个对象