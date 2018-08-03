## 泛型的使用

泛型有三种使用方式，分别为：泛型类、泛型接口、泛型方法


### 泛型类和泛型接口

泛型类的最基本写法

```java
class 类名称 <泛型标识：可以随便写任意标识号，标识指定的泛型的类型>{
    private 泛型标识 /*（成员变量类型）*/ var;
        .....
    }
}
```

一个最普通的泛型类：

```java
//此处T可以随便写为任意标识，常见的如T、E、K、V等形式的参数常用于表示泛型
//在实例化泛型类时，必须指定T的具体类型
public class Generic<T> {
    //key这个成员变量的类型为T,T的类型由外部指定  
    private T key;
    public Generic(T key) { //泛型构造方法形参key的类型也为T，T的类型由外部指定
        this.key = key;
    }
    public T getKey() { //泛型方法getKey的返回值类型为T，T的类型由外部指定
        return key;
    }
}
```

注意：范型类也可以传入范型实参，同样也会被类的定义所限制

```java
interface Sayfather {
    void say();
}
class SayImp implements Sayfather {
    public void say() {
        System.out.println("hello world");
    }
}
interface TestFather<T> {
    T say(T t);
}
//继承指派方法，前面范型声明必须满足后面的范型声明
class FatherTestImp<S extends Sayfather,T> implements TestFather<T> {
    public S say(S t) {
        t.say();
        return t;
    }
    public T say(T t) {
        return null;
    }
}
```

## 范型方法

泛型类，是在实例化类的时候指明泛型的具体类型；泛型方法，是在调用方法的时候指明泛型的具体类型 。

```java
/**
 * 泛型方法的基本介绍
 * @param tClass 传入的泛型实参
 * @return T 返回值为T类型
 * 说明：
 *  1）public 与 返回值中间<T>非常重要，可以理解为声明此方法为泛型方法。
 *  2）只有声明了<T>的方法才是泛型方法，泛型类中的使用了泛型的成员方法并不是泛型方法。
 *  3）<T>表明该方法将使用泛型类型T，此时才可以在方法中使用泛型类型T。
 *  4）与泛型类的定义一样，此处T可以随便写为任意标识，常见的如T、E、K、V等形式的参数常用于表示泛型。
 */
public <T> T genericMethod(Class<T> tClass)throws InstantiationException ,
        IllegalAccessException{
    T instance = tClass.newInstance();
    return instance;
}
```

注意：即使在范型类中指定范型标识和类中的范型方法使用的范型标识相同，类中的范型方法使用的范型标识也相当于一个新的标识

```java
class GenerateTest<T>{
    public void show_1(T t){
        System.out.println(t.toString());
    }
    //在泛型类中声明了一个泛型方法，使用泛型E，这种泛型E可以为任意类型。可以类型与T相同，也可以不同。
    //由于泛型方法在声明的时候会声明泛型<E>，因此即使在泛型类中并未声明泛型，编译器也能够正确识别泛型方法中识别的泛型。
    public <E> void show_3(E t){
        System.out.println(t.toString());
    }
    //在泛型类中声明了一个泛型方法，使用泛型T，注意这个T是一种全新的类型，可以与泛型类中声明的T不是同一种类型。
    public <T> void show_2(T t){
        System.out.println(t.toString());
    }
}
```

注意：静态方法只能声明为范型函数，否则不可以带有范型

```java
public class StaticGenerator<T> {
    ....
    ....
    /**
     * 如果在类中定义使用泛型的静态方法，需要添加额外的泛型声明（将这个方法定义成泛型方法）
     * 即使静态方法要使用泛型类中已经声明过的泛型也不可以。
     * 如：public static void show(T t){..},此时编译器会提示错误信息：
          "StaticGenerator cannot be refrenced from static context"
     */
    public static <T> void show(T t){
    }
}
```

## 泛型上下边界和通配符

java 使用extends 和 super 分别表示 范型声明时的只能是extends及其子类，和使用时必须是super及其父类的限制

