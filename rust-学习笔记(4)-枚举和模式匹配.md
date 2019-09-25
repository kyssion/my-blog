
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
