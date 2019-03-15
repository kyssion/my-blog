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