```java
class Other{
	//?通配符表示一般的匹配相关的有嗯来约束一类的类型
	class Rong<T>{}
	class One{}
	class Two extends One{}
	class Three extends Two{}
	public void methodone() {
		Rong<? extends Two> rong = new Rong<Three>();
		//Rong<? extends Two> rong2 = new Rong<One>();//报错了因为不满足上界
		Rong<? super Two> rong3 = new Rong<One>();
		//---注意--- 集合类型的通配符模式下 	extends只能取不能存取得是extends后面的类型  
		//								surper 只能存变量强制转化成Object类型不能取
		List<? extends Two> list=new ArrayList<>();
		One one= list.get(0);
		Two two = list.get(0);//之所以只能取是因为强制转换的问题
		//list.set(0, new Three());//报错
		List<? super Two> list2 = new ArrayList<>();
		list2.add(new Three());//适因为内部一定知道相关 术语上转型
		One two1= (Two) list2.get(0);
	}
}
```
上面的例子中使用了通配符

在java 的范型中通配符解决了范型多版本不兼容的问题

比如Generic<Integer>不能被看作为`Generic<Number>的子类。所以同一种泛型可以对应多个版本（因为参数类型是不确定的），不同版本的泛型类实例是不兼容的。

因此我们需要一个在逻辑上可以表示同时是Generic<Integer>和Generic<Number>父类的引用类型。由此类型通配符应运而生。

例子如下

```java

public void showKeyValue1(Generic<Number> obj){
    Log.d("泛型测试","key value is " + obj.getKey());
}

Generic<Integer> gInteger = new Generic<Integer>(123);
Generic<Number> gNumber = new Generic<Number>(456);

showKeyValue(gNumber);
//此处在调用的时候限制了类型所以无法使用

// showKeyValue这个方法编译器会为我们报错：Generic<java.lang.Integer> 
// cannot be applied to Generic<java.lang.Number>
// showKeyValue(gInteger);
```

将程序改成这样既可以通过

```java
public void showKeyValue1(Generic<?> obj){
    Log.d("泛型测试","key value is " + obj.getKey());
}
```

类型通配符一般是使用？代替具体的类型实参，注意了，此处’？’是类型实参，而不是类型形参 ，可以把？看成所有类型的父类。是一种真实的类型。



## 范型数组（范型的限制）

关于泛型数组要提一下
看到了很多文章中都会提起泛型数组，经过查看sun的说明文档，在java中是”不能创建一个确切的泛型类型的数组”的。

也就是说下面的这个例子是不可以的：
```java
List<String>[] ls = new ArrayList<String>[10];  
```
而使用通配符创建泛型数组是可以的，如下面这个例子：
```java
List<?>[] ls = new ArrayList<?>[10];  
```
这样也是可以的：
```java
List<String>[] ls = new ArrayList[10];
```
下面使用Sun的一篇文档的一个例子来说明这个问题：

```java
List<String>[] lsa = new List<String>[10]; // Not really allowed.    
Object o = lsa;    
Object[] oa = (Object[]) o;    
List<Integer> li = new ArrayList<Integer>();    
li.add(new Integer(3));    
oa[1] = li; // Unsound, but passes run time store check    
String s = lsa[1].get(0); // Run-time error: ClassCastException.
```

其实说白了就是java在实现范型的时候使用了擦除的方法，所以在上面代码的最后一行将会出现string = object 这种类型不匹配的情况


下面采用通配符的方式是被允许的:数组的类型不可以是类型变量，除非是采用通配符的方式，因为对于通配符的方式，最后取出数据是要做显式的类型转换的。

```java
List<?>[] lsa = new List<?>[10]; // OK, array of unbounded wildcard type.    
Object o = lsa;    
Object[] oa = (Object[]) o;    
List<Integer> li = new ArrayList<Integer>();    
li.add(new Integer(3));    
oa[1] = li; // Correct.    
Integer i = (Integer) lsa[1].get(0); // OK 
```