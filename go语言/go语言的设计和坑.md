# Go 语言的设计和坑

本文目的：
- 理解Go为什么X，摆脱原语言的思维
- 解决写代码时比较困惑和不满的点，对容易出错的语法有个印象
- 规范一些习惯性写法，保持代码strength & clean
Go学起来非常简单，但是这是语言设计者刻意为之，很多复杂的细节都藏在语言实现里，导致我们迅速学会Go之后不断踩坑，希望本文能让大家在工作中少踩坑，早下班！

## Why Go

2007年，Google设计Go，目的在于提高在并行编程（多核CPU越来越多）、分布式部署、大型代码库（以及维护他们的非常多的开发人员）的情况下的开发效率。设计时，在吸收C++优点的基础上，收集于很多工程师之间流传的的“不要像C++”的缺点。

### Go like C++：

- 内存消耗少
- 执行速度快
- 启动快

### Go not like C++：

- 程序编译时间短（按照作者过去的工程经验，一个C++大型项目即使make -j8也需要编译一个小时以上）
- 像动态语言一样灵活（提供了如runtime、interface、闭包、反射等很多增加灵活性的特性）
- 内置并发支持（C++的协程至少得等到std23才有，非常落后）
- 丰富的原生库（C++解析json，建立http服务器，使用redis这种都很难找到靠谱的库）
- 多语义（取消了指针运算、取消隐式类型转换、取消类型别名，取消重载，++和赋值作为表达式...）

### Go的优点：

- 面向工程：简单。只有25个关键字，代码风格统一，可读性高，go mod包丰富
- 自动垃圾回收：语言运行时内置垃圾回收
- 语言级并发：非常好用的routine和channel，更高层次的并发抽象
- 静态语言，动态特性

### Go的缺点：

- runtime的性能还需要提高
- 没有泛型（这一项很快就可以克服了）
- 冗余的错误处理
- Go mod不够完善
（Go语⾔将⾛向何⽅?）https://chai2010.cn/static-public/talks/giac2018-go-talk.pdf
（我为什么放弃Go语言）https://blog.csdn.net/liigo/article/details/23699459

Go的设计哲学

（创始人Rob Pike在SPLASH上的演讲，阐述了设计Go的初衷）https://talks.golang.org/2012/splash.article
（许式伟，Go和Java在继承观念上的对比）https://www.infoq.cn/article/go-based-on-connection-combination-language-1
（对面向对象的批评）https://studygolang.com/articles/2944
（王垠：解密“设计模式”，对设计模式的批评）https://www.yinwang.org/blog-cn/2013/03/07/design-patterns

- 少即是多（less is more）：如果一个特性并不对解决任何问题有显著价值，那么go就不提供它；如果需要一个特性，那么只有一种方法去实现
- 面向接口编程：非侵入式接口，反对继承、反对虚函数和虚函数重载（多态）、删除构造和析构函数
- 正交+组合的语言特性：语言的特性之间相互独立，不相互影响。比如类型和方法是互相独立的，类型之间也是相互独立的，没有子类，包也没有子包。不同特性用组合的方式来松耦合
- 并发在语言层面支持：并发更好利用多核，有更强的表现力来模拟真实世界

在设计上，Go秉承了C的简单粗暴。

### 为什么没有继承？

Go没有子类型的概念，只能把类型嵌入到另一个类型中，所以没有类型系统。Go的作者认为类型系统被过度使用了，应该在这个方向上退一步。

- 使用伸缩性良好的组合，而不是继承
- 数据和方法不再绑定在一起，数据的集合用struct，方法的集合用interface，保持正交

类似子类父类的系统造成非常脆弱的代码。类型的层次必须在早期进行设计，通常会是程序设计的第一步，但是一旦写出程序后，早期的决策就很难进行改变了。所以，类型层次结构会促成早期的过度设计，因为程序员要尽力对软件可能需要的各种可能的用法进行预测，不断地为了避免挂一漏万，不断的增加类型和抽象的层次。这种做法有点颠倒了，系统各个部分之间交互的方式本应该随着系统的发展而做出相应的改变，而不应该在一开始就固定下来。
作者附了一个例子，是一些以接口为参数并且其返回结果也是一个接口的函数：

