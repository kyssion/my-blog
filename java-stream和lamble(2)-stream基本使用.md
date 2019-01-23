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

#### 2.1 mapToLong mapToInt mapToDouble

这三个方法是java 的stream 针对java对基本类型的自动装箱和自动拆箱的优化

传入的参数拿 Long类型举例

ToLongFunction -> 实现对象到long 类型的转换

这些方法将会返回一下特殊的stream 比如LongStream等等

而这种stream针对不同的输出,拥有不同的适配方法

比如long转double会有 LongToDoubleFunction接口
比如long转Long 对象 会有 LongFunction接口
而这种stream 实现的map接口是LongUnaryOperator,通过这种方法实现性能上的高效


> ****引申 java在针对数字统计的时候,有意识的提供了额外的方法来统计数据->summaryStatistics 方法,这个方法能计算出各种各样的统计值， 如 IntStream 对象内所有元素中的最小值、 最大值、 平均值以及数值总和,例子如下

```java
public static void printTrackLengthStatistics(Album album) {
    IntSummaryStatistics trackLengthStats
            = album.getTracks()
            .mapToInt(track -> track.getLength())
            .summaryStatistics();
    System.out.printf("Max: %d, Min: %d, Ave: %f, Sum: %d",
            trackLengthStats.getMax(),
            trackLengthStats.getMin(),
            trackLengthStats.getAverage(),
            trackLengthStats.getSum());
}
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

#### 8. 流式迭代操作

其实java的所有惰性求值都可以不停的第迭代(流式操作)))的, 比如想下面这样

```java
Set<String> origins = album.getMusicians()
        .filter(artist -> artist.getName().startsWith("The"))
        .map(artist -> artist.getNationality())
        .collect(toSet());
```

#### 9. foreach 迭代

一个基本的java 迭代操作像如下的形式

```java
for(Integer i : list){
    System.out.println(i);
}
```
使用foreach 改造成函数式编程变成如下的形式

```java
list.stream().forEach((i)-> System.out.println(i));
```

### 10. sorted

排序方法,和list的集合sort一样 惰性求值方法

### 11. unordered

unordered操作不会进行任何显式的打乱流的操作。它的工作是：消除流中必须保持的有序约束，因此允许之后的操作使用 不必考虑有序的优化。

### 12. 针对map的新操作

```java
map.compute("string",(key,oldValue)-> "sdf");//如果map中没有这个值将会使用后面的函数进行计算
map.putIfAbsent("string", "defaule"); // 如果map没有值，将会用后面的值替代它
map.computeIfAbsent("string",(i)->i+"sdf"); // 如果map中没有这个值将会使用后面的函数进行计算 不过之传入value
map.computeIfPresent("string",(key,oldValue)-> key+oldValue); // 如果map中有值，将会使用后面的值替代相关的数量
```

### 一个高级例子

首先我们定义稍微复杂的对象,School 学校对象,Student 用户对象

```java
class School{
    private String schoolName;
    private String schoolAddress;
    private List<Student> students;
}
class Student{
    private String name;
    private String age;
    private List<Student> friends;
}
```

定义初始化方法allInit

```java
class JavaStreamUp{
    public void allInit(){
        List<School> schools = new ArrayList<>();
        School schoolUSA = new School("ONE", "USA");
        School schoolUK = new School("TOW", "UK");

        List<Student> studentsUSA = initStudent(schoolUSA);
        List<Student> studentsUK = initStudent(schoolUK);
        createFrient(studentsUSA,studentsUK);
        createFrient(studentsUK,studentsUSA);
        schools.add(schoolUK);
        schools.add(schoolUSA);
    }
    public void createFrient(List<Student> addF,List<Student> fStudent){
        for (Student student:addF){
            int item = (int) (Math.random()*fStudent.size());
            for(int i=0 ;i<item;i++){
                addF.add(student);
            }
        }
    }
    public List<Student>  initStudent(School schools){
        List<Student> students = new ArrayList<>();
        for (int item = 0; item < 10; item++) {
            Student student = new Student();
            student.setName("item_"+item);
            student.setAge(""+(item+1)*3);
            students.add(student);
        }
        return students;
    }
}
```

这里定义一个需求,找到这两个大学找出其中所有年纪大于14岁的所有学生的姓名和学校姓名

1. 最基本的遍历方法 (简单双层for循环遍历)

```java
public void functionBaseMethod(List<School> schools) {
    Set<String> studentSet = new HashSet<>();
    for (School school : schools) {
        for (Student student : school.getStudents()) {
            if (student.getAge() > 14) {
                studentSet.add(student.getName()+"|"+student.getSchoolName());
            }
        }
    }
    for (String student : studentSet) {
        System.out.println(student);
    }
}
```

2. foreach 处理迭代

```java
public void functionForEachMethod(List<School> schools) {
    Set<String> studentSet = new HashSet<>();
    schools.stream().forEach(item -> {
        item.getStudents().forEach(iii -> {
            if (iii.getAge() > 14) {
                studentSet.add(iii.getName()+"|"+iii.getSchoolName());
            }
        });
    });
    for (String student : studentSet) {
        System.out.println(student);
    }
}
```

3. 使用 filter过滤用户年龄使用 map 生成新的对象

```java
public void functionForFilterMap(List<School> schools){
    Set<String> stringSet = new HashSet<>();
    schools.stream().forEach(item->{
        item.getStudents().stream().filter(i->i.getAge()>14)
                .map(i-> i.getName()+"|"+i.getSchoolName())
                .forEach(i->stringSet.add(i));
    });
    for (String student : stringSet) {
        System.out.println(student);
    }
}
```

4. 进阶 使用flatmap 配合 collect(collection.toset())一次性生成

```java
Set<String> stringSet=schools.stream().flatMap(i->i.getStudents().stream())
        .filter(i->i.getAge()>14).map(i->i.getName()+"|"+i.getSchoolName()).collect(Collectors.toSet());
