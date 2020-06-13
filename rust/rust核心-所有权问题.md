# 在rust中，所有权有一下的几个规则

1. 块级范围中，所有权向下传导

```rust
pub fn test1(){
    let a = "111";
    {
        println!("a: {}",a);
        let b = "222";
    }
    //错误超出了所有权范围
    println!("b:{}",b);
}
```

> 一个变量只能拥有他自己或者比自己小的作用域 ， 可以使用领域返回值扩展作用领域

使用表达式返回值即可

```rust
fn test2(){
    let a = {
        let b = "222";
        b
    };
    //错误超出了所有权范围
    println!("a:{}",a);
}
```

2. 全局范围一个变量的所有权只能唯一持有

> 任何一个变量的所有权只能有一个变量持有

举一个 rust 移动的例子

```rust
fn test3(){
    let a= String::from("test");
    let b = a;
    //错误 ， 所有权转移了
    //println!("{}",a);
    //------可以使用clone方法给予新的值

    let a = String::from("test");
    let b = a.clone();
    println!("{}",a);
}
```

3. 函数范围传入参数和返回参数都可以转移所有权

> 当是函数的时候 ， 可以动态的转移对应的所有权，类似规则1 ， 调用函数的范围失去传入变量的所有权

```rust
fn test4(){
    let a = String::from("test1");
    /// a 变量所有权下移，但前失去了a的所有权
    let b = error_add_str(a);
    /// b 获取了 新的所有权范围，所以可以使用了
    println!("{}",b);
}

/// 内部生成一个新的变量 ，重新返回给上层，将所有权付给上层 ， 原来的值将回收
fn add_str(str : String) -> String{
    let mut new_str = str.clone();
    new_str.push_str("_add_ok");
    return new_str
}

/// 将但前的所有权转移下去 ， 并且再将原来的值返回出来
fn add_str_no_clone(mut str : String) -> String {
    str.push_str("_add_ok");
    return str;
}
```

# 使用引用和分片简化所有权转移

上面的规则3 我们会发现所有权每次编写的时候都需要考虑进来 ， 这样就有很多准备工作去做 , rust提供了一个方法来简化所有权转移问题

4. 引用传参可以简化所有权转移，保持调用者所有权不变

```rust
fn test5() {
    let mut a = String::from("test");
    add_str_l(&mut a);
    println!("{}",a);
}

fn add_str_l(str: &mut String){
    str.push_str("_add_ok_l");
}
```

5. 借阅和普通本质上上相同 ， 只是为了方便函数做所有权转移限制

这样会出错

```rust
fn test5() {
    let mut a = String::from("test");
    add_str_l(&mut a);
    let mut b = &mut a;
    /// 错误 ，这个时候所有权已经转移到了b中了
    ///a.push_str("test");
    println!("{}",b);
}

fn add_str_l(str: &mut String){
    str.push_str("_add_ok_l");
}
```

6. rust 禁止多指针共享相同变量 ， 如果存在以最后一个为准 ,只针对可变引用 

```rust
fn test6(){
    let mut a = String::from("test");
    let item = &mut a;
    let item2 = &mut a;
    /// 报错 ， 不能多引用
    println!("{} {}",item,item2);
}
```

7. 可变与不可变引用组合的情况下，要保证在不可变引用定义使用之间，不存在数据修改或者可变引用存在

```rust
fn test6(){
    let mut a = String::from("test");
    let item = &a;
    let item2 = &a;
    ///
    ///  这之间不能存在修改原始数据的逻辑，和 元数据的&mut 引用
    ///
    ///
    println!("{} {}",item,item2);

    /// 之后就可以进行处理了
    a.push_str("test");
    println!("{}",a);
    /// a 的第一次借阅
    let item = &mut a;
    /// 这个函数也用了借阅 所以是第二次
    a.push_str("test");
    /// 以第二次为准 ， 使用第一次出现问题
    println!("{}",a);
}
```

> 注意一个地方就是 push_str 本身也是使用借阅 ， 对象内写法，等价于下面的这个逻辑

```rust
a的方法.put_str(&mut a,"test");
let a = &mut a;
```

这里强制刷新了所有关于a的引用都是为最后操作了这个a的位置

8. rust 当函数有借阅并且返回值也是借阅的时候 ， 在rust中返回值必然为传入的借阅的子集，这样相同类型的借阅会被认为重新借阅

> rust不能在函数中返回但前环境生成的借阅类型 ， 因为借阅在rust中是一个非常特殊的存在 ， 用来解决函数所有权转移的问题的，所以rust对借阅的范围方法是，对于借阅生效的作用领域范围只有最后一个借阅生效 ， rust只支持领域范围缩小 ， 不支持函数返回值导致领域范围扩大

举例子： rust只支持领域范围缩小 ， 不支持函数返回值导致领域范围扩大

```rust
fn test8(){
    let item = String::from("test");

    ///引用类型不允许扩展作用领域
    let new = {
        let mut i = String::from("test");
        &mut i
    };
    println!("{}",new);
}

/// 返回对但前函数拥有的引用
fn test9() -> &'static mut String{
    let mut item = String::from("test");
    return &mut item;
}
```

看一个函数加引用的复杂例子

```rust
fn test7(){
    let mut a = String::from("test");
    // let mut b = &mut a;
    let mut b = add_str_ls(&mut a);
    let mut c = &mut a;
    let mut d = add_str_ls(c);
    // let mut d =&mut b;
    d.push_str("test");
    println!("{}",a);
}

fn add_str_ls(str: &mut String)->&mut String{
    str.push_str("_add_ok_l");
    return str;
}
```

以上的b c d 在rust中都是认为和&mut a 一样的引用 因为函数和返回之值的类型相同 ，所以最后只能是 d

# rust 切片

注意一个点就行了 切片类型不可修改 ， 从定义到使用之间元数组对应的切片范围不可变更

```rust
fn test(){
    let ccc = 123;
    let mut a = [1,2,3,4,5,6];
    let b = &a[1..3];
    a[5] = 5;
    println!("{:?}",b);
}
```

> 引申 > rust 对应的切片类型必须是& 开头的，因为切片本质上为元数组的一段引用，所有必须用指针