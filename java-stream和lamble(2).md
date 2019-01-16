上一节我们梳理了java lamble相关的东西,这里梳理一下java8 stream相关的东西

### java集合类型的迭代方法

1. 外部迭代 - 循环体和迭代的逻辑在外部

```java
List<Integer>  list = new ArrayList<>();
for (int a=0;a<list.size();a++){
    System.out.println(list.get(a));
}
for(Integer a : list){
    System.out.println(a);
}
Iterator<Integer> integerIterator = list.iterator();
while(integerIterator.hasNext()){
    System.out.println(integerIterator.next());
}
```

> 本质上来讲就是迭代的流程在外部用户可见

![](/blogimg/java/stream_lamble/1.png)


2. 内部迭代

这个是java8的新东西,所有的结合类都可以使用stream接口进行迭代

这里写一个例子,迭代出所有的偶数

```java
List<Integer> list1 = list.stream().filter((item)->{
    if (item % 2 == 0) {
        return true;
    }
    return false;
}).collect(Collectors.toList());
```

> 本质上是内部实现数据的迭代更新,而外部只是实现内部的迭代逻辑罢了

![](/blogimg/java/stream_lamble/2.png)

内部迭代本质上可以是一种函数调用,上面这个例子干了两件事请

- 过滤出所有的偶数
- 生成一个新的集合

> 注意这里好像是迭代了两次但是本质上并没有,记下来说明一下实现的原理

### java stream迭代的内部实现

在java的实现原理中有两种类型,一种是　**惰性求值**　另一种是　**尽早求值**

#### 惰性求值和尽早求值区分方法

其实这个很好记 就是如果返回是stream类的都是惰性求值,反之就是尽早求值

#### 惰性求值和尽早求值的差别

惰性求值其实本质上是不会运行其中的代码的,只有在尽在求值的时候才是真正意义上的执行逻辑

比如这样一个代码

```java
list.stream().filter((item) -> {
    System.out.println(item);
    if (item % 2 == 0) {
        return true;
    }
    return false;
});
```

在这个过程中不会输出item对应的值

> 引申一下:其实这个过程和建造者模式类似,在真正实现之前不停的添加配置和操作,只有在最后的Build过程中才真正的执行

### java stream 的常用操作

1. collect(toList); 及早求值 就不罗嗦了

不过这个有两种种结构

```java
<R> R collect(Supplier<R> supplier,BiConsumer<R, ? super T> accumulator,BiConsumer<R, R> combiner);
```

```java
<R, A> R collect(Collector<? super T, A, R> collector);
```

2. map类型

这个方法很常用,就像他的名字映射,使用这种方法可以直接将一个流转化成另一个流

一个例子,进行一下对比

```java
//使用传统方法
for(String s:strings){
    s.toUpperCase();
}
//使用stream流
strings = strings.stream().map((item)->{
    return item.toUpperCase();
}).collect(Collectors.toList());

strings = strings.stream().map(String::toUpperCase).collect(Collectors.toList());
```




