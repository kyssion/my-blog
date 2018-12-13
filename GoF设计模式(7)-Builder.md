### 建造者模式

这个模式在我的个人感觉中感觉就像是升级版的模板方法模式，这个模式中的director起到了监控和调用各种builer类的方法（感觉相当于在），然后在director中编写对应的流程函数（construction）来调用指定的相关的各种函数。和模板方法中使用hashmap进行字符串到具体clone 的对应关系相同，在建造者模式中我也使用了HashMap进行获取对象的解耦，实现了统一入口

> 引申: 其实在director中指定相关的函数并不是一个很好的方法，其实可以实现一个模板接口，通过这个接口动态的实现相关的策略，以后再想想。

### 建造者模式类图

![](blogimg/GAF/8.png)

### 建造者模式实例

#### Director

```java
package org.kys.Gaf.builder;

import java.util.HashMap;

public class Director {
    private HashMap<String,Builer> map = new HashMap<>();
    public Director(String name,Builer builer){
        map.put(name,builer);
    }
    public Director(){
        super();
    }
    public boolean setBuiler(String name,Builer builer){
        if(builer==null){
            return false;
        }
        map.put(name,builer);
        return true;
    }
    public void construction(String name){
        Builer builer = map.get(name);
        //build 只能按照输入进行运作，无法窥视到内部实现
        builer.makeTitile("----------");
        builer.makeItem("builer item");
        builer.makeEndoFText("----------");
    }
}
```

#### builer接口

```java
package org.kys.Gaf.builder;

public abstract class Builer<T> {
    public abstract void makeTitile(String title);
    public abstract void makeItem(String item);
    public abstract void makeEndoFText(String end);
    public abstract T getResult();
}
```

#### builer 实现类

```java
package org.kys.Gaf.builder;

public class HtmlBuiler extends Builer{

    StringBuffer stringBuffer = new StringBuffer();

    @Override
    public void makeTitile(String title) {
        stringBuffer.append("<p>"+title+"</p>\n");
    }

    @Override
    public void makeItem(String item) {
        stringBuffer.append("<p>"+item+"</p>\n");
    }

    @Override
    public void makeEndoFText(String end) {
        stringBuffer.append("<p>"+end+"</p>\n");
    }

    @Override
    public String getResult() {
        return stringBuffer.toString();
    }
}
```

```java
package org.kys.Gaf.builder;

//范型在定义的时候使用
public class TextBuilder extends Builer{

    StringBuffer stringBuffer = new StringBuffer();

    @Override
    public void makeTitile(String title) {
        stringBuffer.append(title+"\n");
    }

    @Override
    public void makeItem(String item) {
        stringBuffer.append(item+"\n");
    }

    @Override
    public void makeEndoFText(String end) {
        stringBuffer.append(end+"\n");
    }

    @Override
    public String getResult(){
        return stringBuffer.toString();
    }
}
```

#### client 或者主函数

```java
package org.kys.Gaf.builder;

public class Main {
    public static void main(String[] args) {
        Builer textBuiler = new TextBuilder();
        Builer htmlBuiler = new HtmlBuiler();
        Director director = new Director();
        director.setBuiler("text",textBuiler);
        director.setBuiler("html",htmlBuiler);

        director.construction("text");
        director.construction("html");

        System.out.println(textBuiler.getResult());
        System.out.println(htmlBuiler.getResult());
    }
}
```