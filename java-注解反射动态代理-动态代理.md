代理模式是软件工程一种常见的设计模式,也是spring框架实现aop的核心方法,这里方便立即首先记录一下静态代理模式

## 静态代理模式

首先定义一个接口和一个接口实现类

```java
public interface UserService {
    public void select();   
    public void update();
}
public class UserServiceImpl implements UserService {  
    public void select() {  
        System.out.println("查询 selectById");
    }
    public void update() {
        System.out.println("更新 update");
    }
}
```

我们将通过静态代理对 UserServiceImpl 进行功能增强，在调用 select 和 update 之前记录一些日志。写一个代理类 UserServiceProxy，代理类需要实现 UserService

```java
public class UserServiceProxy implements UserService {
    private UserService target; // 被代理的对象
    public UserServiceProxy(UserService target) {
        this.target = target;
    }
    public void select() {
        before();
        target.select();    // 这里才实际调用真实主题角色的方法
        after();
    }
    public void update() {
        before();
        target.update();    // 这里才实际调用真实主题角色的方法
        after();
    }
    private void before() {     // 在执行方法之前执行
        System.out.println(String.format("log start time [%s] ", new Date()));
    }
    private void after() {      // 在执行方法之后执行
        System.out.println(String.format("log end time [%s] ", new Date()));
    }
}
```

客户端测试

```java
public class Client1 {
    public static void main(String[] args) {
        UserService userServiceImpl = new UserServiceImpl();
        UserService proxy = new UserServiceProxy(userServiceImpl);
        proxy.select();
        proxy.update();
    }
}
```

输出

```shell
log start time [Thu Dec 20 14:13:25 CST 2018] 
查询 selectById
log end time [Thu Dec 20 14:13:25 CST 2018] 
log start time [Thu Dec 20 14:13:25 CST 2018] 
更新 update
log end time [Thu Dec 20 14:13:25 CST 2018] 
```

通过静态代理，我们达到了功能增强的目的，而且没有侵入原代码，这是静态代理的一个优点。

> 静态代理的缺点

    虽然静态代理实现简单，且不侵入原代码，但是，当场景稍微复杂一些的时候，静态代理的缺点也会暴露出来。

1. 当需要代理多个类的时候，由于代理对象要实现与目标对象一致的接口，有两种方式：
    只维护一个代理类，由这个代理类实现多个接口，但是这样就导致代理类过于庞大    
    新建多个代理类，每个目标对象对应一个代理类，但是这样会产生过多的代理类
2. 当接口需要增加、删除、修改方法的时候，目标对象与代理类都要同时修改，不易维护。

## java提供的jdk代理

java 作为面向对象的坚挺实现者,必然支持动态代理,这里介绍一下java基于接口设计的动态代理模式

1. java动态代理的实现者 InvocationHandler 接口

每一个动态代理类都必须要实现InvocationHandler这个接口，并且每个代理类的实例都关联到了一个handler，当我们通过代理对象调用一个方法的时候，这个方法的调用就会被转发为由InvocationHandler这个接口的 invoke 方法来进行调用。

```java
Object invoke(Object proxy, Method method, Object[] args) throws Throwable
```

这个方法拥有三个参数分别表示

- proxy:指代我们所代理的那个真实对象
- method:指代的是我们所要调用真实对象的某个方法的Method对象
- args:指代的是调用真实对象某个方法时接受的参数

2. 创建代理的类Proxy

之前说了通过实现Invocationhandle接口可以创建代理,java 还提供了一个特殊的类来方便我们创建代理对象实例

proxy类有很多方法,这里我们只观察最常用的方法

```java
public static Object newProxyInstance(ClassLoader loader, Class<?>[] interfaces,  InvocationHandler h)  throws IllegalArgumentException
```

这个方法有三个参数,这里列举一下这些方法的作用 

- loader:一个ClassLoader对象，定义了由哪个ClassLoader对象来对生成的代理对象进行加载
- interfaces:一个Interface对象的数组，表示的是我将要给我需要代理的对象提供一组什么接口，如果我提供了一组接口给它，那么这个代理对象就宣称实现了该接口(多态)，这样我就能调用这组接口中的方法了
- h:一个InvocationHandler对象，表示的是当我这个动态代理对象在调用方法的时候，会关联到哪一个InvocationHandler对象上

这里列一个列子

接口和实现类

```java
public interface TestInterface {
    String say(String he);
}

public class TestInterfaceImp implements TestInterface {
    @Override
    public String say(String he) {
        System.out.println("this is " + he);
        return he;
    }
}
```

InvocationHandle接口实现类

```java
public class Myproxy<T> implements InvocationHandler {
    private T testT;
    public Myproxy(T testT){
        this.testT=testT;
    }
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        System.out.println("before");
        Object tiem = method.invoke(testT,args);
        System.out.println("end");
        return tiem;
    }
}
```

调用方法

```java
public static void main(String[] args) {
    Myproxy<TestInterface> myproxy = new Myproxy<>(new TestInterfaceImp());
    TestInterface testInterface = (TestInterface) Proxy.newProxyInstance(main.class.getClassLoader(),new Class[]{TestInterface.class},myproxy);
    testInterface.say("test");
}
```

输出结果

```shell
before
this is test
end
```

引申: java是动态生成代理,调用的是真实的类的方法

上面Main方法中通过动态代理生成的对象,其实并不是TestInterface对象,而是$Proxy0..2 这样的对象,这个是java一个特殊的代理对象,可以强制转化成Proxy的newProxyInstance方法第二个参数传入的所有类型

当这个方法调用对应的方法时,将会动态的桥接给实现Invocationhandle接口的代理类的invoke方法,其实method解释这个接口这个方法的Method反射