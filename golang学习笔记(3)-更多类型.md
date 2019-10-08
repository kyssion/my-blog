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

# for 循环迭代

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

