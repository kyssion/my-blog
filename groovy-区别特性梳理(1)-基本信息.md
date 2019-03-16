## groovy相比较java的特殊的字符串操作

1. $ 引用当前作用域中的变量名称,这种方法叫插值

groovy中可以使用${xxx sxx}或者 $xxx 来直接在字符串中拼接信息

```groovy
def name = "item"
def name2 = "name is ${item}"
def name3 = "name is $item"
```

groovy 插值方法还有两种特殊用法

> 表达式使用方法

```groovy
${->1+2*10}//插入一个表达式
```

```groovy
"charu*${w->w<<"dddd"}" //这里的w就是charu*
```

> 注意: 如果<<后面是字符串的时候,将表示插入方法,如果是字符串就是位移逻辑

2. 'x' ,"xx", '''xxxx''',/xxx/,四种字符串的区别

在很多编程语言中都有这个特性

- '' : 简单的一个字符串,在groovy中这个字符串不支持插值($)操作
- "" : '' 特性加上支持插值
-''' ''' : 保留格式,有些地方需要使用\ 来消除 '\n' 换行问题
-/xx/ : 特殊字符不需要转义(只有/需要使用\进行转义),正则表达式专用

3. 使用~ 或者=~快速创建正则表达匹配式

```groovy
def pattern = ~/foo/
```

通过~ 这个方法可以快速的创建java中的java.utilregex.pattern对象,注意这种方法=和~ 之间一定要有空格,否则会解释成~=操作运算符

```groovy
def text = "some text to matcher"
def Matcher = text =~ /txt/
```

引申: 匹配运算符（==~）是find运算符的一个小变体，它不返回Matcher一个布尔值，并且需要输入字符串的严格匹配

```groovy
def m = text ==~ /match/                                              
assert m instanceof Boolean                                       
if (m) {                                                          
    throw new RuntimeException("Should not reach that point!")
}
```

## groovy中相比较java特殊的变量名称操作

1. groovy中可以使用字符串变量来作为变量名称

```groovy
def map = [:]
map."item hhh *" = 1234
print(map."item hhh *")
```

## groovy相比较java特殊的对象操作

1. 空指针的安全保证

groovy中如果对象为空,可以使用?.的方法来消除异常

```groovy
def person = null
def item person?.name
println(item)// show null
```

2. 对象的getter和setter的不同之处

在groovy中如果设置了getter使用对象.xx的时候将会自动的调用getter方法,如果没有设置,将会直接使用这个变量
groovy还是支持使用对象.@xx方法来直接的调用对应的变量

```groovy
class User {
    public final name
    User(item){
        this.name= item
    }
    def getName() {
        "this name is $name"
    }
}
def user = new User("bod")
println(user.name)
println(user.@name)
```

注意其实本质上是groovy默认就为每一个参数声明了getter和setter方法罢了,我们可以不使用getxx而是直接使用对象.xxx来调用getter或者setter方法

3. 方法指针

这个算是一个高级特性了,通过这种方法,可以快速的拉取一个对象的方法引用,类似js,function也是变量

```groovy
class User {
    public final name
    User(item){
        this.name= item
    }

    def getName() {
        "this name is $name"
    }
}

def user1 = new User("tom")
def user2 = new User("jerry")

def user1getter = user1.&getName
def user2getter = user2.&getName

println(user1getter())
println(user2getter())
```

> 注意:groovy是引用了对应对象的方法

4. 对象属性聚合操作 *.

在groovy中可以使用*.操作将一个对象数组中的对象的某个属性聚合起来,表达式cars*.make相当于cars.collect{ it.make },区别是groovy的*,表达式可以使用null  

```groovy
class Make {
    String name
    List<Model> models
}
@Canonical
class Model {
    String name
}
def cars = [
    new Make(name: 'Peugeot',
             models: [new Model('408'), new Model('508')]),
    new Make(name: 'Renault',
             models: [new Model('Clio'), new Model('Captur')])
]
def makes = cars*.name
assert makes == ['Peugeot', 'Renault']

def models = cars*.models*.name
assert models == [['408', '508'], ['Clio', 'Captur']]
assert models.sum() == ['408', '508', 'Clio', 'Captur'] // flatten one level
assert models.flatten() == ['408', '508', 'Clio', 'Captur'] // flatten all levels (one in this case)  
```

5. 对象中的call用法

在groovy中,对象也可以抽象成一个函数,使用对象名()方法的时候,将会隐式的调用对象中的call方法

