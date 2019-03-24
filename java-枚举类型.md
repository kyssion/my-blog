## 枚举类型

在java世界使用enum类型的场景是非常多的，但是相比较java中其他的类型这个类型使用的时候还是比较少的这里记录一下

### 枚举类型创建

> 枚举类型的创建和传统的类的实现是相同的，不过要注意枚举类型拥有一个高级的用法用法就是使用values对枚举类型每部的属性进行迭代，和使用valueof 获得指定的枚举对象

```java
package com.kys;

enum Color {
    RED("红色"),BLUE("蓝色");
    private String colorName;
    Color(String colorName){
        this.colorName=colorName;
    }
    public String getColorName() {
        return colorName;
    }

    public void setColorName(String colorName) {
        this.colorName = colorName;
    }
}
public class Demo {
    public static void main(String[] args) {
        Color color = Color.valueOf("RED");//通过使用此方法获得指定的枚举
        System.out.println(color.getColorName());
        Color[] colors = Color.values();//通过这个方法获得所有的枚举
        Color red = Color.RED;//获得其中一个对象
    }
}

```

### 使用switch 判断Enum对象

```java
public enum POSITION {
    BEFORE(1), END(2), BEFEND(3), OTHER(4);
    public int way;

    POSITION(int way) {
        this.way = way;
    }

    public int getWay() {
        return way;
    }

    public void setWay(int way) {
        this.way = way;
    }

    public static POSITION getPositionValue(int way) {
        for (POSITION position : values()) {
            if (position.getWay() == way) {
                return position;
            }
        }
        return OTHER;
    }
}
public static String SolLikeFieldSqlInjPlbm(String s, POSITION sqlPostion) {
    if (s == null || s.equals("")) {
        return null;
    }
    switch (POSITION.getPositionValue(sqlPostion.getWay())) {
        case BEFORE:
            return "%" + s;
        case END:
            return s + "%";
        case BEFEND:
            return "%" + s + "%";
        default:
            return null;
    }
}
```

> 注意这里使用的getPositionValue 方法 因为POSTOPN相当一个声明和String类似，所以不能直接的使用sqlPostion来作为switch的标记，需要使用实现类来标记，所以使用switch的写法要这样写