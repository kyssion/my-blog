
1.

golang 包导入语句支持多包导入

```
import ("fmt","math"))
```

约定 : golang中首字母大写的表示导出, 比如math包中的math.Pi

2. 
golang的函数 多参数,多返回值,和变量绑定

golang 返回多函数的可以实现解包

3. 
golang 的变量系统

```
var(
    变量名称 类型 = 值
)
```

强制装换,使用类型()进行强制装换

complex64 complex128 就是long


静态类型

const


循环 goalng 没有 () wiile 都用 for代替,其他的和java 相同    



if else 判断

1没有括号 2可以在之前执行一个语句,这个语句中的变量可以在整个if else 语法块中使用

switch 

struct 结构体

构造结构体对象的时候可以制定名称来指定的负值

```
type xxx type{
    a int
}

func main(){
    var p = xxx(a:123)
}

```

```
type xxx type{
    x int
    y int
}

func main(){
    p := xxx(123,123)
    q :=&p

}
```


golang 可以使用 new函数来构造一个新的结构体引用不过需要自己进行赋值

```
type Vertex struct {
	X, Y int
}

func main() {
	v := new(Vertex)
	fmt.Println(v)
	v.X, v.Y = 11, 9
	fmt.Println(v)
}
```


golang的数组和[] 放在类型的前面其他的和 java相同

切片的支持类似rust


golang支持make创建 arr map channel 三个参数分别表示 类型长度和容量, 初始化的时候如果长度不等0 将会默认的赋0

range 可以循环迭代 arr

```
var pow = []int{1, 2, 4, 8, 16, 32, 64, 128}

func main() {
	for i, v := range pow {
		fmt.Printf("2**%d = %d\n", i, v)
	}
}
```

golang 有一个切片生成多个数组的方法

```
	s := []struct {
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
```


数组有两个概念容量和长度
长度表示 数据的量
容量表示能容纳多少的量

nil是空指针

数组长度超过上限就需要实用append方法来增加元素

```
	for i, v := range pow {
		fmt.Printf("2**%d = %d\n", i, v)
	}
```

切片的循环迭代

可以实用 _ 来忽略
```
	for i := range pow {
		pow[i] = 1 << uint(i) // == 2**i
	}
	for _, value := range pow {
		fmt.Printf("%d\n", value)
	}
	```
map
```
package main

import "fmt"

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


如果知道类型既可以直接的省略掉他


在映射 m 中插入或修改元素：

m[key] = elem
获取元素：

elem = m[key]
删除元素：

delete(m, key)
通过双赋值检测某个键是否存在：

elem, ok = m[key]
若 key 在 m 中，ok 为 true ；否则，ok 为 false。

若 key 不在映射中，那么 elem 是该映射元素类型的零值。

同样的，当从映射中读取某个不存在的键时，结果是映射的元素类型的零值。


golang支持闭包, 闭包的所有变量的值都是共享的

