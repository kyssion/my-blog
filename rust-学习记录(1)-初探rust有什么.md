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

###3. 所有权和引用

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

### 3. 函数

rust的函数其实还是很标准的没啥特殊的语法

> 函数定义 参数使用类型：名称分割，返回值写在-> 后面

```rust
pub fn test5(i32:a,i8:b)->i32{
    return a+b;
}
pub fn test6(){
    println!("test6");
}
```

> 函数指针

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
