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

> 注意:lamble的new的对象必须为接口，并且接口中必须只有一个函数

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

