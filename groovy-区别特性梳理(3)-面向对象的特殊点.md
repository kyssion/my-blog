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