for (String student : stringSet) {
    System.out.println(student);
}
```

> 这里简单的原因是 flatMap整合了流,而collect 结合了list


### @FunctionalInterface 注解

其实看一下所有java 内置的函数化接口其实都使用了这个注解

该注解会强制 javac 检查一个接口是否符合函数接口的标准。如果该注释添加给一个枚举
类型、类或另一个注释，或者接口包含不止一个抽象方法，javac 就会报错。重构代码时，
使用它能很容易发现问题。

### java 收集器

java stream的收集器就是为了将数据整理成同一结构的工具

#### java 内部类库实现的部分收集器

> tolist toSet

```java
Collectors.toList();
Collectors.toSet();
```

以上两个式最简单的,就是将stream中的方法形成新的集合

------

> toCollection

```java
List<Integer> list = new ArrayList<>();
list.stream().collect(Collectors.toCollection(HashSet::new));
```

上面这个可以将 list 转化成stream方法定义接口的相同的集合实现自定义

比如stream是定义在collection接口上的,那个通过这个方法能实现list和set的相互转化

> ps 这个方法的实现建议仔细的研究一下

------

> minBy maxBy

```java
List<Integer> item = new ArrayList<>();
Optional<Integ> i = item.stream().collect(Collectors.minBy(Comparator.comparingInt((i)->i)));
Optional<Integ> i = item.stream().collect(Collectors.maxBy(Comparator.comparingInt((i)->i)));
```

这个方法将会把这个集合中制定参数最小的那个对象返回

-----

> averagingInt 平均数  summarizingInt 求合

```java
double item3 = item.stream().collect(Collectors.averagingInt((i)->{
    return i;
}));
item.stream().collect(Collectors.summarizingInt(Fox::getInteger));
```

这个方法可以获取这个integer数组的平均值

------

> partitioningBy 分组筛选

```java
Map<Boolean,List<Fox>> listMap=item.stream().collect(Collectors.partitioningBy((Fox::isNeed)));
Map<Boolean,List<Fox>> listMap2=item.stream().collect(Collectors.partitioningBy((i)->{
    return i.getInteger()+10>5;
}));
```

数据分组， 通过一个返回boolean类型的表达式从而实现两种返回值的特殊收集器

------

> java  字符串拼接方法

```java
String result = artists.stream().map(Artist::getName)
            .collect(Collectors.joining(", ", "[", "]"));