```golang
type Reader interface {
    Read(p []byte) (n int, err error)
}
// 入参是接口的函数，而不是成员方法
func ReadAll(r io.Reader) ([]byte, error)
// 封装器 - 出入参都是接口
func LoggingReader(r io.Reader) io.Reader    //读到的内容录入日志
func LimitingReader(r io.Reader, n int64) io.Reader    //读n个字节停下来
func ErrorInjector(r io.Reader) io.Reader
```

这种组合+函数的模式是相当灵活的。如果用继承，我们可能会多三个io.Reader的定义（或者若干个成员函数）；然后用多态去获得对应的功能
为什么没有异常？

panic和recover这些函数是故意弄的不好用的，因为我们应该减少使用他们。不像Java库中使用异常那样，在go的库中这两个关键字几乎没有使用。

1. 业务中的错误并不是真正的异常情况，if和return完全可以胜任，无需控制流
2. 如果错误要使用特殊的控制结构，错误处理就会扭曲程序的控制流，非常复杂
3. 显式的错误检查会迫使程序员在错误出现的时候对错误进行思考，并进行相应的处理，而不是推给前面的调用堆栈

毫无疑问这会使代码更长一些，但如此编码带来的清晰度和简单性可以弥补其冗长的缺点

为什么没有X？

总结：Go的设计着眼于编程的便利性、编译的速度、概念的正交性以及支持并发和垃圾回收等功能。如果你在Go中找不到其他语言的X特性，那么只能说明这个特性不适合Go，比如它会影响编译速度或设计的清晰度，或者使得基础系统变得特别复杂。

保持Go的特性和风格
- 从Go的角度考虑问题，更加让人容易理解
- 用Go的方式写代码，more effective

# 容易出错的细节

## 创建对象
新建一个对象在go里面有好几种方法，让人迷惑，而且似乎和简洁这一设计原则违背。我们按照对象类型讨论一下：

1. 对于结构体，new(T)和&T{}是等价的，都会给对象赋零值（一般人很少用new）。
Note：直接var obj T;&T也是等价的，只不过变量有可能在堆上，有可能在栈上

2. 对于slice、map、chan，make(map[string]int)和map[string]int{}等价，会对对象进行初始化。

```golang
var a []int                      // nil
a := []int{}                     // not nil
a := *new([]int)                 // nil
a := make([]int,0)               // not nil
```

看一个代码里的badcase：

```golang
//Badcase
ins, err := rpc.GetInsuranceInfoList(ctx, append(make([]string, 0), strconv.FormatInt(parentOrderId, 10)), orderInfo.UserId)
//Correct
ins, err := rpc.GetInsuranceInfoList(ctx, []string{strconv.FormatInt(parentOrderId, 10)},
```

## 零值

零值和未初始化的值并不相同。不同类型的零值是什么？

1. 布尔类型是false，整型是0，字符串是""
2. 指针、函数、interface、slice、channel和map的零值都是nil
3. 结构体的零值是递归生成的，每个成员都是对应的零值

我们来看一个例子。一个为nil的slice和map能做什么操作：

```golang
// 一个为nil的slice，除了不能索引外，其他的操作都是可以的
// Note: 如果这个slice是个指针，不适用这里的规则
var a []int        
fmt.Printf("len(a):%d, cap(a):%d, a==nil:%v\n", len(a),cap(a), a == nil) //0 0 true
for _, v := range a{// 遍历nil切片，不会panic
        fmt.Println(v) 
}
aa := a[0:0]     // 取切片下标，也不会panic，只要索引都是0
bb := a[0:1]     // panic

// nil的map，我们可以简单把它看成是一个只读的map
var b map[string]string
if val, ok := b["notexist"];ok{// 不会panic
        fmt.Println(val)
}
for k, v := range b{// 不会panic
        fmt.Println(k,v)
}
delete(b, "foo") // 也不会panic
fmt.Printf("len(b):%d, b==nil:%v\n", len(b), b == nil) // 0 true
```

### 值传递

