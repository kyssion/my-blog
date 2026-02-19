java8 stream 在collection接口中添加了一个新的方法叫做stream,之前如果自己定义的子类如果在java8 中没有实现将会报错

所以java在接口上添加了默认方法 default字段来实现更加方便的扩展

### 接口default 的继承性问题

首先总结一下继承的规则:

1. 类胜于接口。如果在继承链中有方法体或抽象的方法声明，那么就可以忽略接口中定义的方法。
2. 子类胜于父类。如果一个接口继承了另一个接口，且两个接口都定义了一个默认方法，那么子类中定义的方法胜出.如果同时继承了两个具有相同方签名的接口,将会报错,因为编辑器不知道选择哪一个,但是可以使用下面的方法来兼容(应用了规则1)

```java
public interface Carriage {
    public default String rock() {
        return "... from side to side";
    }
}
public interface Jukebox {
    public default String rock() {
        return "... all over the world!";
    }
}
public class MusicalCarriage
    implements Carriage, Jukebox {
    @Override
    public String rock() {  //规则1 父类覆盖子类 所以继承的冲突不必考虑了
        return Carriage.super.rock();
    }
}
```
3. 如果上面两条规则不适用，子类要么需要实现该方法，要么将该方法声明为抽象方法.
4. 注意default是针对接口的,所以不存在继承的问题,实现接口的类只是覆盖,不能想类那样使用super去调用父类的东西

### java 接口中statis和 default相同点和区别

- static和之前的规则相同,并不会产生继承效果并且如果要调用这个方法,只能使用定义的时候的类或者接口来进行调用

- defaule 同样是一个默认方法,但是default可以使用继承的或者实现的类来进行调用,但是子类或者接口如果实现了重载

注意: 如果子类或者子接口要想调用父接口中的default方法,可以使用接口名称+super+方法名称调用


```java
public class MusicalCarriage
    implements Carriage, Jukebox {
    @Override
    public String rock() {  //规则1 父类覆盖子类 所以继承的冲突不必考虑了
        return Carriage.super.rock();
    }
}
```
