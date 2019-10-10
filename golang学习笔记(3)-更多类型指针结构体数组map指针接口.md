# 指针

Go 拥有指针。指针保存了值的内存地址。

类型 *T 是指向 T 类型值的指针。其零值为 nil。
```golang
var p *int
```
& 操作符会生成一个指向其操作数的指针。

```golang
i := 42
p = &i
```
* 操作符表示指针指向的底层值。

```golang
fmt.Println(*p) // 通过指针 p 读取 i
*p = 21         // 通过指针 p 设置 i
```

这也就是通常所说的“间接引用”或“重定向”。
与 C 不同，Go 没有指针运算。

# 结构体

## 结构体基本使用

```golang
//定义结构体
type Vertex struct {
	X int
	Y int
}
//使用.符号使用结构体
func main() {
	v := Vertex{1, 2}
	v.X = 4
	fmt.Println(v.X)
}
```

## 结构体指针

```golang
type Vertex struct {
	X int
	Y int
}

func main() {
	v := Vertex{1, 2}
	p := &v
	p.X = 1e9
	fmt.Println(v)
}
```

如果我们有一个指向结构体的指针 p，那么可以通过 (*p).X 来访问其字段 X。不过这么写太啰嗦了，所以语言也允许我们使用隐式间接引用，直接写 p.X 就可以。

## 结构体声明方法

```golang
type Vertex struct {
	X, Y int
}

var (
	v1 = Vertex{1, 2}  // 创建一个 Vertex 类型的结构体
	v2 = Vertex{X: 1}  // Y:0 被隐式地赋予
	v3 = Vertex{}      // X:0 Y:0
	p  = &Vertex{1, 2} // 创建一个 *Vertex 类型的结构体（指针）
)
func main() {
	fmt.Println(v1, p, v2, v3)
}
```

1. 顺序赋值
2. 指定赋值
3. 默认赋值
4. 快速指针


## 结构体默认方法

golang的结构体支持默认支持的方法，用来表示对象

```golang
type Vertex struct {
	X, Y float64
}
func (v Vertex) Abs() float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}
func main() {
	v := Vertex{3, 4}
	fmt.Println(v.Abs())
}
```

注意这种方法是只读的，修改将不会生效，如果需要修改需要使用指针接收方法

```golang
type Vertex struct {
	X, Y float64
}
func (v Vertex) Abs() float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}
func (v *Vertex) Scale(f float64) {
	v.X = v.X * f
	v.Y = v.Y * f
}
func main() {
	v := Vertex{3, 4}
	v.Scale(10)
	fmt.Println(v.Abs())
}
```

使用指针接收者的原因有二：
首先，方法能够修改其接收者指向的值。
其次，这样可以避免在每次调用方法时复制该值。若值的类型为大型结构体时，这样做会更加高效。

# 数组

```golang
func main() {
	var a [2]string
	a[0] = "Hello"
	a[1] = "World"
	fmt.Println(a[0], a[1])
	fmt.Println(a)

	primes := [6]int{2, 3, 5, 7, 11, 13}
	fmt.Println(primes)
}
```

# 数组切片

```golang
func main() {
	primes := [6]int{2, 3, 5, 7, 11, 13}

	var s []int = primes[1:4]
    fmt.Println(s)
    
    //生成结构体数组
    P := []struct {
		i int
		b bool
	}{
		{2, true},
		{3, false},
		{5, true},
		{7, true},
		{11, false},
		{13, true},
	}
}
```
注意是 [start:end) 这种方法是前开后闭的

注意切片其实是引用切片，数据修改会共享

注意:如果没有写数字将会以数组长度来衡量

以下切片是等价的：
```golang
a[0:10]
a[:10]
a[0:]
a[:]
```

# 切片的长度与容量
切片拥有 长度 和 容量。

切片的长度就是它所包含的元素个数。

切片的容量是从它的第一个元素开始数，到其底层数组元素末尾的个数。

切片 s 的长度和容量可通过表达式 len(s) 和 cap(s) 来获取。

你可以通过重新切片来扩展一个切片，给它提供足够的容量。这样会形成一个窗口来审视原来的数组

```golang
func main() {
	s := []int{2, 3, 5, 7, 11, 13}
	printSlice(s)
	// 截取切片使其长度为 0
	s = s[:0]
	printSlice(s)
	// 拓展其长度
	s = s[:4]
	printSlice(s)
	// 舍弃前两个值
	s = s[2:]
	printSlice(s)
}
func printSlice(s []int) {
	fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)
}
```
注意：切片的零值是 nil

# 动态创建数组或者切片

