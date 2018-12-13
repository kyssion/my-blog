### go 变量声明

第一种，指定变量类型，声明后若不赋值，使用默认值。
```go
var v_name v_type
```
第二种，根据值自行判定变量类型。
```go
var v_name = value
```
第三种，省略var, 注意 :=左侧的变量不应该是已经声明过的，否则会导致编译错误。
```go
v_name := value
// 例如
var a int = 10
var b = 10
c : = 10
```

###go多变量声明

```go
package main
var x, y int
var ( //这种只能出现在全局变量中，函数体内不支持
	a int
	b bool
)
var c, d int = 1, 2
var e, f = 123, "hello"//类型可以不同
//这种不带声明格式的只能在函数体中出现
//g, h := 123, "hello"
func main() {
	x = 123
	y = 22
	g, h := 123, "hello"
	println(x, y, a, b, c, d, e, f, g, h)
}
```
执行结果

```
0 0 0 false 1 2 123 hello 123 hello
```
注意：在多赋值的时候如果想要省略掉一个可以使用这种方法 _,b=12,333 ,_在go语言中有只读的作用，使用这个方法可以灵活的处理

### go 引用取值

```go
package main
func main() {
	var a = 123
	var b *int = &a
	
}
```
这里使用了地址操作符所以 b和a 其实是一个东西

> 注意 &符号的意思是对变量取地址，如：变量a的地址是&a ，* 符号的意思是对指针取值，如: *&a，就是a变量所在地址的值，当然也就是a的值了