Go语言中所有的传参都是值传递，都是原值的一个副本，或者说一个拷贝。传入的数据能不能在函数内被修改，取决于是不是指针或者含有指针的类型（指针被值传递复制后依然指向同一块地址）。这就让人很疑惑，什么时候传入的参数修改会生效，什么时候不会生效？
slice类型在 值传递的时候len和cap不会变，所以函数内append没有用：
type slice struct {
    array unsafe.Pointer
    len   int
    cap   int
}
// badcase
func appendMe(s []int){
    s = append(s, -1)
}

map 和 chan类型，本来就是个指针，所以函数内修改一定会生效：
// map实际上是一个 *hmap
func makemap(t *maptype, hint int64, h *hmap, bucket unsafe.Pointer) *hmap {
    //省略无关代码
}

// chan实际上是个 *hchan
func makechan(t *chantype, size int64) *hchan {
    //省略无关代码
}

再比如一个结构体作为参数：
// 这是一个典型的指针包裹类型
type Person struct {
    name string
    age  *int
}
func modify(x Person){
    x.name = "modified"
    *x.age = 66
}

这个结构体里的age是个指针类型，所以在函数内会被修改。
这种含有指针的结构体类型，里面的指针指向了其他的内存。在发生拷贝的时候，只有结构体本身的内存会被拷贝，指向的内存是和原值共享的。
（更多细节参考 值部：https://gfw.go101.org/article/value-part.html )
但是我们一般希望的是，要么结构体的成员一起改变（这个简单，参数传person的指针），要么一起不改变（深拷贝）。那么另一个让人头疼的问题来了，那我如何深拷贝这个对象？
深拷贝
对于slice，go提供了似乎还不错的方式：
// 自己复制
s1 := []int{1,2,3}
s2 := append([]int{}, s1...)
// 效率更高的复制
s1 := []int{1,2,3}
s2 := make([]int, len(s1))
copy(s2, s1)

如果你要拷贝一个map，只能用for循环依次把键值对赋值到新map里。
切记：需要拷贝map一定要深拷贝，不然如果后续在不同的协程里操作map会panic
如果有其他更复杂的结构体需要深拷贝呢？目前还没有很好的办法：
1. 自己写一个复制值的函数
2. 用序列化/反序列化的方法来做，json，bson
3. 用反射来做
age := 22
p := &Person{"Bob", &age}

v := reflect.ValueOf(p).Elem()
vp2 := reflect.New(v.Type())
vp2.Elem().Set(v)

小心interface判等
go实现接口的时候有两个属性，type T和value V，判等的时候两个属性都要比较。比如一个interface存了3，那么T=int，v=3。只有当两个值都没有设置才等于nil。
var pi *int = nil
var pb *bool = nil
var x interface{} = pi
var y interface{} = pb
var z interface{} = nil

fmt.Println(x == y)   // false
fmt.Println(x == nil) // false
fmt.Println(x == z)   // false

// badcase
type error interface {
    Error() string
}
func returnsError() error {
    var p *MyError = nil
    if bad() {
        p = ErrBad
    }
    return p // Will always return a non-nil error.
}

还有一种常见的场景是我们容易漏掉的。int64和int的interface也不相等：
var int1,int2 interface{}
int1 = int64(0)
int2 = int(0)
fmt.Printf("%v %v = %v", int1, int2, int1 == int2) // 0 0 false

// 如果函数参数用了interface，如果我们很容易犯错
func (m *Map) Load(key, value interface{}) {
    if e, ok := read.m[key]; ok {
        ...
    }
}
// badcase 1: key的类型不一致导致缓存无法取出
m := sync.Map{}
m.Store(0, "ManualCache")
val, ok := m.Load(int64(0)) // nil false 
// badcase 2: value的类型不一致导致断言失败
m.Store("key", 0)
if val, ok := m.Load("key"); ok {
        _ = val.(int64)    // panic
}

点点点
...是个很常用的语法糖，能帮我们节省很多代码。
用作展开：
x := []int{1,2,3}
y := []int{4,5,6}
x = append(x, y...) //而不是for循环
x = append(x, 4, 5, 6) //等价于上面的

用作可变参数列表：
// Println prints to the standard logger in the manner of fmt.Println.
func Println(v ...interface{}) {
    std.Output(2, fmt.Sprintln(v...))  // Output takes parameters (int, string)
}

