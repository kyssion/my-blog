### 工厂方法模式

这个模式之前的时候感觉比较困难，现在感觉这个模式同样是比较简单的，要注意一下的几个思想。
1. 工厂方法模式一开始的时候是将工厂接口和工厂生产的产品同时定义出来的。
2. 工厂生产的东西需要传入指定的数据才能生产出来比如下面例子中定义的IDcard类

> 扩展思路> 其实感觉这个模式其实可以和模板方法模式结合使用，在构建产品的过程中使用模板方法模式可以进一步的解耦和优化流程。

### 工厂方法模式的类图

![](blogimg/GAF/5.png)

从类图中可以看出项目中工厂和产品之间的关系

### 工厂方法模式例子

#### 接口

1. 工厂接口

```java
package org.kys.Gaf.FactoryMethod;
public interface Factory{
     Product create(IDcard iDcard);
}
```

2. 产品接口

```java
package org.kys.Gaf.FactoryMethod;
public interface Product {
    void use();
}
```

#### 接口的实现类

1. 工厂的实现类

```java
package org.kys.Gaf.FactoryMethod;

public class BookProduct implements Product{
    IDcard iDcard;
    public BookProduct(IDcard iDcard){
        this.iDcard=iDcard;
    }
    @Override
    public void use() {
        System.out.println(iDcard.getName()+"正在使用：\""+iDcard.getCardName()+"\"ID 卡");
    }
}
```

2. 商品的实现类

```java
package org.kys.Gaf.FactoryMethod;

public class BookProduct implements Product{
    IDcard iDcard;
    public BookProduct(IDcard iDcard){
        this.iDcard=iDcard;
    }
    @Override
    public void use() {
        System.out.println(iDcard.getName()+"正在使用：\""+iDcard.getCardName()+"\"ID 卡");
    }
}
```

#### 信息载体

```java
package org.kys.Gaf.FactoryMethod;

public class IDcard {
    private String cardName;
    private String name;

    public IDcard(String cardName,String name){
        this.cardName=cardName;
        this.name=name;
        System.out.println("创建了"+this.getName()+"的"+this.getCardName()+"卡片");
    }

    public String getCardName() {
        return cardName;
    }

    public void setCardName(String cardName) {
        this.cardName = cardName;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
```

#### 运行主函数

```java
package org.kys.Gaf.FactoryMethod;

public class Main {
    public static void main(String[] args) {
        Factory factory = new BookFactory();
        Product product1= factory.create(new IDcard("美容卡","tom"));
        Product product2= factory.create(new IDcard("购物卡","jack"));
        product1.use();
        product2.use();
    }
}
```
