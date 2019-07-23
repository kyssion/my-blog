ps 这里只是简单的纪录一些rust相关的东西

## 变量

### 1. 位置表达式和值表达式（左值和右值）、位置上下文和值上下文

规则 ： 值表达式不能出现在位置上下文中

```rust

pub fn temp() -> i32{
    return 1;
}
pub fn test(){
    let x= &temp();
    temp() = &x; //这里报错 temp是值表达式不能不能放在位置表达式上
}
```

### 2. 不可变与可变

```rust
pub fn test2(){
    let a = 1;
    a = 2;
    let mut  b = 2;
    b = 3;
}
```
在 rust 中 所有变量都默认像java的final关键字，是不可改变的如果需要改变需要指定mut 参数,表示这个值是可以变的

### 3. 所有权和引用

这个和c语言是类似的

所有权 > 直接赋值的时候将会自动的将对应的值转移到新的变量上来

```rust
pub fn ownership(){
    let place1 = "hello";
    //  ^^ 位置表达式 ^^  值表达式
    //   ^ 位置上下文  ^  值上下文
    let place2 = "hello".to_string();
    let other = place1;    // Copy
    // ^^ 位置表达式出现在了值上下文中
    println!("{:?}", place1);  // place1还可以继续使用
    let other = place2;    // Move
    // ^^ 位置表达式出现在了值上下文中
    println!("{:?}", place2); // place2不能再被使用，编译出错 error[E0382]: borrow of moved value: `place2`
}
```
>  rust 官方解释：在语义上，每个变量绑定都有该存储单元的所有权，这种转移内存地址的行为就是所有权的转移，在rust 中称为移动，不转移的情况下其实是一种复制语义

在日常的开发中，有时候并不需要转移所有权，rust 提供& 符号直接操作内存地址

上面的代码这样修改就可以通过了

```rust
pub fn ownership(){
    let place1 = "hello";
    //  ^^ 位置表达式 ^^  值表达式
    //   ^ 位置上下文  ^  值上下文
    let place2 = "hello".to_string();
    let other = place1;    // Copy
    println!("{:?}",other);
    // ^^ 位置表达式出现在了值上下文中
    println!("{:?}", place1);  // place1还可以继续使用
    let other = &place2;    // Move
    // ^^ 位置表达式出现在了值上下文中
    println!("{:?}", place2); // place2不能再被使用，编译出错
    println!("{:?}",other);
}
```

> ps ： 猜测 其实在这里发现一个问题，rust的字符串本身其实返回的就是一个内存地址，而"".to_string() 返回就是一个对象，move是针对对象的

## 函数

rust的函数其实还是很标准的没啥特殊的语法

### 1.  函数定义 参数使用类型：名称分割，返回值写在-> 后面

```rust
pub fn test5(i32:a,i8:b)->i32{
    return a+b;
}
pub fn test6(){
    println!("test6");
}
```

### 2. 函数指针

rust 的函数是一等公民，可以函数化传参或者作为返回值（注意函数参数定义必须是变量名：类型）

```rust
//函数作为参数
pub fn test7(op:fn(i32:a,i8b)->i32,a:String,bool:c)->&str{
    return "sdfsdf";
}
//函数作为返回值
pub fn ff(){
    
}

pub fn ff2()->i32{
    return 12;
}

pub fn test8()->fn() {
    return ff;
}

pub fn test9()->fn()->i32{
    return ff2;
}
```

### 3. 函数闭包

rust 闭包的特点

- 可以像函数一样被调用
- 可以捕获上下文环境中的自由变量
- 可以自动推断输入和返回的类型

#### 1. 闭包传参

```rust
pub fn  test_fun<F: Fn(i32,i32)->i32>(op:F,a:i32,b:i32)->i32{
    return op(a,b);
}

pub fn test(){
    let c = 2;
    let d = 3;
    let a= test_fun(|a,b|->i32 {return a+b }, 0, 1);

    let b = test_fn2(||c+d);
    println!("{:?}",a);
    println!("{:?}",b);
}

pub fn math<F: Fn() -> i32>(op: F) -> i32 {
    op()
}
pub fn test_fn2<F: Fn()->i32>(op:F)->i32{
    return op();
}

pub fn test2(){
    let a = 2;
    let b = 3;
    println!("{:?}",math(|| a + b));
    println!("{:?}",math(|| a * b));
}
```

