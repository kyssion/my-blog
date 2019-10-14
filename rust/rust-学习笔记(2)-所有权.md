所有权是Rust的最独特功能，它使Rust无需垃圾收集器即可保证内存安全 

所有权以及几个相关功能：借用，切片以及Rust如何在内存中布置数据

> 引申 栈和堆

# 所有权规则

首先，让我们看一下所有权规则。在通过示例进行说明时，请牢记以下规则：

Rust中的每个值都有一个变量，称为其所有者。
一次只能有一个所有者。
当所有者超出范围时，该值将被删除。

# 可变范围

可以理解成java的作用域

# 变量回收

rust和gc编程语言不同，他使用可变范围来控制变量的自动回收

```rust
{
    let s = String::from("hello"); // s is valid from this point forward

    // do stuff with s
}// this scope is now over, and s is no longer valid
```

但是有一个问题，比如这种代码

```rust
{
    let s1 = String::from("hello"); // s is valid from this point forward
    let s2= s1;
    // do stuff with s
}// this scope is now over, and s is no longer valid
```

这是一个问题：当s2和s1走出去的范围，他们都将尝试释放相同的内存。这被称为双重释放错误，是我们前面提到的内存安全性错误之一。释放内存两次可能导致内存损坏，从而可能导致安全漏洞。

为了确保内存安全，在Rust中，在这种情况下会发生的事情还有一个细节。Rust认为s1不再有效，而不是尝试复制分配的内存

> 注意这个很重要，也就是说在rust中如果发生了已经拥有的变量再进行赋值，并且原来的值还是有效的那么一定是copy的值

```rust
let s1 = String::from("hello");
let s2 = s1.clone();
println!("s1 = {}, s2 = {}", s1, s2);
```

rust对一些常用的对象在进行上面的操作的时候不需要调用copy方法，这些对象如下

- 所有整数类型，例如u32。
- 布尔类型，bool值true和false。
- 所有浮点类型，例如f64。
- 字符类型char。
- 元组（如果它们仅包含also的类型）Copy。例如， (i32, i32)是Copy，但(i32, String)不是。

# 所有权和职能

这个很重要

用于将值传递给函数的语义类似于用于将值分配给变量的语义。就像赋值一样，将变量传递给函数将移动或复制。

1. 函数传参语义

```rust
fn main() {
    let s = String::from("hello");  // s进入范围
    takes_ownership(s);             // s的值移入函数...因此在这里不再有效
    //print("{}",s);     //这样做会报错，因为环境已经发生改变了
    let x = 5;                      //x进入范围
    makes_copy(x);                  // x会移入函数，但i32是Copy，因此以后仍然可以使用x

} //在此，x超出范围，然后是s。 但是因为s的值被移动了，所以没有什么特别的事情发生。
fn takes_ownership(some_string: String) { //some_string进入范围
    println!("{}", some_string);
} // 在这里，some_string超出范围并调用`drop`。 备份内存已释放。
fn makes_copy(some_integer: i32) { // some_integer进入范围
    println!("{}", some_integer);
} // 在这里，some_integer超出范围。 没什么特别的。
```

2. 函数返回值语义

```rust
fn main() {
    let s1 = gives_ownership();         // Gives_ownership将其返回值移至s1
    let s2 = String::from("hello");     // s2进入范围
    let s3 = takes_and_gives_back(s2);  // s2被移入takes_and_gives_back，它的返回值也移入s3
} // 在此，s3超出范围并被丢弃。 s2超出范围但被移动了，所以什么也没发生。 s1超出范围并被丢弃。

fn gives_ownership() -> String {             // gets_ownership会将其返回值移至调用它的函数中
    let some_string = String::from("hello"); // some_string进入范围
    some_string      // 返回some_string并移至调用函数
}

// take_and_gives_back将获取一个String并返回一个
fn takes_and_gives_back(a_string: String) -> String { // a_string comes into
    // scope
    a_string  // 返回a_string并移至调用函数
}
```


# 所有权在函数中存在的问题

拥有所有权然后返回所有功能的所有权有点乏味。如果我们想让函数使用值而不是所有权，该怎么办？令人非常烦恼的是，除了我们可能还想返回的函数主体所产生的任何数据之外，如果我们想要再次使用它，则还需要将返回的信息传递回去。

可以使用元组返回多个值

```rust
fn main() {
    let s1 = String::from("hello");
    let (s2, len) = calculate_length(s1);
    println!("The length of '{}' is {}.", s2, len);
}

fn calculate_length(s: String) -> (String, usize) {
    let length = s.len(); // len() returns the length of a String

    (s, length)
}
```

