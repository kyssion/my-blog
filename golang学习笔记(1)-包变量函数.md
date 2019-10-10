golang的包管理和变量管理都是非常容易的

# golang 包

golang在使用的时候可以通过import 关键字引入包

其他的包在定义的时候可以使用package 来定义一个包

注意 main包是一个特殊的包，这个包表示golang执行的入口

```golang
package main

import "golang-study/test"
func main()  {
	test.IsTest()
}
```

这里其实有一个小坑，就是golang的代码开发目录必须是是GOPATH环境变量下的src目录中，不然引用包的时候找不到代码

注意 在全局环境中同一个包名中不能有相同的方法接口声明 ， 除了main包，其他的包名称必须和他的上层文件夹的名称一致

# goang 函数定义

```golang
func test(a string) （int,string){
    return (123,"sdfsdf");
}

func main(){
    a,b := test("sdfsdf");
}
```

1. golang的参数类型是放在后面的
2. golang的返回值是int类型
3. 注意如果这个方法是可以导出的首字母要大写
4. golang 支持多个返回值,使用的是反解包模式

```golang
func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}
func main() {
	fmt.Println(split(17))
}
```

golang还支持命名返回直接使用返回的变量作为返回值

# golang 变量

声明方法

```golang
// 简单声明
var c, python, java bool
func main() {
	var i int
	fmt.Println(i, c, python, java)
}

//初始化声明
var i, j int = 1, 2
func main() {
	var c, python, java = true, false, "no!"
	fmt.Println(i, j, c, python, java)
}

//类型补充声明
func main(){
    k := 3
}
```

golang基本类型

```
bool
string
int  int8  int16  int32  int64
uint uint8 uint16 uint32 uint64 uintptr
byte // uint8 的别名
rune // int32 的别名
    // 表示一个 Unicode 码点
float32 float64
complex64 complex128
```

# golang 初始化值

没有明确初始值的变量声明会被赋予它们的 零值。

零值是：

- 数值类型为 0，
- 布尔类型为 false，
- 字符串为 ""（空字符串）。

# 类型强制转化方法

golang使用变量名称+() 强制转化

```golang
var i int = 42
var f float64 = float64(i)
var u uint = uint(f)

i := 42
f := float64(i)
u := uint(f)
```

# 常量

```golang
const Pi = 3.14
func main() {
	const World = "世界"
	fmt.Println("Hello", World)
	fmt.Println("Happy", Pi, "Day")

	const Truth = true
	fmt.Println("Go rules?", Truth)
}
```

注意

- 常量的声明与变量类似，只不过是使用 const 关键字。
- 常量可以是字符、字符串、布尔值或数值。
- 常量不能用 := 语法声明。也不用带上类型



