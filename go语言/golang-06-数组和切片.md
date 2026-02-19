# golang 数组声明的三种方法

```golang
var arr [3]int
var arr2 = [4]int{1,2,3,4}
arr3 := [...]int{1,2,3,4} // []int{1,2,3,4}-> 这个是切片
```

> printLn 使用 %T 打印数组类型

```golang
func TestS() {
	arr := []int{1, 2, 3, 4, 5, 6, 7, 8}
	fmt.Printf("%T\n%+v", arr, arr)
}
```
输出：
```
[]int
[1 2 3 4 5 6 7 8]
```

# golang 数组引用

```golang
func TestS() {
	arr1 := [...]int{1, 2, 3, 4, 5, 6, 7, 8}
	arr2 := arr1
	arr1[0] = 100
	arr2[0] = 99
	fmt.Printf("a:%p value:%+v\n", &arr1, arr1)
	fmt.Printf("b:%p value:%+v\n", &arr2, arr2)
	CopyArray(arr1)
	fmt.Printf("c|a:%p value:%+v\n", &arr1, arr1)
	fmt.Printf("c|b:%p value:%+v\n", &arr2, arr2)
}

func CopyArray(c [8]int) {
	c[0] = 98
	fmt.Printf("c:%p value:%+v\n", &c, c)
}
```
输出
```
a:0xc0004d20c0 value:[100 2 3 4 5 6 7 8]
b:0xc0004d2100 value:[99 2 3 4 5 6 7 8]
c:0xc0004d21c0 value:[98 2 3 4 5 6 7 8]
c|a:0xc0004d20c0 value:[100 2 3 4 5 6 7 8]
c|b:0xc0004d2100 value:[99 2 3 4 5 6 7 8]
```

> golang 数组赋值和函数引用都是


# golang 数组内部数据格式

```golang
type Array struct{
    Elem *Type
    Bound int64
}
```

# golang 切片

> 切片初始化方法

```golang
var slice1 []int
var slice2 = make([]int , 5)
var slice2 = make([]int , 5, 7) // 长度为5 容量为7 
numbers := []int{1,2,3,4,5}
```

```golang
func TestT() {
	arr := make([]int, 5, 7)
	fmt.Printf("arr -> len : %d,cap : %d", len(arr), cap(arr))
}
// 输出 ： arr -> len : 5,cap : 7
```

## golang 切片截取

```golang
func TestT() {
	arr := make([]int, 10, 20)
	fmt.Printf("arr -> len : %d,cap : %d\n", len(arr), cap(arr))
	arr1 := arr[1:2]
	fmt.Printf("arr1 -> len : %d,cap : %d", len(arr1), cap(arr1))
}
//输出
//arr -> len : 10,cap : 20
//arr1 -> len : 1,cap : 19
```

> golang 截取语法 ， [1:2], 从1 ->2 不包括2 ， 长度和容量都是按照原来的数组的容量和长度截断

# golang 切片类型的底层实现

```golang
type Slice struct{
	Elem *Type // element type
}
```
## golang make 初始化切片大小支持

golang 在初始化的时候会动态检测是分配到栈区中还是分配到堆区中 ， 默认大小是64 KB 可以在在编译期指定 smallframes 标识进行更新

so make([]int64 ,1023) 和 make([]int64,1024)细节上是截然不同的
## golang 复制

```golang
func TestU() {
	arr := []int{1, 2, 3, 4}
	var arrC [4]int
	// 前面表示复制进 , 后面表示复制出
	copy(arrC[2:], arr[3:])
	// 输出 : [0 0 4 0]
	fmt.Printf("%+v\n", arrC)
}
```

> 注意： 如果才用了协程调用的方法或者加入了 race检测， 就会运行 slicestringcopy或者slicecopy函数进行额外的检查， 默认使用的memmove 函数实现内存复制

> 引申： race 检测 -> go 工具链集成了 race 检测 ， 用于检测golang竞争的问题

```golang
go test -race mypkg
go run -race
go build -race
go install -race
```

## golang 切片扩容规则 

1. 如果新申请的容量大于原来的经容量的2倍，则使用新申请的容量
2. 如果接切片长度小于 1024 ， 则最终容量是就容量的2倍
3. 如果接切片长度大于或等于1024 ， 则从旧容量开始的1/4 循环增加直到大于等于新容量
4. 如果最终容量过大导致溢出， 则最终容量就是新申请的容量

