# 1. 浮点数陷阱

```golang
var f1 float64 = 0.3
var f2 float64 = 0.6
fmt.Println(f1 + f2)
```
> 这种情况输出的是0.99999 而不是0.9 ， 这个其实是IEEE 标准的现实的陷阱

# 2. 浮点数和定点数

INF -INF 分别描述最大值和最小值

golang 中简单的精度处理 ： 使用strconv 处理

```golang
func TestP() {
	var f1 float64 = 1.4
	var f2 float64 = 0.9
	//printed by the 'e', 'E', 'f', 'g', 'G', 'x', and 'X' formats.
	fmt.Println(f1 - f2)
	fmt.Println(strconv.FormatFloat(f1-f2, 'e', 2, 64))
	fmt.Println(strconv.FormatFloat(f1-f2, 'E', 2, 64))
	fmt.Println(strconv.FormatFloat(f1-f2, 'f', 2, 64))
	fmt.Println(strconv.FormatFloat(f1-f2, 'g', 2, 64))
	fmt.Println(strconv.FormatFloat(f1-f2, 'G', 2, 64))
	fmt.Println(strconv.FormatFloat(f1-f2, 'x', 2, 64))
	fmt.Println(strconv.FormatFloat(f1-f2, 'X', 2, 64))
	var f3, err = strconv.ParseFloat(strconv.FormatFloat(f1-f2, 'f', 2, 64), 64)
	fmt.Println(f3)
	fmt.Println(err)
}
```

输出结果

```
0.4999999999999999
5.00e-01
5.00E-01
0.50
0.5
0.5
0x1.00p-01
0X1.00P-01
0.5
<nil>
```

## golang 大数

math.big

golang big标准库提供了3中数据类型 ： big.Int big.Float big.Rat

1. big.Int 核心思想是使用uint切片来存储大整数  , go 大整数乘法用了 karatsuba算法（todo）执行时候使用了汇编代码
2. big.Float golang 实现原理简单粗暴 ， 小数先转成整数 ， 然后处理 ， 注意这么做同样有精度问题 。 因为有限位数无法表达无限小数，但是可以通过prec存储数字的位数来提高精度
3. big.Rat 分数运算 -  会进行一些优化， 尽量避免精度问题， 比如 1/2+2/3 会变成 (1×3+2×3)/2×3 这样


```golang
func TestQ() {
	var i1, _ = new(big.Int).SetString("9999999999999999999999999", 10)
	var i2, _ = new(big.Int).SetString("10000000000000000000000000000000", 10)
	// i1 + i2 结果值写入i1 并且返回 i1 的副本 i3
	var i3 = i1.Add(i1, i2)
	fmt.Println(i1)
	fmt.Println(i3)

	// 浮点数运算 prec 描述精度位置 ,
	var f1 = big.NewFloat(1.4).SetPrec(1000)
	var f2 = big.NewFloat(0.9).SetPrec(1000)
	var f3 = f1.Sub(f1, f2)
	// 0.49999999999999988897769753748434595763683319091796875 还是会有精度问题
	fmt.Println(f3)

	// 分数运算
	var d1 = big.NewRat(1, 2)
	var d2 = big.NewRat(2, 3)
	var d3 = d1.Add(d1, d2)
	// 7/6
	fmt.Println(d3)
	// 1.1666666666666667 false
	fmt.Println(d3.Float64())
}
```
# 类型转化

golang 内置了几个类型转化的函数

```golang
strconv 系列函数
```