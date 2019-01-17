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

####　1. collect(toList); 及早求值 就不罗嗦了

不过这个有两种种结构

```java
<R> R collect(Supplier<R> supplier,BiConsumer<R, ? super T> accumulator,BiConsumer<R, R> combiner);
```

```java
<R, A> R collect(Collector<? super T, A, R> collector);
```

#### 2. map类型

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

#### 3. filter 

这个是过滤器,通过这种方法可以将感兴趣的stream流中的对象整合进新的对象中

```java
list.stream().filter((item) -> {
    System.out.println(item);
    if (item % 2 == 0) {
        return true;
    }
    return false;
}).collect(Collectors.toList());
```

#### 4. flapMap

map 的升级版 flatMap 方法可用 Stream 替换值，然后将多个 Stream 连接成一个 Stream,说白了就是整合流用的

```java
List<String> objects = Stream.of(strings).flatMap(item->{// 这里的item是list对象,应为传入的就是strings list
//返回值需要是stream用于合并流
    return item.stream().map(i->{
        i.toUpperCase();
        i+="xxx";
        return i;
    });
}).collect(Collectors.toList());
```
#### 5. max和min

```java
Integer integer = list.stream().max(Comparator.comparing(item->{
    return item;
})).get();
```

max 和min一样只要有一个比较器就好了,但是java底层有关这一层的封装特性比较复杂,接下来引申一下java Comparator#comparing方法的相关实现

```java
public static <T, U extends Comparable<? super U>> Comparator<T> comparing(
            Function<? super T, ? extends U> keyExtractor){
    Objects.requireNonNull(keyExtractor);
    return (Comparator<T> & Serializable)
        (c1, c2) -> keyExtractor.apply(c1).compareTo(keyExtractor.apply(c2));
}
```

首先看一下接口的定义 T 只是一个普通的变量 U在这里必须是一个实现了Comparable接口的类(java类内部比较函数), 而传入的Function Lamble 表达式的返回值也是u,这样就可以理解了java Comparator的这个方法干了什么了-> **传入一个可以生成可比较类的Function lamble 表达式,返回一个Comparator 比较逻辑** ps: 封转的很牛逼!

> 注意这里有一个java8 的全新语法 类1 & 类2 其实这个接口相当于强制转化成一个同时 继承了类1 类2 的对象,这个用法的规则通java的继承规则

其实java 如果编写相关的逻辑的时候使用的写法类似这样的

```java
Object accumulator = initialValue;
for(Object element : collection) {
    accumulator = combine(accumulator, element);
    //combine 是一个方法 比较accumulator 和 element 然后挑选一个进行赋值
}
```

> *** : 其实看一下jdk底层的源代码就知道了,其实这个东西本质上是调用了reduce 方法接下来来说一下reduce这个方法

####　6. reduce 

一个调用的例子
```java
int a=list.stream().reduce(0,(x,y)->{
    return x+y;
},(x,y)->{
    return x-y;
});
```

reduce模式的核心就是accumulator 迭代器, 这个方法第一个参数是每次迭代的返回值,第二个参数是当前进行迭代的值, 转换成java代码就是如下的形式

```java
U result = identity;
for (T element : this stream){
    result = accumulator.apply(result, element)
    return result;
}
```

reduce主要有三种形式

```java
T reduce(T identity, BinaryOperator<T> accumulator);
Optional<T> reduce(BinaryOperator<T> accumulator);
<U> U reduce(U identity,BiFunction<U, ? super T, U> accumulator,BinaryOperator<U> combiner);
```

类型1 和 2 没什么好说的都是迭代求值,罢了 注意第二种方法是Optional类型的返回值

类型3 有两个相同的迭代函数 accumulator 和 combiner,具有这个设计的原因是这样的,Stream是支持并发操作的，为了避免竞争，对于reduce线程都会有独立的result，combiner的作用在于合并每个线程的result得到最终结果。这也说明了了第三个函数参数的数据类型必须为返回数据类型了

#### 8. 整合操作

其实java的所有惰性求值都可以不停的第迭代的, 比如想下面这样

```java
Set<String> origins = album.getMusicians()
        .filter(artist -> artist.getName().startsWith("The"))
        .map(artist -> artist.getNationality())
        .collect(toSet());
```