用作简化数组声明：
var _ = [...]language{
        {"C", 1972},
        {"Python", 1991},
        {"Go", 2009},
}
var b = [...]string{0: "foo", 2: "foo"}        // [3]string{"foo", "", "foo"}

闭包里的局部变量是引用
闭包里起的go协程里面引用的是变量i的地址。所有的go协程启动后等待调用，在下面的协程中，部分协程很可能在for循环完成之后才被调用，所以输出结果很多都是最后一个i的值
// bad case
done := make(chan bool)
for i := 0; i < 5; i++ {
    go func() {
        println(i)
        done <- true
    }()
}
for i := 0; i < 5; i++{
    <-done
}
// 5 5 5 5 5

// good sample 1
for i := 0; i < 5; i++ {
    defer func(i int) {
        println(i)
        done <- true
    }(i)
}
// good sample 2
for i := 0; i < 5; i++ {
    i := i    // 新建变量
    go func() {
        println(i)
        done <- true
    }()
}
//1 3 5 4 2

不要引用大数组
被切片引用的数据不会被释放（即使你仅仅引用了很小一部分），会大幅降低代码性能
headerMap := make(map[string][]byte)

for i := 0; i < 5; i++ {
    name := "/path/to/file"
    data, err := ioutil.ReadFile(name)
    if err != nil {
        log.Fatal(err)
    }
    headerMap[name] = data[:1]
    // better:  headerMap[name] = append([]byte{}, data[:1]...)
}

赋值不是原子操作
在64位的机器上，赋值很可能被拆成mov两次的汇编代码，因此不是原子的。我们可以用atomic里的方法帮助我们做原子操作。
考虑一个内存cache定时刷新的协程：因为随时有请求在读cache，所以刷新cache的时候需要保证cache的指针存取是原子操作。
举例：mycache *map[string]*Cache
// 加载（读取）
var _ = (*T)(atomic.LoadPointer((*unsafe.Pointer)(unsafe.Pointer(mycache))))

// 存储（修改）
atomic.StorePointer(
    (*unsafe.Pointer)(unsafe.Pointer(mycache)), unsafe.Pointer(&newMycache))

所有的操作，只要存在同时存在多个goroutine同时操作一个资源（临界区），除了带有sync，atomic，或者channel关键字的，都不安全。包括但不限于：
1. 并发读写map
2. 并发append切片
3. 自增变量
4. 赋值
接收器用指针还是值
Go的接收器可以传指针进来，也可以传值。注意传值的时候接收器不会被改变。官方推荐下面两种情况该用指针：
1. MyStruct很大，需要拷贝的成本太高
2. 方法需要修改MyStruct
否则Go推荐使用值接收器
Note：如果对象有可能并发执行方法，指针接收器中可能产生数据竞争，记得加锁
func（s * MyStruct）pointerMethod（）{    // 指针方法
    s.Age = -1  // useful
}
func（s MyStruct）valueMethod（）{        // 值方法
    s.Age = -1 // no use
}     

for循环里的变量都是副本
for key, element = range aContainer {...}

关于上面for循环有几个点：
1. 实际遍历的aContainer是原始值的一个副本
2. element是遍历到的元素的原始值的一个副本
3. key和element整个循环都是同一个变量，而不是每次迭代都生成新变量
这里涉及到几个问题。一个是aContainer和element的拷贝成本。aContainer是数组的时候的拷贝成本比较大，而切片和map的拷贝成本比较小。如果想要缩小拷贝成本，我们有几个建议：
1. 遍历大数组时，可以先创建大数组的切片再放在range后面
2. element结构比较大的时候，直接用下标key遍历，舍弃element
还有一个问题是遍历的时候修改，能不能生效？
1. 当aContainer是数组时，因为数组是整个复制，所以直接修改aContainer不会生效
2. 直接修改key或者element，？
3. 因为切片和map是浅复制，在循环中操作aContainer或者aContainer[key]可以生效

