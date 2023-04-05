今天在进行 java 反射库的封装过程中,发现了一个问题,之前对java重载和重写的机制认识并不是很深入.这里决定深入的整理一下

## 重载

- 定义
  - 一个类中具有多个重名的方法,如果父子类满足条件也能构成重载方法
- 特点
  - 1. 方法名称相同
  - 2. 参数列表不许不同
    - 个数不同
    - 个数相同但是类型不同(包不包括父子关系)
    - 返回值,访问修饰符号可以相同也可以不相同

注意:这一点没有考虑到如果是继承关系,两个看似重载的父子关系是否实际上构成重载关系

## 重写
- 定义
  - 子类重写父类的一个方法
- 特点
  - 1. 子类继承父类
  - 2. 返回值名称参数不能改变(子类的参数,返回值可以是父类对应的参数的子类)
- 限制(不能进行重写的方法)
  - 1. private修饰的方法
  - 2. 构造函数
  - 3. final,static 方法(static 将会被再次声明)
  - 4. 重写方法不能缩小父方法的权限
  - 5. 重写方法不能抛出任何新的强制性异常或者比父类方法范围广的强制性异常(补充出列RuntimeException之外都是强制异常)

## 重载和重写的对比

![](blogimg/java/12.png)

## 重载中产生的桥接方法

重载中可能有这样一种情况:重写方法的返回类型是其父类返回类型的子类型

在这种情况下jvm将会自动的生成桥接方法来作为子类和父类调用之间的桥梁

```java
public class Merchant {
    public Number actionPrice(double price) {
        return price * 0.8;
    }
}
public class NaiveMerchant extends Merchant {

    @Override
    public Double actionPrice(double price) {
        return 0.9 * price;
    }
    public static void main(String[] args) {
        Merchant merchant = new NaiveMerchant();
        // price 必须定义成 Number 类型 
        Number price = merchant.actionPrice(40);
        System.out.println(price);
    }
}
```

比如这样的两个类,NaiveMerchant类继承自Merchant,重载了actionPrice方法,并且Double类型是Number类型的子类

这样在jvm编译过程中将会自动生成一个中间方法

```java
public Number actionPrice(double price) {
     return this.actionPrice(price);
}
```

注意这种情况只是针对,使用父类调用子类重写的逻辑这种情况

```java
public static void main(String[] args) {
    Merchant merchant = new NaiveMerchant();
    // price 必须定义成 Number 类型 
    Number price = merchant.actionPrice(40);
    System.out.println(price);
}
```

引申一下: 其实在泛型的使用中,同样会出现这种情况