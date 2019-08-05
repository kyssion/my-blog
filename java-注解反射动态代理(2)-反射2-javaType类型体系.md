

# Java Type体系简介

Type是Java 编程语言中所有类型的公共高级接口,注意这个类型并不是我们传统上常说的int、String、List、Map等数据类型而是从Java语言角度来说，对基本类型、引用类型向上的抽象

Type体系中类型的包括：

- 原始类型\基本类型(Class) : 常所指的类，还包括枚举、数组、注解等
- 参数化类型(ParameterizedType) : 指泛型,如泛型List、Map或泛型类
- 数组类型(GenericArrayType) : 指带有泛型的数组，即T[] 
- 类型变量(TypeVariable) : 类型变量，即泛型中的变量；例如：T、K、V等变量，可以表示任何类
- 泛型表达式(WildcardType) : 这个type类型是解决泛型? extend Number、? super Integer这样的表达式,相关类型的特殊Type子类(这个类和TypeVariable对应,TypeVariable相当于具体的类型而WildcardType相当于真实的类型)

这里具体的介绍一下相关的内容

## 1. ParameterizedType

ParameterizedType表示参数化类型，也就是泛型，例如List<T>、Set<T>等,

在ParameterizedType接口中，有3个方法，分别是getActualTypeArgumen   ts()、 getRawType()、 getOwnerType();

1. getActualTypeArguments()
 
获取泛型中的实际类型，可能会存在多个泛型，例如Map<K,V>,所以会返回Type[]数组

![](/blogimg/java/t/1.png)

值得注意的是，无论<>中有几层嵌套(List<Map<String,Integer>)，getActualTypeArguments()方法永远都是脱去最外层的<>(也就是List<>)，将口号内的内容（Map<String,Integer>）返回；我们经常遇到的List<T>，通过getActualTypeArguments()方法，得到的返回值是TypeVariableImpl对象，也就是TypeVariable类型(后面介绍);


2. getRawType()

获取声明泛型的类或者接口，也就是泛型中<>前面的那个值；

![](/blogimg/java/t/2.png)

3. getOwnerType()

通过方法的名称，我们大概了解到，此方法是获取泛型的拥有者，那么拥有者是个什么意思？Returns a {@code Type} object representing the type that this type     * is a member of.  For example, if this type is {@code O.I},     * return a representation of {@code O}.  （摘自JDK注释）通过注解，我们得知，“拥有者”表示的含义--内部类的“父类”，通过getOwnerType()方法可以获取到内部类的“拥有者”；例如： Map  就是 Map.Entry<String,String>的拥有者；

![](/blogimg/java/t/3.png)

## 2. GenericArrayType

泛型数组类型，例如List<String>[] 、T[]等；

![](/blogimg/java/t/4.png)

在GenericArrayType接口中，仅有1个方法，就是getGenericComponentType()；

![](/blogimg/java/t/5.png)

1. getGenericComponentType()

返回泛型数组中元素的Type类型，即List<String>[] 中的 List<String>（ParameterizedTypeImpl）、T[] 中的T（TypeVariableImpl）；

![](/blogimg/java/t/6.png)

值得注意的是，无论是几维数组，getGenericComponentType()方法都只会脱去最右边的[]，返回剩下的值

## 3. TypeVariable

泛型的类型变量，指的是List<T>、Map<K,V>中的T，K，V等值，实际的Java类型是TypeVariableImpl（TypeVariable的子类）；此外，还可以对类型变量加上extend限定，这样会有类型变量对应的上限

![](/blogimg/java/t/7.png)

在TypeVariable接口中，有3个方法，分别为getBounds()、getGenericDeclaration()、getName()

1.  getBounds()

获得该类型变量的上限，也就是泛型中extend右边的值；例如 List<T extends Number> ，Number就是类型变量T的上限；如果我们只是简单的声明了List<T>（无显式定义extends），那么默认为Object；

![](/blogimg/java/t/8.png)

无显式定义extends：

![](/blogimg/java/t/9.png)

值得注意的是，类型变量的上限可以为多个，必须使用&符号相连接，例如 List<T extends Number & Serializable>；其中，& 后必须为接口；

2. getGenericDeclaration()

获取声明该类型变量实体，也就是TypeVariableTest<T>中的TypeVariableTest

![](/blogimg/java/t/10.png)

3. getName()

获取类型变量在源码中定义的名称

![](/blogimg/java/t/11.png)

说到TypeVariable类，就不得不提及Java-Type体系中另一个比较重要的接口---GenericDeclaration；含义为：声明类型变量的所有实体的公共接口；也就是说该接口定义了哪些地方可以定义类型变量（泛型）；

通过查看源码发现，GenericDeclaration下有三个子类，分别为Class、Method、Constructor；也就是说，我们定义泛型只能在一个类中这3个地方自定义泛型；

![](/blogimg/java/t/12.png)

此时，我们不禁要问，我们不是经常在类中的属性声明泛型吗，怎么Field没有实现 GenericDeclaration接口呢？

其实，我们在Field中并没有声明泛型，而是在使用泛型而已

```java
class Item<T>{
    T item;
}
```

正因为是使用泛型，所以Field并没有实现GenericDeclaration接口

## 4. WildcardType

？---通配符表达式，表示通配符泛型，但是WildcardType并不属于Java-Type中的一钟；例如：List<? extends Number> 和 List<? super Integer>

在WildcardType接口中，有2个方法，分别为getUpperBounds()、getLowerBounds();

![](/blogimg/java/t/13.png)

1. getUpperBounds()

获取泛型变量的上边界（extends）

![](/blogimg/java/t/14.png)

2. getLowerBounds

获取泛型变量的下边界（super）

![](/blogimg/java/t/15.png)