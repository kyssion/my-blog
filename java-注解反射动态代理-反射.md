## 反射的定义

在运行状态中，对于任意一个类，都能够知道这个类的所有属性和方法；对于任意一个对象，都能够调用它的任意一个方法和属性；这种动态获取的信息以及动态调用对象的方法的功能称为反射。

在java中反射是基于class信息的

> 关于Class

1. Class是一个类，一个描述类的类（也就是描述类本身），封装了描述方法的Method，描述字段的Filed，描述构造器的Constructor等属性

2. 对象照镜子后（反射）可以得到的信息：某个类的数据成员名、方法和构造器、某个类到底实现了哪些接口。

3. 对于每个类而言，JRE 都为其保留一个不变的 Class 类型的对象。一个 Class 对象包含了特定某个类的有关信息。

4. Class 对象只能由系统建立对象

5. 一个类在 JVM 中只会有一个Class实例

## java 通过编程方法应用反射特性

### 1. 获取类的方法

```java
//使用对象获取Class
Class<?> itemClass = new String().getClass();
//直接使用类名.class获取
Class<?> itemClass2 = String.class;
//使用类的完整路径获取
Class<?> itemClass3 = Class.forName("java.lang.String");
//获取父类
Class<?> fatherClass = itemClass.getSuperClass();
```

### 2. 使用class创建类

> 使用newInstance生成对象

```java
String string= (String) itemClass.newInstance();
```

> 使用构造方法生成对象

```java
Constructor<?> constructor = itemClass.getConstructor(Integer.class,String.class);
//返回这个class所含有的所有方法--不包括继承的方法--只能使用自己定义的构造方法
Constructor<?>[] constructors = itemClass.getConstructors();
constructor.newInstance(12,"sf");
```

### 使用反射获取类加载器

```java
//1、获取一个系统的类加载器
ClassLoader classLoader = ClassLoader.getSystemClassLoader();
System.out.println("系统的类加载器-->" + classLoader);

//2、获取系统类加载器的父类加载器(扩展类加载器（extensions classLoader）)
classLoader = classLoader.getParent();
System.out.println("扩展类加载器-->" + classLoader);

//3、获取扩展类加载器的父类加载器
//输出为Null,无法被Java程序直接引用
classLoader = classLoader.getParent();
System.out.println("启动类加载器-->" + classLoader);

//4、测试当前类由哪个类加载器进行加载 ,结果就是系统的类加载器
classLoader = Class.forName("com.kys.test.InvokeTest").getClassLoader();
System.out.println("当前类由哪个类加载器进行加载-->"+classLoader);

//5、测试JDK提供的Object类由哪个类加载器负责加载的
classLoader = Class.forName("java.lang.Object").getClassLoader();
System.out.println("JDK提供的Object类由哪个类加载器加载-->" + classLoader);
```

```java
#输出
系统的类加载器-->sun.misc.Launcher$AppClassLoader@18b4aac2
扩展类加载器-->sun.misc.Launcher$ExtClassLoader@61bbe9ba
启动类加载器-->null
当前类由哪个类加载器进行加载-->sun.misc.Launcher$AppClassLoader@18b4aac2
JDK提供的Object类由哪个类加载器加载-->null
```

### 引申使用class 类获取资源

```java
// /(左划线)表示使用classpath根目录进行下过关属性的查找
TestRelativePath.class.getResource(“/test.txt”).getFile()
Thread.currentThread().getContextClassLoader().getResource(“test.txt”).getFile()
```

### method 获取类中的方法

```java
//返回名称为xx参数为后面的变长数组的 直接成员方法
Method method = class1.getDeclaredMethod("xx", Integer.class);
//方法处理继承的方法
Method method2 = class1.getMethod("x", Integer.class);
```

### Field字段

```java
//--成员变量
Field field =class1.getDeclaredField("xixi");//返回变量名称为 field 的直接成员变量名称
Field field2= class1.getField("xxixi");//返回变量名称包括父元素的成员变量
//f ye e d
Field[] fields=class1.getDeclaredFields();//返回所有直接的成员变量
Field[] fields2 = class1.getFields();//返回所有的成员变量 包括父类进行继承的变量
```

### 注解使用

所有继承和实现了AnnotatedElement接口的类都具有返回对应的接口信息的方法，比如class method feild constructor

```java
Annotation annotation = xxx.getAnnotation(hehehe.class);//返回当前类中是否存在出传入的注解 有的时候将会进行返回相应的注解
//class1.isAnnotationPresent(Ceshi2.class);//判断是否存在一个注解
Annotation[] annotations = xxx.getAnnotations();//返回类中所有的注解包括继承的
Annotation[] annotations2= xxx.getDeclaredAnnotations();//f返回类中直接继承的元素
```

### 特殊的enclose* 方法

```java
package com.kys.test;
import java.lang.annotation.Annotation;
import java.lang.reflect.AnnotatedElement;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;

public class Outer {
    public Outer() {
        // 构造方法中的匿名内部类
        InnerClass innerClass = new InnerClass() {
            @Override
            public void fun() {
                getEnclosing(this.getClass());
            }
        };
        innerClass.fun();
    }
    // 匿名内部类
    static InnerClass innerClass = new InnerClass() {
        public void fun() {
            getEnclosing(this.getClass());
            /**
             * enclosingClass=class reflect.Outer
             * enclosingConstructor=null
             * enclosingMethod=null
             */
        }
    };

    public static void test() {
        // 方法中的匿名内部类
        InnerClass innerClass = new InnerClass() {
            @Override
            public void fun() {
                getEnclosing(this.getClass());
                /**
                 * enclosingClass=class reflect.Outer
                 * enclosingConstructor=null
                 * enclosingMethod=public static void reflect.Outer.test()
                 */
            }
        };
        innerClass.fun();
    }
    // 内部类
    public static class InnerClass {
        public InnerClass() {}
        public void fun() {}
    }

    public static void main(String[] args) {
        System.out.println("------内部类------");
        getEnclosing(InnerClass.class);

        System.out.println("------匿名内部类------");
        innerClass.fun();

        System.out.println("------方法中的匿名内部类------");
        Outer.test();

        System.out.println("------构造函数中的匿名内部类------");
        new Outer();
    }

    /**
     * getEnclosingClass:该类是在那个类中定义的， 比如直接定义的内部类或匿名内部类
     * getEnclosingConstructor：该类是在哪个构造函数中定义的，比如构造方法中定义的匿名内部类
     * getEnclosingMethod：该类是在哪个方法中定义的，比如方法中定义的匿名内部类
     *
     * @param cls
     */
    private static void getEnclosing(Class cls) {
        Class enclosingClass = cls.getEnclosingClass();
        Constructor enclosingConstructor = cls.getEnclosingConstructor();
        Method enclosingMethod = cls.getEnclosingMethod();
        System.out.println("enclosingClass=" + enclosingClass);
        System.out.println("enclosingConstructor=" + enclosingConstructor);
        System.out.println("enclosingMethod=" + enclosingMethod);
    }
}
```

这个方法是针对内部类的，如果这个class是一个内部类通过这个方法可以得出这个内部类对应的声明位置

