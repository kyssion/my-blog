## groovy 变量可见性和javabean相比较java的不同点

groovy如果没有定义可见性(public private),默认使用public

groovy 不提供getter和setter

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

## groovy集成登

groovy的继承和java的非常类似,都拥有private protected public 关键字,都有interface abstract 关键字,并且语义相同


Groovy接口不支持Java 8接口等默认实现。但是groovy提供了一个特殊的东西叫做Traits,特征

## groovy对象new

1. groovy既然是脚本语言所以在构建一个新的对象的时候也相当灵活,groovy提供了如下的几种方法来创建对象

```groovy
class PersonConstructor {
    String name
    Integer age
    PersonConstructor(name, age) {
        this.name = name
        this.age = age
    }
}
def person1 = new PersonConstructor('Marie', 1)
def person2 = ['Marie', 2] as PersonConstructor
PersonConstructor person3 = ['Marie', 3]
```

- 传统的java创建方法
- 使用as指定创建的对象类型
- 直接定义创建的类型,进行强制转换

2. 如果没有提供构造参数,groovy还提供了参数映射来动态的初始化对应的字段信息

```groovy
class PersonWOConstructor {                                  
    String name
    Integer age
}
def person4 = new PersonWOConstructor()
def person5 = new PersonWOConstructor(name: 'Marie')
def person6 = new PersonWOConstructor(age: 1)
def person7 = new PersonWOConstructor(name: 'Marie', age: 2)
```

注意: 这种方案传递的参数是一个map类型,名称和对象中的变量一一对应