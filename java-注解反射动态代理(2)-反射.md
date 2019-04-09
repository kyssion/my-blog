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

### 2. 使用class类

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

> 其他用法

```java
//--返回成员枚举类型 如果不是枚举类型返回 null
class1.getEnumConstants();
//---class 类强制转化方法
class1.asSubclass(class2);//将class1转化成class2
class1.cast(i);// 讲 i强制转化成 class1所表示的实现类
//获得classloader
ClassLoader acClassLoader = class1.getClassLoader();
Class<?>[] classes=class2.getInterfaces();//获得接口数组
String string = class1.getName();//返回类名称
Package string2 =class1.getPackage();//返回变量的包类
URL rUrl = class1.getResource("xx");//返回给定名称所属的资源
InputStream string3 = class1.getResourceAsStream("xxx");//将给定的资源变成输入流
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
Annotation[][] annotations = method.getParameterAnnotations();//返回一个注解的二维数组 --同上面
Annotation[] annotations2=method.getAnnotations();
Class<?>[] class3 = method.getParameterTypes();//返回参数数组
Class<?> class4 = method.getReturnType();//返回返回值数组
int count=method.getParameterCount();//返回参数的数量
Parameter[] parameters=method.getParameters();//返回参数列表
class c = method.getDeclaringClass();//返回这个方法对应的class类
parameters[0].getName();
parameters[0].getType();//返回类型的class数组
//参数类型没有注入 参数
method.invoke(new ThisisCeshe(), null);//类似 FIeld的get方法--调用指定的实例的一个此method指定的方法
```

### Field字段

field 相关方法

```java
//--成员变量
Field field =class1.getDeclaredField("xixi");//返回变量名称为 field 的直接成员变量名称
Field field2= class1.getField("xxixi");//返回变量名称包括父元素的成员变量
//f ye e d
Field[] fields=class1.getDeclaredFields();//返回所有直接的成员变量
Field[] fields2 = class1.getFields();//返回所有的成员变量 包括父类进行继承的变量
field.get(new ThisisCeshe());//返回object 传入一个得出field对象的class的实例才能对其使用 取出实例中的对应的field对象 --存在基本类型的那一坨方法
field.getType();//返回一个class 对象表明这个字段的类型
field.getName();//返回这个字段的名字
field.set(new Integer(12), 123);//在前一个对象中 加入 后一个变量到field指定的变量上 --存在基本类型的那一坨方法
int a=field.getModifiers();//返回参数类型--public或者其他
```

### Annotated字段

所有继承和实现了AnnotatedElement接口的类都具有返回对应的接口信息的方法，比如class method feild constructor

> 注意下面的代码 *** 表示全部的反射都支持，特殊情况使用||分割

```java
Target Target = ***.getAnnotation(Target.class);//返回当前类中是否存在传入的注解 有的时候将会进行返回相应的注解
***.isAnnotationPresent(Ceshi2.class);//判断是否存在一个注解
Annotation[] annotations = ***.getAnnotations();//返回类中所有的注解包括继承的
Annotation[] annotations2= ***.getDeclaredAnnotations();//f返回类中直接继承的元素
```

注解的用法

```java

Annotation[][] annotation = constructor.getParameterAnnotations();
//所使用类型判断 强制转换
if(annotation[0][0] instanceof Target){
    Target targets= (Target) annotation[0][0];
}

//直接获取直接使用
Target annotation = ***.getAnnotation(Target.class);
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

### array 范型

```java
//创建一个第二个参数是边长参数的组 第一个参数是指定类型的数组
Array[][] arrays=(Array[][]) Array.newInstance(Integer.class, 100,100);
Array.get(arrays, 0);//返回制定对象索引的值 注意只能返回一维 并且返回的对象是object类型---相关  函数还有getint等基本类型
Array.set(arrays, 0, new Integer(12));//将指定的类型传递到数组指定的位置中
```

### AccessibleObject

> AccessibleObject是 Method Fielt Construction的一个父类-都实现了此类的方法,这个类主要是扩展了访问权限的控制

```java
AccessibleObject accessibleObject = null;
accessibleObject.isAnnotationPresent(hehehe.class);//判断这个类是否实现了hehehe这个接口
accessibleObject.getAnnotation(hehehe.class);
accessibleObject.getAnnotations();
//!!!---设置当前东西的访问性--- 设置为true的时候将可以实现对私有变量的  该便似有变量和成员的访问性
accessibleObject.setAccessible(true);
```

尤其要注意这个地方setAccessible(true); 正是通过这个配置方法的访问权限

## 这里其实要记录一下有关于泛型反射的一些东西

我们都知道java的泛型实现是基于类型擦除的,这将会会导致这个泛型的类型将在反射的时候返回具体类型(默认是object)但是这种情况并不是绝对了,目前我总结了三种情况下java会保证原来的类型

1. 生成匿名内部类的时候

也就是new一个接口或者new一个抽象类 这种情况下将会保留原来的属性

实现的原理是java针对匿名内部类将会动态的生成新的class 而这个class的泛型是带有参数的

2. 方法的返回值

所有的方法的方法如果使用泛型类,比如 List<String> 这种情况下是能获取到泛型中的类型的

3. 子类继承泛型父类

其实这种情况是1 类型的手动实现也就是实现下面这种情况

```java
class Item<T>{}

class Itemchildren extends Item<String>{
    private Class<T> entityClass; //这里将会获取到entityClass中的值
    public Itemchildren() {
        entityClass =(Class<T>) ((ParameterizedType) getClass()
                       .getGenericSuperclass()).getActualTypeArguments()[0];
    }
    public T get(Serializable id) {
        T o = (T) getHibernateTemplate().get(entityClass, id);
    }
}
```