因为循环里的副本和函数参数的副本非常类似，所以我们可以参考上面的“值传递”中的内容来判断修改副本是否会使得修改达到想要的效果。
map的值不可取址
map是哈希表实现的，所以值的地址在哈希表动态调整的时候可能会产生变化。因此。存着map值的地址是没有意义的，go中直接禁止了map的值的取地址。这些类型都不能取址：
- map元素
- string的字节元素
- 常量（有名常量和字面量都不可以）
- 中间结果值（函数调用、显式值转换、各种操作）
// 下面这几行编译不通过。
_ = &[3]int{2, 3, 5}[0]        //字面量
_ = &map[int]bool{1: true}[1]  //字面量
const pi = 3.14
_ = &pi                        //有名常量
m := map[int]bool{1: true}
_ = &m[1]                      //map的value
lt := [3]int{2, 3, 5}
_ = &lt[1:1]                   //切片操作

一般来说，一个不可寻址的值的直接部分是不可修改的。但是map的元素是个例外。 map的元素虽然不可寻址，但是每个映射元素可以被整个修改（但不可以被部分修改）：
type T struct{age int}
mt := map[string]T{}
mt["John"] = T{age: 29} // 整体修改是允许的
ma := map[int][5]int{}
ma[1] = [5]int{1: 789} // 整体修改是允许的

// 这两个赋值编译不通过，因为部分修改一个映射元素是非法的。这看上去确实有些反直觉。
ma[1][1] = 123      // error
mt["John"].age = 30 // error

// 读取映射元素的元素或者字段是没问题的。
fmt.Println(ma[1][1])       // 789
fmt.Println(mt["John"].age) // 29

逃逸分析
关心变量在栈或者堆上有助于我们对变量的生命周期有所了解，写出更好性能的代码。比如一些短周期的变量的指针如果和长生命周期的变量绑定，就会使得这个变量迟迟不能回收，影响性能。
Go在栈上的变量不会产生GC成本，因为变量会随着函数的退出一起销毁（当然这样性能也是最高的）。但是，变量是否在栈上，不能简单的通过是否局部变量或者是否使用new构建的引用类型来判断。有一个基本的判断原则：
情况1：如果变量的引用被声明它的函数返回了，那么这个变量就会逃逸到堆上
func ref(z S) *S {
  return &z
}
// go run -gcflags '-m -l' main.go
./escape.go:10: moved to heap: z
./escape.go:11: &z escapes to heap

情况2：返回的结构体引用的对象会逃逸
func refStruct(y int) (z S) {
  z.M = &y
  return z
}
// go run -gcflags '-m -l' main.go
./escape.go:12: moved to heap: y
./escape.go:13: &y escapes to heap

情况3：map、slice、chan引用的对象会逃逸
func main() {
    a := make([]*int,1)
    b := 12
    a[0] = &b
}
// go run -gcflags '-m -l' maint.go
./maint.go:5:2: moved to heap: b
./maint.go:4:11: make([]*int, 1) does not escape

我们看一个例子，逃逸使得性能下降了不少：
func BenchmarkHeap(b *testing.B) {
    b.ResetTimer()
    c := make(chan *T, b.N)
    // c := make(chan T, b.N)
    for i := 0; i < b.N; i++ {
        b := T{a: 3, b: 5}
        c <- &b
        // c <- b
    }
}
//  go test -bench=. -run=none
BenchmarkStack-12       32297865                32.1 ns/op
BenchmarkHeap-12        28062832                40.2 ns/op

routine
Golang并发注意点 
goroutine性能探究和编程规范 
1. 最好确认routine任务的开销大于上下文切换的开销时，才使用routine。
2. 要尽量控制routine的数量，不然会起到反效果
3. channel要注意缓冲区的大小和每次写入的数量，尽量打包写入
防止泄漏
如果routine在运行中被阻塞，或者速度很慢，就会发生泄漏（routine的数量会迅速线性增长）
1. routinue卡死在读取chan却没数据
理想情况下，我们设计的读取chan的routine会把所有的内容读取完毕后才会关闭。但是，一旦读取者在读取完成之前退出，写入方写满chan之后就会卡死。
2. routinue处理的速度过慢
这个情况有点类似消息队列消费者的堆积，如果新起的routine处理速度比主协程还慢的话，堆积起来的routine会越来越多，最终打爆内存
复用timer来替代timer.After
timer.After会创建很多的timer，引发很大的GC消耗。
// 如果有100w个msg推进来，就会有100w个timer被销毁
func longRunning(messages <-chan string) {
        for {
                select {
                // 消息间隔超过1min会return
                case <-time.After(time.Minute):
                        return
                case msg := <-messages:
                        fmt.Println(msg)
                }
        }
}
func longRunning(messages <-chan string) {
        timer := time.NewTimer(time.Minute)
        defer timer.Stop()
        for {
                select {
                case <-timer.C: // 过期了
                        return
                case msg := <-messages:
                        fmt.Println(msg)
                        // 此if代码块很重要。
                        if !timer.Stop() {
                                <-timer.C
                        }
                }
                // 必须重置以复用。
                timer.Reset(time.Minute)
        }
}

