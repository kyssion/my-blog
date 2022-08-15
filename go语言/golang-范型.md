# golang 范型类型声明

```golang
 // type TPatype TParam[T ~int | float64] T 不能声明基础类型， 没有意义
type Map1 [KEY int|string, VALUE string| float64] map[KEY]VALUE // 声明范型map
type Slice [T int|float64] []T // 声明范型切片
type Struct1 [T string|int|float64] struct {  Title string  Content  T} // 声明范型结构体

```
golang 增加了一个 [] 符号的语法， 里面可以增加我们的约束，这个约束中的信息是低类型 ， 向上兼容所有派生类型比如

```golang
type DDD int // 派生类型
```


# golang 初始化


```golang
type DDD int
type Map1[KEY int | string, VALUE string | float64] map[KEY]VALUE // 声明范型map
type Slice[T int | float64] []T                                   // 声明范型切片
type Struct1[T string | int | float64] struct {
	Title   string
	Content T
} // 声明范型结构体

func Test1(t *testing.T) {
	var d DDD = 123
	var P Slice[int] = []int{123, 223} // 还不支持诶性推导 - 这里需要直接生命变量
	var M Map1[string, string] = map[string]string{
		"t": "t",
	}
	var STR = Struct1[string]{
		Title:   "",
		Content: "",
	}

	d2 := DDD(123)             // 简写
	P2 := Slice[int]{222, 333} // 简写
	M2 := Map1[string, string]{
		"T": "t",
	}
	// 匿名结构体不支持
	fmt.Printf("%d , %v , %v ， %v\n", d, P, M, STR)
	fmt.Printf("%d , %v , %v ， %v\n", d2, P2, M2)
}
```

> 复杂的嵌套类型

```golang
type MyStruct[S int | string, P map[S]string] struct {
	Name    string
	Content S
	Job     P
}

func Test2(t *testing.T) {
	ppp := MyStruct[int, map[int]string]{
		Name:    "",
		Content: 12,
		Job: map[int]string{
			1: "123",
		},
	}
	fmt.Sprintf("%v", ppp)
}
```

> golang范型类型初始化方法和自定义类型初始化方法一样 ， 但是注意范型使用的时候要声明范型类型 ， golang暂时不提供推导能力


# 范型函数

> 约束类型 关键字

any -> 指定任意类型 
comparator -> 指实现了比较接口
interface 