```golang
b := make([]int, 0, 5) // len(b)=0, cap(b)=5

func main() {
	a := make([]int, 5)
	printSlice("a", a)
	b := make([]int, 0, 5)
	printSlice("b", b)
	c := b[:2]
	printSlice("c", c)
	d := c[2:5]
	printSlice("d", d)
}
```
# 切片追加数据

```golang
func append(s []T, vs ...T) []T
```

append 的第一个参数 s 是一个元素类型为 T 的切片，其余类型为 T 的值将会追加到该切片的末尾。

append 的结果是一个包含原切片所有元素加上新添加元素的切片。

当 s 的底层数组太小，不足以容纳所有给定的值时，它就会分配一个更大的数组。返回的切片会指向这个新分配的数组。

## for 循环迭代

for 循环的 range 形式可遍历切片或映射。

当使用 for 循环遍历切片时，每次迭代都会返回两个值。第一个值为当前元素的下标，第二个值为该下标所对应元素的一份副本

```golang
func main() {
	for i, v := range pow {
		fmt.Printf("2**%d = %d\n", i, v)
	}
}
```


可以将下标或值赋予 _ 来忽略它。

```golang
for i, _ := range pow
for _, value := range pow
```

若你只需要索引，忽略第二个变量即可。

```golang
for i := range pow
```

# map

map 使用make 方法生成，两个参数 类型和值

```golang
type Vertex struct {
	Lat, Long float64
}

var m map[string]Vertex

func main() {
	m = make(map[string]Vertex)
	m["Bell Labs"] = Vertex{
		40.68433, -74.39967,
	}
	fmt.Println(m["Bell Labs"])
}
```

golang支持初始化映射语法

映射的文法与结构体相似，不过必须有键名。

```golang
type Vertex struct {
	Lat, Long float64
}

var m = map[string]Vertex{
	"Bell Labs": Vertex{
		40.68433, -74.39967,
	},
	"Google": Vertex{
		37.42202, -122.08408,
	},
}

func main() {
	fmt.Println(m)
}
```

若顶级类型只是一个类型名，你可以在文法的元素中省略它。

```golang
type Vertex struct {
	Lat, Long float64
}
var m = map[string]Vertex{
	"Bell Labs": {40.68433, -74.39967},
	"Google":    {37.42202, -122.08408},
}
func main() {
	fmt.Println(m)
}
```

在映射 m 中插入或修改元素：
```golang
m[key] = elem
```

获取元素：

```golang
elem = m[key]
```

删除元素：

```golang
delete(m, key)
```

通过双赋值检测某个键是否存在：

```golang
elem, ok = m[key]
```

若 key 在 m 中，ok 为 true ；否则，ok 为 false。
若 key 不在映射中，那么 elem 是该映射元素类型的零值。
同样的，当从映射中读取某个不存在的键时，结果是映射的元素类型的零值。
注 ：若 elem 或 ok 还未声明，你可以使用短变量声明：

```golang
elem, ok := m[key]
```

# 函数值传参

golang中函数也是顶级的变量

它们可以像其它值一样传递。可以用作函数的参数或返回值。

```golang
func compute(fn func(float64, float64) float64) float64 {
	return fn(3, 4)
}

func main() {
	hypot := func(x, y float64) float64 {
		return math.Sqrt(x*x + y*y)
	}
	fmt.Println(hypot(5, 12))

	fmt.Println(compute(hypot))
	fmt.Println(compute(math.Pow))
}
```

# 函数闭包

```golang
func adder() func(int) int {
	sum := 0
	return func(x int) int {
		sum += x
		return sum
	}
}
func main() {
	pos, neg := adder(), adder()
	for i := 0; i < 10; i++ {
		fmt.Println(
			pos(i),
			neg(-2*i),
		)
	}
}
```

# 函数多态

golang支持定义多个函数，每个函数要保证方法签名不同，名称可以相同

# 接口

```golang
type Abser interface {
	Abs() float64
}
func main() {
	var a Abser
	f := MyFloat(-math.Sqrt2)
	v := Vertex{3, 4}
	a = f  // a MyFloat 实现了 Abser
	a = &v // a *Vertex 实现了 Abser

	// 下面一行，v 是一个 Vertex（而不是 *Vertex）
	// 所以没有实现 Abser。
	a = v

	fmt.Println(a.Abs())
}
type MyFloat float64
func (f MyFloat) Abs() float64 {
	if f < 0 {
		return float64(-f)
	}
	return float64(f)
}
type Vertex struct {
	X, Y float64
}
func (v *Vertex) Abs() float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}
```

其实 goalng的接口编程是针对类型方法来说的，比如使用golang的前缀函数声明绑定使用对象

```golang
func (T type) methodName(param type) return_type{
	xxxxx
}
```

