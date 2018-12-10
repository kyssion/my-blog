### 原型模式

原型模式其实本质上解决了如下的两个问题：
- 类名称和类的绑定，无法实现动态的（通过字符串或者名称很方便的）生成想要生成的相关累的实例。
- 一个统一的入口将相同种类（实现同一个借口或者继承自相同的类的类）进行统一的管理

> 自我引申： 感觉这个模式，相当于商品的买卖，而圆形模式中的字符串就相当于需要金钱（一种通用的可共识的东西），而产出的类，就相当于商品

### 原型模式类图

![](blogimg/GAF/6.png)

根据上面所说的我的理解可以这么类比

- client 相当于用户
- users 的过程相当于付款
- prototype的createClone 相当于取货的过程
- 最后 concretePrototype（prototype） 就是商品

通过这样的分析，其实理论上createClone和prototype应该是要解耦的但是，因为java中clone只能自调用所以采用这种方法，其实可以在分装一层调用层，不过这样就增加了复杂度了，这里就不多说了。

方便理解；下面是程序的类图

![](blogimg/GAF/7.png)

### 原型模式例子

#### client 的实现

```java
package org.kys.Gaf.prototype;

import java.util.HashMap;

public class Message {
    private HashMap<String,Product> showcase =
            new HashMap<>();
    public void register(String name,Product o){
        showcase.put(name,o);
    }
    public Product create(String name){
        return showcase.get(name).createClone();
    }
}
```

#### 商品接口的实现

```java
package org.kys.Gaf.prototype;

public interface Product extends Cloneable{
    void use(String message);
    Product createClone();
}
```

#### 商品接口的实现类

```java
package org.kys.Gaf.prototype;

public class MessageBox implements Product {

    private char segmentation;

    public MessageBox(char segmentation) {
        this.segmentation = segmentation;
    }

    @Override
    public void use(String message) {
        printLine(message.length());
        System.out.println(this.segmentation + message + this.segmentation);
        printLine(message.length());
    }

    private void printLine(int length) {
        for (int a = 0; a < length + 2; a++) {
            System.out.print(this.segmentation);
        }
        System.out.println();
    }

    @Override
    public Product createClone() {
        try {
            return (Product) this.clone();
        } catch (CloneNotSupportedException e) {
            e.printStackTrace();
            return null;
        }
    }
}
```

```java
package org.kys.Gaf.prototype;

public class UnderLinerBox implements Product{

    private char segmentation;

    public UnderLinerBox(char segmentation){
        this.segmentation=segmentation;
    }

    @Override
    public void use(String message) {
        System.out.println(this.segmentation+message+this.segmentation);
        printLine(message.length());
    }

    private void printLine(int length) {
        for (int a = 0; a < length + 2; a++) {
            System.out.print(this.segmentation);
        }
        System.out.println();
    }

    @Override
    public Product createClone() {
        try {
            return (Product) this.clone();
        } catch (CloneNotSupportedException e) {
            e.printStackTrace();
            return null;
        }
    }
}
```

#### 主函数

```java
package org.kys.Gaf.prototype;

public class Main {
    public static void main(String[] args) {
        Message message = new Message();
        Product box1 = new MessageBox('~');
        Product box2 = new MessageBox('*');
        Product box3 = new UnderLinerBox('-');

        message.register("~",box1);
        message.register("*",box2);
        message.register("-",box3);

        Product boxx1 = message.create("~");
        Product boxx2 = message.create("*");
        Product boxx3 = message.create("-");

        System.out.println(box1+" "+boxx1);
        System.out.println(box2+" "+boxx2);
        System.out.println(box3+" "+boxx3);

        boxx1.use("hello world");
        boxx2.use("hello world");
        boxx3.use("hello world");
    }
}
```