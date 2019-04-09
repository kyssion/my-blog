
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