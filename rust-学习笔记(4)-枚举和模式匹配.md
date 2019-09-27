
rust的枚举类型其实是一种定义(java中更像一种对象可以储存数据)

rust 中的枚举是不能给定默认值的,枚举的类型一般是通过和struct连用来进行使用的

# 枚举的定义和赋值

```rust
enum IpAddrKind {
    V4,
    V6,
}

struct IpAddr {
    kind: IpAddrKind,
    address: String,
}

let home = IpAddr {
    kind: IpAddrKind::V4,
    address: String::from("127.0.0.1"),
};

let loopback = IpAddr {
    kind: IpAddrKind::V6,
    address: String::from("::1"),
};
```

上面的列子,我们使用了结构体存储数据使用枚举来定义类型

# rust提供了更加简单的方法来定义枚举- 枚举变量

```rust
enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

let home = IpAddr::V4(127, 0, 0, 1);

let loopback = IpAddr::V6(String::from("::1"));
```

# 枚举变量的类型支持

rust 的枚举其实支持多种类型 例如，字符串，数字类型或结构。您甚至可以包含另一个枚举

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}
```

# rust 枚举定义通用方法

rust的枚举和struct类似可以定义通用方法

```rust
impl Message {
    fn call(&self) {
        // method body would be defined here
    }
}
let m = Message::Write(String::from("hello"));
m.call();
```

# rust的Option 枚举

rust 实Option枚举来解决null问题的

标准库定义如下

```rust
enum Option<T> {
    Some(T),
    None,
}
```

该Option<T>枚举是非常有用，它甚至包括中拉开序幕; 您无需将其明确纳入范围。此外，这样是它的变体：你可以使用Some和None直接不带Option::前缀。该 Option<T>枚举仍然只是一个普通的枚举，并Some(T)和None类型仍然变种Option<T>。

注意:如果使用None而不是Some，则需要告诉Rust Option<T>我们拥有哪种类型 ，因为编译器无法Some 通过仅查看一个None值来推断该变量将拥有的类型。

```rust
let some_number = Some(5);
let some_string = Some("a string");
let absent_number: Option<i32> = None;
```

# 枚举和rust match 连用

Rust具有一个非常强大的控制流运算符match，该运算符使您可以将值与一系列模式进行比较，然后根据匹配的模式执行代码。模式可以由文字值，变量名，通配符和许多其他东西组成

```rust
#[derive(Debug)] // so we can inspect the state in a minute
enum UsState {
    Alabama,
    Alaska,
    // --snip--
}

enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter(UsState),
}

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter(state) => {
            println!("State quarter from {:?}!", state);
            25
        },
    }
}
```

注意 Coin枚举最后一个参数,使用 Quarter反解析可以获取state中定义的UsState枚举信息


# match 语法和 Option连用

假设我们要编写一个函数，该函数需要一个Option<i32>，如果内部有一个值，则将该值加1。如果内部没有值，该函数应返回该None值，而不要尝试执行任何操作。实用match进行操作

```rust
fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        None => None,
        Some(i) => Some(i + 1),
    }
}

let five = Some(5);
let six = plus_one(five);
let none = plus_one(None);
```

注意: rust对some的处理方法其实是一层语法糖,先反解析some中的内容然后进行其中表达式的操作

# match _占位符

```rust
let some_u8_value = 0u8;
match some_u8_value {
    1 => println!("one"),
    3 => println!("three"),
    5 => println!("five"),
    7 => println!("seven"),
    _ => (),
}
```

该_模式将匹配任何值。通过将其放在我们的其他手臂之后， _它将匹配之前未指定的所有可能情况。的() 只是单位值，所以什么都不会的发生_情况。结果，我们可以说，我们不希望对未在_占位符之前列出的所有可能值不执行任何操作。

# 解决match 在部分情况下的局限性的 if lef 语法

比如 我们只想实用match 表达式在一个单一情况下做点什么其他情况什么都不做,那么rust需要这么去写

```rust
let some_u8_value = Some(0u8);
match some_u8_value {
    Some(3) => println!("three"),
    _ => (),
}
```

这种情况下我们需要写一个_ 来匹配其他情况

注意: rust 会 判断 match 可能匹配的所有情况,如果不满足情况,将会自动报错,这个时候我们需要 使用_ 来匹配所有的其他情况

# if let 语法本质上其实和 if|else if|else 相同的

```rust
let b= if let Some(3) = a{
    println!("three");
    3
}else if let Some(4)= a{
    println!("four");
    4
}else{
    println!("other");
    -1
};
println!("{}",b);
```