不过rust提供了特殊的语义叫参考和借用来解决这个问题

# 参考和借用（引用和可变引用）突破所有权的限制

修改方法 这种引用的方法其实是传一个引用地址，不过是只读的

```rust
fn main() {
    let s1 = String::from("hello");
    println!("info : {},length : {}",s1,calculate_length(&s1))
}
fn calculate_length(s: &String) -> usize {
    s.len()
}
```

如果需要可读，就需要用下面这种方法

```rust
fn main() {
    let mut s = String::from("hello");
    println!("len : {}",change(&mut s));
    println!("data : {}",s);
}

fn change(some_string: &mut String) -> usize{
    some_string.push_str(", world");
    return some_string.len();
}
```


注意如果这样写就会有错误

```rust
fn main() {
    let mut s = String::from("hello");
    println!("data : {} ，len : {}",s,change(&mut s));
}
fn change(some_string: &mut String) -> usize{
    some_string.push_str(", world");
    return some_string.len();
}
```

```
3 |     println!("data : {} ，len : {}",s,change(&mut s));
  |              ---------------------- -        ^^^^^^ mutable borrow occurs here
  |              |                      |
  |              |                      immutable borrow occurs here
  |              immutable borrow later used here
```

这个在一行来写就会有问题，因为一行的时候就是一个作用域，必须保证一致性


# 可变引用的限制

但是可变引用有一个很大的限制：您只能在一个特定范围内对一个特定的数据进行一个可变引用

比如这种两种情况情况

```rust
//两个可变引用
let r1 = &mut s;
let r2 = &mut s;//ERROR

//有不可变和可变引用
let r1 = &s; // no problem
let r2 = &s; // no problem
let r3 = &mut s; 
println!("{}, {}, and {}", r1, r2, r3);// BIG PROBLEM
```

如果将r1和r2 分别给两个不同的线程可能会出现征用问题，简单的说就是这样

- 两个或多个指针同时访问相同的数据。
- 至少有一个指针用于写入数据。
- 没有用于同步对数据访问的机制。

上面的例子2 如果写成这种就没有问题

```rust
let r1 = &s; // no problem
let r2 = &s; // no problem
println!("{}, {}, ", r1, r2);// BIG PROBLEM
let r3 = &mut s; 
```

> 注意问题就是在一个范围内不但使用了不可变引用，而且使用了可变引用


# 突破限制

与往常一样，我们可以使用大括号创建新的范围，从而允许多个可变引用，而不是同时引用：

```rust
let mut s = String::from("hello");
    let r1 = &mut s;

} // r1 goes out of scope here, so we can make a new reference with no problems.

let r2 = &mut s;
```

# 悬挂指针处理

```rust
fn main() {
    let reference_to_nothing = dangle();
}

fn dangle() -> &String {
    let s = String::from("hello");

    &s
}
```

由于s是在内部创建的dangle，当代码dangle完成时， s将被释放。但是我们试图返回对它的引用。这意味着此引用将指向无效String。

修改成这样就可以编译通过

```rust
fn no_dangle() -> String {
    let s = String::from("hello");
    s
}
```

# 另一个突破所有权的方法,切片

切片其实本是上是连续数据的引用

比如一个 数组  0 1 2 3 4 5 6 

其中变量x 指向 0 

然后生成x的切片 y 指向 3

这个时候y就是x的一部分引用，注意所有的切片都是只读的不可以进行修改(类型是&str)，相当于给上面的arr开了一个口子可以看见数据

```rust
fn main() {
    let mut str = String::from("one");
    let p = test(&mut str);
    println!("{}",p);
    str.clear();
}
fn test(st:&mut String)->&str{
    st.push_str("sdfsdf");
    &st[..]
}
```

注意一个地方，如果代码这样写将会报错

```rust
fn main() {
    let mut str = String::from("one");
    let p = test(&mut str);
    str.clear();
    println!("{}",p);
}

fn test(st:&mut String)->&str{
    st.push_str("sdfsdf");
    &st[..]
}
```

```rust
 --> src/main.rs:4:5
  |
3 |     let p = test(&mut str);
  |                  -------- first mutable borrow occurs here
4 |     str.clear();
  |     ^^^ second mutable borrow occurs here
5 |     println!("{}",p);
  |                   - first borrow later used here
```

原因时数据产生了脏数据，多个引用在使用前发生了变化

# rust 数组切片

```rust
let a = [1, 2, 3, 4, 5];
let slice = &a[1..3];
```