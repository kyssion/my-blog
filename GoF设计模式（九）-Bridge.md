### 桥接模式

桥接模式我的感觉这个模式就是使用模板方法模式和适配器的模式的结合。

在GoF书中，将类的扩展分为，类的功能层次划分和类的结构层次划分

- 类的功能层次划分： 通过继承来对添加相关的功能，其实也就是外部调用的实际方法

- 类的实现层次划分：父类（接口或者抽象类），通过继承将这个作为一个特殊的实现类适配不同的情况，比如说一个类定义了一个操作系统底层的接口，其子类通过实现，支持了windowns和linux，这里就是类的实现层次划分，针对不同的情况事项不同的接口。

> 桥接模式本质上就是将类的功能层次和实现层次分离


### 桥接模式

![](blogimg/GAF/9.png)

> 桥接模式本质上就是将类的功能层次和实现层次分离

- Abstraction： 这个类提供的功能是对外的功能，也就是说功能上的扩展就是使用这个类通过继承或者其他的方法就行扩展

- Implementor ： 这个类提供的是底层的操作也就是说，这个类只能被Abstraction类使用。

注意：Abstraction的相关方发是使用适配器模式的思想进行调用的，其实本质上是因为Implement是使用引用的方法传入Abstraction类中的，不过这样也好，更加的提高了系统的可扩展性。

### 适配器模式的代码实现

#### Abstraction 功能层次的扩展方法

```java
package org.kys.Gaf.bridge;

public class Abstraction {
    private Implementor implementor=null;
    public Abstraction(Implementor implementor){
        this.implementor = implementor;
    }
    public void showprint(int speed){
        implementor.print(speed);
    }
}
```

#### Abstraction 的两个实现类，实现不同的功能（startToDisplay）方法

```java
package org.kys.Gaf.bridge;

public class CountAbstraction extends Abstraction {
    public CountAbstraction(Implementor implementor) {
        super(implementor);
    }
    public void startToDisplay(int line){
        for(int a=0;a<line;a++){
            showprint(a);
        }
    }
}

package org.kys.Gaf.bridge;

public class DubboAbstraction extends Abstraction{

    public DubboAbstraction(Implementor Implementor) {
        super(Implementor);
    }

    public void startToDisplay(int line){
        for(int a=0;a<line;a++){
            showprint(a*2);
        }
    }
}
```

#### Implement 类的实现层次

```java
package org.kys.Gaf.bridge;

public abstract class Implementor {
    public abstract void print(int a);
}
```

#### 类的实现层次的功能

```java
package org.kys.Gaf.bridge;

public class StringImplementor extends Implementor{
    private String cStart;
    private String cEnd;
    private String item;
    public StringImplementor(String cStart,String cEnd,String item) {
        this.cStart = cStart;
        this.cEnd = cEnd;
        this.item=item;
    }
    @Override
    public void print(int length) {
        System.out.print(cStart);
        for(int a=0;a<length;a++){
            System.out.print(item);
        }
        System.out.println(cEnd);
    }
}
```

#### 主函数

```java
package org.kys.Gaf.bridge;

public class Main {
    public static void main(String[] args) {
        Abstraction display = new CountAbstraction(new StringImplementor("|","|","*"));
        display.showprint(6);
        System.out.println();
        ((CountAbstraction) display).startToDisplay(6);

        Abstraction display2 = new DubboAbstraction(new StringImplementor("|","|","*"));
        display.showprint(6);
        System.out.println();
        ((DubboAbstraction) display2).startToDisplay(6);
    }
}
```