golang的这种设计其实更像一种声明，这种声明是全局通用的，也就是说如果用接口声明了一种类型那么只要实现了相同的方法就可以重用了，golang支持方法重载所以这种方法其实更能提高通用性

注意：golang在这里又限制了一个条件就是，在全局环境中同一个包名中不能有相同的方法接口声明

-----

# 引申 ： golang的type关键字

Golang语言中存在一个关键字type，type又有两种使用方式，一种是类型别名，一种是类型定义

类型定义

```golang
type Student struct {
  name String
  age int
}
```

```golang
type I int
类型别名
type Sdt = Student
type I = int
```

# golang 接口可以做变量传参，注意如果接口指向的一定是一个指针，因为他不可能需要复制的

```golang
import (
	"fmt"
	"math"
)
type I interface {
	M()
}
type T struct {
	S string
}
func (t *T) M() {
	fmt.Println(t.S)
}
type F float64
func (f F) M() {
	fmt.Println(f)
}
func main() {
	var i I
	i = &T{"Hello"}
	describe(i)
	i.M()
	i = F(math.Pi)
	describe(i)
	i.M()
}
func describe(i I) {
	fmt.Printf("(%v, %T)\n", i, i)
}
```

# 如果接口被null 调用了

如果接口被null 调用了，golang不会报错，而是继续以nil为入参运行，比如下面的例子，将会输出 nil

```golang
type I interface {
	M()
}
type T struct {
	S string
}
func (t *T) M() {
	if t == nil {
		fmt.Println("<nil>")
		return
	}
	fmt.Println(t.S)
}
func main() {
	var i I
	var t *T
	i = t
	i.M()
}
```

注意:如果接口没有找到对应的函数，将会报错

```golang
type I interface {
	M()
}
func main() {
	var i I
	describe(i)
	i.M()
}
func describe(i I) {
	fmt.Printf("(%v, %T)\n", i, i)
}
```

# 空接口

指定了零个方法的接口值被称为 *空接口：*

interface{}
空接口可保存任何类型的值。（因为每个类型都至少实现了零个方法。）

空接口被用来处理未知类型的值。例如，fmt.Print 可接受类型为 interface{} 的任意数量的参数。

# 空接口承载接口类型判断类型断言
类型断言 提供了访问接口值底层具体值的方式。

```golang
t := i.(T)
```

该语句断言接口值 i 保存了具体类型 T，并将其底层类型为 T 的值赋予变量 t。
若 i 并未保存 T 类型的值，该语句就会触发一个恐慌。
为了 判断 一个接口值是否保存了一个特定的类型，类型断言可返回两个值：其底层值以及一个报告断言是否成功的布尔值。
```golang
t, ok := i.(T)
```

若 i 保存了一个 T，那么 t 将会是其底层值，而 ok 为 true。
否则，ok 将为 false 而 t 将为 T 类型的零值，程序并不会产生恐慌。
请注意这种语法和读取一个映射时的相同之处。

# 上面的问题的简化版

类型选择
类型选择 是一种按顺序从几个类型断言中选择分支的结构。

类型选择与一般的 switch 语句相似，不过类型选择中的 case 为类型（而非值）， 它们针对给定接口值所存储的值的类型进行比较。

```golang
switch v := i.(type) {
case T:
    // v 的类型为 T
case S:
    // v 的类型为 S
default:
    // 没有匹配，v 与 i 的类型相同
}
```
类型选择中的声明与类型断言 i.(T) 的语法相同，只是具体类型 T 被替换成了关键字 type。

此选择语句判断接口值 i 保存的值类型是 T 还是 S。在 T 或 S 的情况下，变量 v 会分别按 T 或 S 类型保存 i 拥有的值。在默认（即没有匹配）的情况下，变量 v 与 i 的接口类型和值相同。

```golang
func do(i interface{}) {
	switch v := i.(type) {
	case int:
		fmt.Printf("Twice %v is %v\n", v, v*2)
	case string:
		fmt.Printf("%q is %v bytes long\n", v, len(v))
	default:
		fmt.Printf("I don't know about type %T!\n", v)
	}
}

func main() {
	do(21)
	do("hello")
	do(true)
}
```

# 特殊接口Error

golang有一个特殊的接口表示错误Error ，其实没啥鸟用。。。。

```golang
package main

import (
	"fmt"
	"time"
)

type MyError struct {
	When time.Time
	What string
}

func (e *MyError) Error() string {
	return fmt.Sprintf("at %v, %s",
		e.When, e.What)
}

func run() error {
	return &MyError{
		time.Now(),
		"it didn't work",
	}
}

func main() {
	if err := run(); err != nil {
		fmt.Println(err)
	}
}

```