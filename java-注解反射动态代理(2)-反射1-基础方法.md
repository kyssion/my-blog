## 反射的定义

在运行状态中，对于任意一个类，都能够知道这个类的所有属性和方法；对于任意一个对象，都能够调用它的任意一个方法和属性；这种动态获取的信息以及动态调用对象的方法的功能称为反射。

在java中反射是基于class信息的

> 关于Class:Class是一个类，一个描述类的类（也就是描述类本身），封装了描述方法的Method，描述字段的Filed，描述构造器的Constructor等属性

## java反射相关的接口方法和最佳实践

### class

class 是java反射的最粗集合,分装了class对应的各种属性

1. 获取class 名称或者类型名称

java的class 对象提供了两个方法获取名称字符串

> getName

这个方法会返回这个class的解析名称,绝提规则如下

如果是对象,就返回对象的全限定名称(没有泛型信息)
如果是数组返回如下信息,[表示维度
[Z = boolean 
[B = byte 
[S = short 
[I = int 
[J = long 
[F = float 
[D = double 
[C = char 
[L = any non-primitives(Object)

> getTypeName

返回类型通getName方法

如果是数组集合或者对象,返回这个的定义格式

比如如果是int[][][] 将会返回int[][][]

2. class 继承关系状态获取

```java
class.getSuperclass();//返回直接的父类,如果没有就返回null
class.getDeclaringClass();//返回内部声明的类的包装类,针对内部类的情况返回包装类
class.getEnclosingClass();//DeclaringClass方法的增强版,还可以返回匿名内部类的增强
class.getInterfaces();//返回这个class直接实现的接口
```

通过这种方法可以快速查找class的继承关系

3. class 有关java Type体系的信息获取

```java
class.getGenericInterfaces();//返回父接口的Type可以针对java泛型参数化规则进行处理,获取泛型中的真实类型
class.getGenericSuperclass();//返回父类的Type,可针对java泛型参数化进行特殊处理,获取到泛型中真实的数值
class.getTypeParameters();//返回这个类的Type类型,符合java 泛型type信息获取规
```

4. class 有关包信息的方法

```java
class.getPackageName();//包名
class.getPackage();//包类
```

5. class的访问级别

```java
class.getModifiers();//返回这个class访问级别
```

6. class 对象或者class类强制转化提供的功能

```java
class.asSubclass(class);//强制转化成指定的class会生成警告,因为泛型无法确定转化是否成功
class.cast(new Object());//将传入的类型前置转化成调用的class类型
```

7. 针对特殊类型比如arr类型枚举的特殊处理方法

```java
class.getComponentType();//如果这个class是一个数组类型,将会返回这个数组的类型
class.getEnumConstants();//返回此枚举类的元素，如果此Class对象不表示枚举类型，则返回null
```

8. 各种is方法

```java
class.isAnnotation();//是否是注解
class.isAnnotationPresent(Mapper.class);//是否是指定的注解
class.isAnonymousClass();//是否是匿名类
class.isArray();//是否是数组
class.isAssignableFrom(Test.class);//如果调用类是参数的父类或者同一个类返回true
class.isEnum();//是否是枚举
class.isInstance(new Object());//确定指定的Object是否与此Class表示的对象分配兼容。相当于动态等效的instanceof
class.isInterface();//是否是接口
class.isLocalClass();//是否是局部类,就是在块中的类
class.isPrimitive();//这个类是否是基本类型
class.isSynthetic();//这个是个bug般的东西,看其他人的博客把https://blog.csdn.net/a327369238/article/details/52608805
```

9. 注解使用方法

```java
item.getAnnotations();//获取所有的注解(包括继承的注解,但是并不包括重复注解)
item.getAnnotation(Mapper.class);//返回指定类型的注解
item.getDeclaredAnnotations();//返回这个类的直接注解
item.getDeclaredAnnotation(Mapper.class);//返回这个类的指定类型的直接注解

item.getAnnotationsByType(Mapper.class);//返回这个这个累的指定类型的注解,包括重复注解
item.getDeclaredAnnotationsByType(Mapper.class);//返回这各类指定类型的注解包括重复注解,不可返回继承的
```

10. 类加载器获取

```java
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

11. 资源获取

```java
// /(左划线)表示使用classpath根目录进行下过关属性的查找
TestRelativePath.class.getResource(“/test.txt”).getFile()
Thread.currentThread().getContextClassLoader().getResource(“test.txt”).getFile()
```

### field

field是java参数属性的载体.

1. field获取方法

```java
class.getField("xxx");//获取指定名称的field对象,只针对于public属性,包括父类
class.getDeclaredField("");//获取名称的field,不限制类型和访问权限,只限于当前类
class.getFields();//获取所有的public对象Field数组
class.getDeclaredFields();//获取当前类型所有的field引用
```

2. field一些属性信息方法

```java
field.getType();//返回参数的class类型如果是泛型将会返回Object类型
field.setAccessible(true);//设置为true表示可以对private参数尽心操作
field.toGenericString();//返回参数名称 比如 T org.ksql.test.Find.test
field.toString();//返回参数名称 java.lang.Object org.ksql.test.Find.test
field.getDeclaringClass();//返回包裹这个参数的类的类型
```

3. field设置和获取方法

```java
field.get();
field.set(Object);

field.getInt();//field 提供了一系列的方法用来获取指定类型
field.setInt(12);//field提供了一系列的方法来设置指定的类型
```

4. field类型获取方法

```java
field.getType();//获取变量对应的类型
field.getGenericType();//获取变量对应的类型type
```

5. 针对注解的方法

```java
Annotation annotation=field.getDeclaredAnnotation(Mapper.class);
Annotation[] annotations= field.getDeclaredAnnotations();//获取所有的注解包括重复主机,不保留继承的注解
Annotation[] annotations2=field.getAnnotations();//获取所有的注解.保留继承

//这两个增加了对java8 重复注解的支持,Declared只是保证非继承
Annotation[] annotations3= field.getAnnotationsByType(Mapper.class);//支持可重复注解
Annotation[] annotations1=field.getDeclaredAnnotationsByType(Mapper.class);//返回直接存在于此元素上的所有注解。与此接口中的其他方法不同，该方法将忽略继承的注释

```

### method

1. 获取方法

```java
item.getMethod("",new Class[]{});
item.getMethods();
item.getDeclaredMethod("",new Class[]{});
item.getDeclaredMethods();
//这些方法和上面的规则相同Declared表示不受访问权限限制但是只能访问当前的类的信息没有表示受但是会返回所有
item.getEnclosingMethod()//该类是在哪个方法中定义的，比如方法中定义的匿名内部类
```

2. method参数相关操作方法方法

```java
method.getGenericParameterTypes();//返回参类型的数组
method.getParameterTypes();//返回参数类型class数组
method.getParams(); //返回参数数组  
method.getTypeParameters();//返回 <S> T method S对应的信息
method.getParameterCount();//返回参数数量
```

3. method返回值相关参数方法

```java
method.getGenericReturnType();//获取变量的type类型
method.getReturnType();//获取变量的返回值class
```

4. 运行方法

```java
method.invoke(new Object(),new Object[]{});//运行方法
```

5. 注解方法

相比较其他的编程语言方法,method只是多了获取参数的注解方法

```java
method.getParameterAnnotations();
method.getDeclaredAnnotations();
method.getDeclaredAnnotation(Mapper.class);
method.getDeclaredAnnotationsByType(Mapper.class);
```

6. 异常捕获

```java
method.getExceptionTypes();//获取异常class
method.getGenericExceptionTypes();//获取异常Type
```

7. method属性操作相关方法

```java
method.getDefaultValue();//如果这个方法是注解类型的方法,就返回这个注解的默认值
method.getName();//返回方法的签名信息
method.getModifiers();//返回方法的类型
method.isBridge();//返回这个方法是否是桥接方法
method.isDefault();//方法这个方法是否是在java8+接口中定义的额default方法
method.isSynthetic();//放回这个方法是否使用了线程同步修饰符号修饰
method.isVarArgs();//这个方法的是否是不定长的
```

8. 

### Constructor

java的constructer可以理解成特殊的方法(java中并不等同,处理方法,继承信息等等都是不相同的),方法都是通用的,这里记录一下不同的方法

1. constructor获取方法

```java
item.getConstructor(String.class);
item.getConstructor();
item.getConstructors();
item.getDeclaredConstructor(String.class);
item.getDeclaredConstructors();
item.getEnclosingConstructor()//该类是在哪个构造函数中定义的，比如构造方法中定义的匿名内部类
```

这里不解释了,没有Declared的方法表示获取所有的public构造函数,有的将会获取这个类中直接定义的构造好书

2. 构造函数创建实体类

```java
constructor.newInstance("param");//直接构造参数,param就是构造函数中的参数
```

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

-----------------

## 这里其实要记录一下有关于泛型反射的一些东西

我们都知道java的泛型实现是基于类型擦除的,这将会会导致这个泛型的类型将在反射的时候返回具体类型(默认是object)但是这种情况并不是绝对了,目前我总结了三种情况下java会保证原来的类型

1. 生成匿名内部类的时候

也就是new一个接口或者new一个抽象类 这种情况下将会保留原来的属性

实现的原理是java针对匿名内部类将会动态的生成新的class 而这个class的泛型是带有参数的

2. 方法的返回值

所有的方法的方法如果使用泛型类,比如 List<String> 这种情况下是能获取到泛型中的类型的

3. 子类继承泛型父类

其实这种情况是1 类型的手动实现也就是实现下面这种情况d

```java
class Item<T>{}

class Itemchildren extends Item<String>{
    private Class<T> entityClass; //这里将会获取到entityClass中的值
    public Itemchildren() {
        entityClass =(Class<T>) ((ParameterizedType) getClass()
                       .getGenericSuperclass()).getActualTypeArguments()[0];
    }
    public T get(Serializable id) {
        //拿到了参数内部强制转化
        return entityClass.case(new Object);
    }
}
```

总结一些,如果泛型想要拿到参数,必须在声明类的时候就将泛型对应的参数传递进入