不知道为啥函数传参数函数名称必须带上类似范型的东西

#### 2. 闭包返回值

玄学了。。。。。

```rust

//动态分发
fn two_times() -> Box<Fn(i32) -> i32> {
    let i = 2;
    Box::new(move |j| j * i)
}
let result = two_times();
assert_eq!(result(2), 4);

//动态分发2018
fn two_times_dyn() -> Box<dyn Fn(i32) -> i32> {
    let i = 2;
    Box::new(move |j| j * i)
}
let result = two_times_dyn();
assert_eq!(result(2), 4);

//静态分发
fn two_times_impl() -> impl Fn(i32) -> i32{
    let i = 2;
    move |j| j * i
}
let result = two_times_impl();
assert_eq!(result(2), 4);
```

## rust 的 CTFE机制

rust 支持在编译期运行函数来进行求值操作

```rustpub fn test3(){
    let a=0;
    let aa = if(a>12){
        12
    }else{
        8
    };
}
pub fn init_arr_leng()->i32{
    return 123;
}

pub fn init_arr(){
    let arr = [0,init_arr_leng()];
    println!("{:?}",arr[1]);
}
```

ps 如果使用的rust2015 需要加上

## rust流程控制

### 1. if else

rust 没有提供三元表达式运算符

```rust
pub fn test3(){
    let a=0;
    let aa = if(a>12){
        12
    }else{
        8
    };
}
```

### 2. where,for...in,loop

rust 提供了三种

```rust
pub fn test4(){
    let a =0;
    while a<10{
        a+=1;
    }
    loop{
        break;
    }
    for a in 1..1000{
        
    }
    return;
}
```

### 3. match 

rust的match 模式匹配相当的强大，匹配是在 rust 中很强的东西，可以匹配所有类型

=> 后面跟的是表达式，不能是语句

#### (1) 基本形式类似这样

```rust
fn match_test(num: u8) {
    match num {
        13 => println!("正确"),
        3 | 4 | 5 | 6 => println!("3 或 4 或 5 或 6"),
        14...20 => println!("14..20"),
        _ => println!("不正确"),
    }
}
```
#### (2) match中可以应用解构

match 中可以应用解构

```rust
// 元组
fn match_test2(){
    let pair = (0, -2);
    match pair {
        (0, y) => println!("y={}", y),
        (x, 0) => println!("x={}", x),
        _ => println!("default")
    }
}
```

ps : 同样可以作用于结构体，指针，枚举

#### (3) 可以加上if来守卫

```rust
fn match_test3(num:i32){
    match num {
        x if x != 20 => println!("14..20"),
        _=> println!("不正确"),
    }
}
```

#### (4) 绑定变量

```rust
fn match_test4(num:i32){
    match num {
        13 => println!("正确"),
        3|4|5|6 => println!("3 或 4 或 5 或 6"),
        n @ 14...20 => println!("{}", n),
        _=> println!("不正确"),
    }
}
```
### if let 和 where let 表达式

#### (1) if let 和 match 相同的地方是

```rust
fn match_test5(){
    let boolean = true;
    if let true = boolean{
        println!("sdfsdf");
    }
}
```

#### (2) while let 

个人感觉while let 语法是为了简化如下的一种方法使用loop循环的一种方法

```rust
fn match_test6(){
    let mut v = vec![1,2,3,4];
    //使用loop 进行pop出参数替换
    loop{
        match v.pop()  {
            Some(x)=>{
                print!(":{}",v)
            },
            None => break
        }
    }
    //使用while方法 获取 v.pop() 出参队列
    while let Some(x) = v.pop(){
        print!(x);
    }
}
```