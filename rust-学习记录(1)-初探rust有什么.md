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
在 rust 中 所有变量都默认像java的final关键字，是不可改变的如果需要改变需要指定mut 参数

###3. 所有权和引用

这个和c语言是类似的

```rust
pub fn test3(){
    let a = "hello";
    let b = "hello".to_string();
    let other = a;
    println!("{:?}",other);
    let other = b;
    println!("{:?}",other);
}
```

