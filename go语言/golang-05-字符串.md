# golang 中字符串的结构

```golang
// reflect 包中
type StringHeader struct {
	Data uintptr
	Len  int
}
```

- Data : 指向底层的字符数组
- Len : 只想底层数组的长度

在golang中使用 rune 来表示一个字符 - print 使用 %#U 输出真实编码

```golang
func TestR() {
	lt := "ab王"
	for index, runeItem := range lt {
		fmt.Printf("index : %d , rune : %d , unicode : %#U\n", index, runeItem, runeItem)
	}
}
```
输出
```
index : 0 , rune : 97 , unicode : U+0061 'a'
index : 1 , rune : 98 , unicode : U+0062 'b'
index : 2 , rune : 29579 , unicode : U+738B '王'
```

# 字符串运行时拼接

```golang

i := "fff"
j := "zzzz"
a := i+kj
```

原理 ：找到一个更大的内存地址， 通过内存复制的方法将字符串复制到其中

> 注意： 如果拼接的时候字符串小于32字节时 ， 会有一个临时的缓存提供使用 ， 大于32 会在堆区开辟一个足够大的内存空间

# 字符串和字节数组转化

```golang
a := "hello world"
b := []byte(a)
c := string(b)
```

> 注意： 二者转化并不是简单的引用互转， 如果大小超过32 位 就会还需要申请内存执行copy才行

> 引申 黑魔法 0 成本转化

