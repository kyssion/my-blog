Rust具有许多功能，可让您管理代码的组织，包括哪些细节被公开，哪些细节是私有的以及程序中每个作用域中的名字。这些功能（有时统称为模块系统）包括：

- 包装：货运功能，可让您构建，测试和共享包装箱
- 板条箱：产生库或可执行文件的模块树
- 模块和用途：让您控制路径的组织，范围和隐私
- 路径：一种命名项目的方式，例如结构，函数或模块

# 包装和板条箱

条板箱是二进制文件或库,一个软件包包含一个Cargo.toml文件，该文件描述了如何构建这些包装箱。
包装箱是其它语言中库（library）或包（package）的同义词

板条箱会将范围内的相关功能分组在一起，因此该功能易于在多个项目之间共享

# 简单的讲解一些rust的包结构

rust在规范中定义了两种类型 src/main.rs 和 src/lib.rs

1. 如果路径中包含 src/main.rs 的时候,将会生成一个执行的而二进制文件叫做包装
2. 如果路径中包含 src/lib.rs 的时候,将会形成一个可加载的包叫做跳板箱
3. 如果既有 src/lib.rs和src/main.rs 的时候,将会生成两个包,一个包装一个跳板箱

# 一个简单的rust包目录

```
├── Cargo.lock
├── Cargo.toml
├── src
│   ├── english
│   │   ├── farewells.rs
│   │   ├── greetings.rs
│   ├── japanese
│   │   ├── farewells.rs
│   │   ├── greetings.rs
│   └── lib.rs
```

上面的其实是一个lib包的路径 如果根的cargo toml 名称叫做phrases,那么上面的模块层次结构如下

```
                                    +-----------+
                                +---| greetings |
                  +---------+   |   +-----------+
              +---| english |---+
              |   +---------+   |   +-----------+
              |                 +---| farewells |
+---------+   |                     +-----------+
| phrases |---+
+---------+   |                     +-----------+
              |                 +---| greetings |
              |   +----------+  |   +-----------+
              +---| japanese |--+
                  +----------+  |   +-----------+
                                +---| farewells |
                                    +-----------+
```

# 定义模块

rust中可以使用mod 关键字定义一个模块, 比如

```rust
mod front_of_house {
    mod hosting {
        fn add_to_waitlist() {}
        fn seat_at_table() {}
    }
    mod serving {
        fn take_order() {}
        fn serve_order() {}
        fn take_payment() {}
    }
}
```

上面例子中的定义的mod其实形成了一个模块素

```
crate
 └── front_of_house
     ├── hosting
     │   ├── add_to_waitlist
     │   └── seat_at_table
     └── serving
         ├── take_order
         ├── serve_order
         └── take_payment
```

从一定的程度上讲rust的其实是一个可分级的模块系统

# 模块定义时路径和访问限制

```rust
mod front_of_house {
    pub mod hosting {
       pub fn add_to_waitlist() {}
    }
}

pub fn eat_at_restaurant() {
    // Absolute path
    crate::front_of_house::hosting::add_to_waitlist();

    // Relative path
    front_of_house::hosting::add_to_waitlist();
}
```

- 上面例子中我从eat_at_restaurant() 方法中引用了front_of_house作用域下的hosting作用域的add_to_waitlist()方法,使用crate表示从项目跟路径的开始向上搜索的绝对路径,没有带上的表示使用以当前文件为跟路径的绝对路径
- 注意add_to_waitlist的pub 关键字, 如果没有这个关键字表示是私有的方法,只有自己和子类可以使用能