```

joining中的各种方法分别表示参数的分隔符，开始符号和结束符号

------

> groupingBy mapping 自定义分组

```java
Map<String,String> map=albums.collect(Collectors.groupingBy(Album::getStringItem,
            Collectors.mapping(Album::getName,Collectors.toList())));
```

这个方法是上面的扩展,函数将会传入两个参数，第一个函数是生成返回的key，第二个函数是生成value


例子中我们都用到了第二个收集器,用以收集最终结果的一个子集。这些收集器叫作下游收集器。收集器是生成最终结果的一剂配方,下游收集器则是生成部分结果的配方,主收集器中会用到下游收集器。这种组合使用收集器的方式,使得它们在 Stream 类库
中的作用更加强大。

那些为基本类型特殊定制的函数,如 averagingInt 、 summarizingLong 等,事实上和调用特殊 Stream 上的方法是等价的,加上它们是为了将它们当作下游收集器来使用的

------

> 其他的一些api

list转map -- 这个非常常用，Function.identity

```java
list.stream().collect(Collectors.toMap(MapItem::getName, Function.identity()));
```

#### 自定义java stream 收集器

有的时候java内置的组合器其实并不能真正的实现我们的需求，这个时候我们就需要自定义收集器来实现我们想要的东西

比如我们有这样的一个业务，存在如下的一种对象和对象的list集合，我们需要遍历的list集合，取出手有的name信息，整合成以"{"符合开头,"]"符号结尾,","符号分隔的字符串

```java
class Fox {
    private Integer integer;
    private String name;
    。。。getter and setter
}
```

> 方法1 传统遍历法

```java
public String userBase(List<Fox> list){
    StringBuilder stringBuilder =
            new StringBuilder();
    boolean isFirst = true;
    String index = null;
    for (Fox fox:list){
        index="{"+fox.getName()+"]";
        stringBuilder.append(isFirst?index :","+index);
        isFirst=false;
    }
    return stringBuilder.toString();
}
```

> 方法2 使用foreach遍历

```java
public String useForEach(List<Fox> list) {
    StringBuilder stringBuilder =
            new StringBuilder();
    list.stream().forEach((i) -> {
        if (stringBuilder.length() == 0) {
            stringBuilder.append("{" + i.getName() + "]");
        } else {
            stringBuilder.append(",{" + i.getName() + "]");
        }
    });
    return stringBuilder.toString();
}
```

> 方法3 发现是一种迭代模型使用reduce实现

```java
public String userStreamReduce(List<Fox> list){
    return list.stream().map(Fox::getName).reduce(new StringBuilder(),(x,y)->{
        if (x.length() == 0) {
            x.append("{").append(y).append("]");
        } else {
            x.append(",{").append(y).append("]");
        }
        return x;
    },(left,right)-> left.append(",").append(right)).toString();
}
```

> 方法4 实现Collector<T, A, R> 接口

首先说一下Collector<T, A, R>接口中的三个范型

- T 待收集元素的类型,这里是 String ;
- A 累加器的类型 StringCombiner ;
- R 最终结果的类型,这里依然是 String 。

几个重要的方法 

- supplier 初始化容器，其实也就是默认的值或者处理类
- accumulator 迭代方法
- combiner 双流合并方法
- finish 最终生成方法
- characteristics 一个优化用的列表

```java
class StringCollector implements Collector<String, StringBuilder, String> {
    @Override
    public Supplier<StringBuilder> supplier() {
        return StringBuilder::new;
    }

    @Override
    public BiConsumer<StringBuilder, String> accumulator() {
        return (before, now) -> {
            if (before.length() == 0) {
                before.append("{" + now + "]");
            } else {
                before.append(",{" + now + "]");
            }
        };
    }

    @Override
    public BinaryOperator<StringBuilder> combiner() {
        return (left, right) -> left.append(",").append(right);
    }

    @Override
    public Function<StringBuilder, String> finisher() {
        return StringBuilder::toString;
    }

    //这个方法使用来进行指数优化的
    @Override
    public Set<Characteristics> characteristics() {
        return new HashSet<>();
    }
}
```

定义好了自定义的collect之后就简单了，直接调用就可以了

```java
list.stream().map(Fox::getName).collect(new StringCollector());
```
