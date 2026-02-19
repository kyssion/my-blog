# 定义和实例化结构

## 定义

```rust
// 普通的
struct User {
    username: String,
    email: String,
    sign_in_count: u64,
    active: bool,
}

//元祖结构体
struct User(i32,i32,i32)

//单元状结构体
struct User()
```

注意rust中所有的结构体都默认被mut标记

2. 函数初始化struct

```rust
fn build_user(email: String, username: String) -> User {
    User {
        email,
        username,
        active: true,
        sign_in_count: 1,
    }
}
```

使用函数的时候可以快速的参数名称和结构体快速 对应

# 使用结构更新语法从其他实例创建实例

```rust
let user2 = User {
    email: String::from("another@example.com"),
    username: String::from("anotherusername567"),
    active: user1.active,
    sign_in_count: user1.sign_in_count,
};
```

其实本质上就是从别的struct体中获取相同的值，但是rust提供了一种快速同种类型转化方法

```rust
let a= User{
    ...b
}
```

```rust
fn main() {
    let user1 = User{
        name:&mut "sdfsdf",
        age:212
    };
    let userTest=UserTest{
        name:&mut "sdfsdf",
        age:212
    };
    let user2 = User{
        ..user1
    };
    let user3= User{
        name:userTest.name,
        age:userTest.age
    };
    //异常必须同种类型
//    let user4 = User{
//        ...userTest
//    }

}
struct User{
    name:&mut str,
    age:i32
}

struct UserTest{
    name:&mut str,
    age:i32
}
```

存在一个疑问点

```rust
fn main() {
    let user1 = User{
        name:String::from("wang"),
        age:212
    };
    let user2 = User{
        ..user1
    };
    user1.name.push_str(" lin");
    println!("{}",user2.name);
}
```

这样写有问题吗，user2.name的值是啥

# 结构体方法

方法和函数类似，但是方法与函数的不同之处在于，它们是在struc的上下文中定义的，并且它们的第一个参数始终为self，它表示调用该方法的struct实例。

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}

fn main() {
    let rect1 = Rectangle { width: 30, height: 50 };
    println!(
        "The area of the rectangle is {} square pixels.",
        rect1.area()
    );
}
```

在C和C ++中，使用两种不同的运算符来调用方法： .如果要直接在对象上调用方法，并且->要在指向对象的指针上调用方法，则需要先取消引用该指针。换句话说，如果object是指针， object->something()则类似于(*object).something()。

Rust没有与->运算符等效的对象。相反，Rust具有称为自动引用和取消引用的功能。调用方法是Rust少数具有这种行为的地方之一。

下面是它如何工作的：当你调用一个方法有object.something()锈会自动添加&，&mut或*使object该方法的签名相匹配。换句话说，以下是相同的：

```rust
p1.distance(&p2);
(&p1).distance(&p2);
```

第一个看起来更干净。这种自动引用行为行之有效，因为方法的接收方很明确-的类型self。给定方法的接收者和名称，Rust可以明确地确定该方法是读取（&self），变异（&mut self）还是使用（self）。Rust使方法接收者隐含借贷这一事实是在实践中使所有权符合人体工程学的重要组成部分。