- 我们在每次处理完消息后调用timer.Stop()以便于复用。如果timer已经过期，stop会返回false，C里面还有一条过期消息，我们需要把它取出来；如果timer没有过期，stop会返回true，继续执行循环
- 在一个Timer终止（stopped）之后并且在重置和重用此Timer值之前，我们应该确保此Timer的通道C中肯定不存在过期的通知
常用的仓库
sync和atomic
strings
Strings库是重复造轮子的重灾区，很多人试图自己再写一遍
前后处理
var s = "abaay森z众xbbab"
o := fmt.Println
o(strings.TrimPrefix(s, "ab")) // aay森z众xbbab
o(strings.TrimSuffix(s, "ab")) // abaay森z众xbb
o(strings.TrimLeft(s, "ab"))   // y森z众xbbab
o(strings.TrimRight(s, "ab"))  // abaay森z众x
o(strings.Trim(s, "ab"))       // y森z众x
o(strings.TrimFunc(s, func(r rune) bool {
        return r < 128 // trim all ascii chars
})) // 森z众

分割与合并
// "1 2 3" -> ["1","2","3"]
func Fields(s string) []string     // 用空白字符分割字符串
// "1|2|3" -> ["1","2","3"]
func Split(s, sep string) []string // 用sep分割字符串，sep会被去掉
// ["1","2","3"] -> "1,2,3"
func Join(a []string, sep string) string // 将一系列字符串连接为一个字符串，之间用sep来分隔

// Note:
// "1||3" -> ["1","","3"]

演化中的错误处理
满足下面的诉求：
1. 可以把异常传递下去，并不丢失自己的类型
2. 可以保存堆栈信息
Go的错误处理一直在讨论和演进，目前官方已经有几种不同的方案。对于反复写错误处理代码的问题，有几种解决的设想，可以看看上面的（Go语⾔将⾛向何⽅?）
import (
   "golang.org/x/xerrors"
)

func bar() error {
   if err := foo(); err != nil {
      return xerrors.Errorf("bar failed: %w", foo())
   }
   return nil
}
func foo() error {
   return xerrors.Errorf("foo failed: %w", sql.ErrNoRows)
}

func main() {
   err := bar()
   if xerrors.Is(err, sql.ErrNoRows) {
      fmt.Printf("data not found, %v\n", err)
      fmt.Printf("%+v\n", err)
      return
   }
}
/* Outputs:data not found, bar failed: foo failed: sql: no rows in result set
bar failed:
    main.bar
        /usr/four/main.go:12
  - foo failed:
    main.foo
        /usr/four/main.go:18
  - sql: no rows in result set
*/



参考资料
《Go Tour》（一个小时学会Go）https://tour.go-zh.org/welcome/1
《The Go Programming Language Specification》（语法细节）https://golang.org/ref/spec#Introduction（中文版《Go语言编码规范》）
《Go语言圣经》（语法细节）https://docs.hacknode.org/gopl-zh/
《Effective Go》（适合刚学完Go的基础语法时候读）https://www.kancloud.cn/kancloud/effective/72199
《Go语言设计和实现》（适合想了解Go某个特性实现原理的时候参考）https://draveness.me/golang/docs/part1-prerequisite/ch02-compile/golang-compile-intro/
《Go Q&A 101》（可以和官方QA结合看）https://gfw.go101.org/article/unofficial-faq.html#time-sleep-after
《Go 语言高级编程》https://chai2010.cn/advanced-go-programming-book/
《Go语言原本》https://golang.design/under-the-hood/
《Google Go代码规范》https://github.com/golang/go/wiki/CodeReviewComments
《Uber Go规范》https://github.com/xxjwxc/uber_go_guide_cn

