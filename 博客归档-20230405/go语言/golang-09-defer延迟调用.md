golang 中的defer 非常灵活， 用来替代类似java 中的try--catch

> Go语言中的defer有一些不同的特点及灵活性，包括程序中可以有多个defer、defer的调用可以存在于函数的任何位置等。defer可能不会被执行，例如，如果判断条件不成立则放置在if语句中的defer可能不会被执行。defer语句在使用时有许多陷阱，Go语言中defer的实现方式也经历了多次演进

# golang defer 使用优势

## 1. 用于资源释放

defer一般用于资源的释放和异常的捕获，作为Go语言的特性之一，defer给Go代码的书写方式带来了很大的变化。下面的CopyFile函数用于将文件srcName的内容复制到文件dstName中。

```golang
func TestNoDefer(dstName, srcName string) {
	src, err := os.Open(srcName)
	if err != nil {
		return
	}
	dst, err := os.Create(dstName)
	if err != nil {
		// dst 报错手动关闭 src
		src.Close()
		return
	}
	written, err := io.Copy(dst, src)
	if err != nil {
		// copy 失败， 全部手动关闭
		dst.Close()
		src.Close()
		return
	}
	fmt.Printf("written num , %d", written)
	dst.Close()
	src.Close()
	return
}
```

> 如果不使用defer 则需要在每一个需要关闭的地方增加逻辑， 非常复杂

- 使用defer优化， 规范写法

```golang
func TestDefer(dstName, srcName string) {
	src, err := os.Open(srcName)
	if err != nil {
		return
	}
	defer func(src *os.File) {
		err := src.Close()
		if err != nil {
			fmt.Printf("src close err : %+v", err)
		}
	}(src)
	dst, err := os.Create(dstName)
	if err != nil {
		return
	}
	defer func(dst *os.File) {
		err := dst.Close()
		if err != nil {
			fmt.Printf("dst close err : %+v", err)
		}
	}(dst)
	written, err := io.Copy(dst, src)
	if err != nil {
		return
	}
	fmt.Printf("written num , %d", written)
	return
}
```

## 2. panic 异常捕获

defer的特性是无论后续函数的执行路径如何以及是否发生了panic，在函数结束后一定会得到执行，这为异常捕获提供了很好的时机。异常捕获通常结合recover函数一起使用

```golang
func TestPanic() {
	defer func() {
		// 使用 recover 拦截错误信息
		if errMsg := recover(); errMsg != nil {
			fmt.Println(errMsg)
		}
		fmt.Println("This is recovery function ... ")
	}()
	panic("This is Panic Situation")
}
```

## 3. 延迟执行

比如加锁延迟执行

```golang
l.lock()
defer l.unlock()
```

## 4. 参数预执行

```golang
func TestNDefer() {
	a := 1
	defer func(b int) {
		fmt.Println(b) //输出2
	}(a + 1)
	a = 99
}
```

> 如上例所示，defer后的函数需要传递int参数，首先将a赋值为1，接着defer函数的参数传递为a+1，最后，在函数返回前a被赋值为99。那么最后defer函数打印出的b值是多少呢？答案是2。原因是传递到defer的参数是预执行的，因此在执行到defer语句时，执行了a+1并将其保留了起来，直到函数执行完成后才执行defer函数体内的语句

## 4. 多个 defer 后入先出运行

```golang
func LIFORun() {
	for i := 1; i <= 4; i++ {
		// 输出 4 3 2 1
		defer fmt.Printf("%d ", i)
	}
}
```

## 5. defer 配合返回值

```golang
func main() {
	iCase1 := ReturnDeferCase1()
	fmt.Printf("case1 - i: %d, g : %d\n", iCase1, gCase1)
	iCase2 := ReturnDeferCase2()
	fmt.Printf("case2 - i: %d, g : %d\n", iCase2, gCase2)
	iCase3 := ReturnDeferCase3()
	fmt.Printf("case3 - i: %d, g : %d\n", iCase3, gCase3)
}

var gCase1 = 100

// 执行逻辑 先将 gCase1 = 100的值附在r 上， defer gCase1值变成 200 ， r作为返回值返回
func ReturnDeferCase1() (r int) {
	defer func() {
		gCase1 = 200
	}()
	return gCase1
}

var gCase2 = 100

// 执行逻辑 先将 gCase2 = 100的值附在r 上， r值 变成0 ， r值付给默认的返回值变量X ，defer r值 变成200，x作为返回值返回
func ReturnDeferCase2() int {
	r := gCase2
	defer func() {
		r = 200
	}()
	r = 0
	return r
}

var gCase3 = 100
// 执行逻辑 先将 gCase2 = 100的值附在r 上， r值 变成0  ，defer r值 变成200，r作为返回值返回
func ReturnDeferCase3() (r int) {
	r = gCase3
	defer func() {
		r = 200
	}()
	r = 0
	return r
}
```
输出

```
case1 - i: 100, g : 200
case2 - i: 0, g : 100
case3 - i: 200, g : 100
```

解释这个其实涉及到一个栈执行逻辑的问题

golang 栈的变量和返回值之间的执行逻辑如下

- 将返回值保存在栈上→执行defer函数→函数返回

> 但是要注意golang 返回之有变量的这种情况 , 如果返回值没有变量名称， 那么golang在返回的会生成一个默认变量来代表返回值的变量名称 ， 这个特性的差异导致了case 2 和case 3 返回值的不同

# defer 底层原理 todo