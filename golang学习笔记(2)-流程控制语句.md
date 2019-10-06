# for

```golang
func main() {
	sum := 0
	for i := 0; i < 10; i++ {
		sum += i
	}
	fmt.Println(sum)
}
```

简单来书就是没有花阔化的for循环

```golang
func main() {
    sum := 1
    //while
	for sum < 1000 {
		sum += sum
	}
    //死循环
    for{

    }
}
```

golang用 for 来代替while循环和死循环

```golang
func main() {
	for i, v := range pow {
		fmt.Printf("2**%d = %d\n", i, v)
	}
}
```
for 循环的 range 形式可遍历切片或映射。

当使用 for 循环遍历切片时，每次迭代都会返回两个值。第一个值为当前元素的下标，第二个值为该下标所对应元素的一份副本。
# if else

```golang

没有括号的if 但是有函数式编程语言的样子，在判断逻辑前执行一

func pow(x, n, lim float64) float64 {
	if v := math.Pow(x, n); v < lim {
		return v
	}
	return lim
}
```

# swich

golang的switch 没有break ，而且所有可以使用= 号进行判断的都可以放入其中

```golang
func main() {
	fmt.Print("Go runs on ")
	switch os := runtime.GOOS; os {
	case "darwin":
		fmt.Println("OS X.")
	case "linux":
		fmt.Println("Linux.")
	default:
		// freebsd, openbsd,
		// plan9, windows...
		fmt.Printf("%s.\n", os)
	}
}
```

注意没有条件的swich

没有条件的 switch 同 switch true 一样。
这种形式能将一长串 if-then-else 写得更加清晰。

# defer

defer 语句会将函数推迟到外层函数返回之后执行。
推迟调用的函数其参数会立即求值，但直到外层函数返回前该函数都不会被调用。

```golang
func main() {
	defer fmt.Println("world")
	fmt.Println("hello")
}
```

注意：推迟的函数调用会被压入一个栈中。当外层函数返回时，被推迟的函数会按照后进先出的顺序调用

```golang
func main() {
	fmt.Println("counting")

	for i := 0; i < 10; i++ {
		defer fmt.Println(i)
	}

	fmt.Println("done")
}
```