```groovy
class MyCallable {
    int call(int x) {
        2*x
    }
}

def mc = new MyCallable()
assert mc.call(2) == 4
assert mc(2) == 4
```


## groovy 相对比java 特殊的函数用法

1. 函数参数数组化映射

```groovy
int function(int x, int y, int z) {
    x*y+z
}

def args = [4,5,6]

assert function(*args) == 26 //
```

2. 函数参数map化映射

在groovy中使用map可以动态的指定相关的参数

```groovy
def foo(Map args) { "${args.name}: ${args.age}" }
foo(name: 'Marie', age: 1)//指定参数的名称和对应的信息

//支持命名空间混合
def foo(Map args, Integer number) { "${args.name}: ${args.age}, and the number is ${number}" }
foo(name: 'Marie', age: 1, 23)  
foo(23, name: 'Marie', age: 1) 
```

注意groovy支持map和其他类型参数混用的逻辑,只有一点需要注意,定义的函数,他的传参的第一个一定是map类型,否则必须显示的指定参数

```groovy
def foo(Integer number, Map args) { "${args.name}: ${args.age}, and the number is ${number}" }
foo(23, [name: 'Marie', age: 1])
```

3. def 返回值参数

groovy是弱类型编程语言,所以返回值支持def弱类型的返回值

## groovy 相对比java的特殊数组用法

1. groovy的快速添加数据

groovy提供了引用的方法,赖在第二个数组中应用另一个数组中的内容

```groovy
//针对arr
def items = [4,5]
def list = [1,2,3,*items,6]
assert list == [1,2,3,4,5,6]
//针对map
def m1 = [c:3, d:4]
def map = [a:1, b:2, *:m1]
assert map == [a:1, b:2, c:3, d:4]
```

2. 快速创建数组信息

通过这种方法可以快速的创建一个指定迭代规律的字符串

```groovy
def range = 0..5                                    
assert (0..5).collect() == [0, 1, 2, 3, 4, 5]
assert (0..<5).collect() == [0, 1, 2, 3, 4]
assert (0..5) instanceof List
assert (0..5).size() == 6
//同样的规则也可应用在字符串中
assert ('a'..'d').collect() == ['a','b','c','d']
```

3. 数组批量赋值

```groovy
def list = [0,1,2,3,4]
assert list[2] == 2
list[2] = 4
assert list[0..2] == [0,1,4]
list[0..2] = [6,6,6]
assert list == [6,6,6,3,4]
```

## groovy和java 在比较方法中的区别

1. == 和 equal的区别

在groovy中== 将会调用java中的equal 方法,如果要比较值是否相等,应该使用is方法


```groovy
def list1 = ['Groovy 1.8','Groovy 2.0','Groovy 2.3']
def list2 = ['Groovy 1.8','Groovy 2.0','Groovy 2.3']
assert list1 == list2 //false
assert !list1.is(list2) //true
```

2. compareTo快速创建方法

在groovy中可以使用<=>来替代compareTo

```groovy
assert (1 <=> 1) == 0
assert (1 <=> 2) == -1
assert (2 <=> 1) == 1
assert ('a' <=> 'z') == -1
```

## groovy 与java不用的运算符用法

1. 运算符重载

在groovy中只要事先指定函数的对象就能将函数对应的运算法运算方法集成到这个对象中

```groovy
class Bucket {
    int size
    Bucket(int size) { this.size = size }
    Bucket plus(Bucket other) {
        return new Bucket(this.size + other.size)
    }
}
```

```groovy
def b1 = new Bucket(4)
def b2 = new Bucket(11)
assert (b1 + b2).size == 15
```

运算符号对应的方法见下表

| Operator | Method        | Operator | Method                  |
|----------|---------------|----------|-------------------------|
| +        | a.plus(b)     | a[b]     | a.getAt(b)              |
| -        | a.minus(b)    | a[b] = c | a.putAt(b, c)           |
| *        | a.multiply(b) | a in b   | b.isCase(a)             |
| /        | a.div(b)      | <<       | a.leftShift(b)          |
| %        | a.mod(b)      | >>       | a.rightShift(b)         |
| **       | a.power(b)    | >>>      | a.rightShiftUnsigned(b) |
| \|       | a.or(b)       | ++       | a.next()                |
| &        | a.and(b)      | --       | a.previous()            |
| ^        | a.xor(b)      | +a       | a.positive()            |
| as       | a.asType(b)   | -a       | a.negative()            |
| a()      | a.call()      | ~a       | a.bitwiseNegate()       |