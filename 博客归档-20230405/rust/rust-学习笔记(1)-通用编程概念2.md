# 特殊的变量类型

rust变量和其他的编程的变量系统是不同的,在rust中默认的变量都是不可改变的类型

```rust
let x = 123;// 这个变量是不可变类型
```

如果让这个变量编程可变类型需要使用一种个关键字 mut

```rust
let mut x = 123;
x =222;
```

> mut 关键字能让这个变量变得可以修改


# 常量

您使用const关键字而不是关键字声明常量let，并且值的类型必须带注释

```rust
const MAX_POINTS: u32 = 100_000;
```

Rust常量的命名约定是使用所有大写字母在单词之间加上下划线，并且可以在数字文字中插入下划线以提高可读性

# rust的影子类型

rust 支持影子模式，这种模式下，可以对统一个名称重复的进行赋值操作

```rust
fn main() {
    let x = 5;
    let x = x + 1;
    println!("the value of x is :{}",x);
    let x =" x * 2";
    println!("The value of x is: {}", x);
}
```

# rust 类型系统

## 1. 基本类型和java相同

（做java的时候很少考虑int 和long之间的区别，其实通过这种方法可以节省大量的内存）

## 2. 复合类型

### 元祖类型

用括号阔起来的类型

```rust
fn main() {
    let tup: (i32, f64, u8) = (500, 6.4, 1);
}
```

支持. 赋值和解析赋值

```rust
fn main() {
    let tup = (500, 6.4, 1);

    let (x, y, z) = tup;

    println!("The value of y is: {}", y);
}

fn main() {
    let x: (i32, f64, u8) = (500, 6.4, 1);

    let five_hundred = x.0;

    let six_point_four = x.1;

    let one = x.2;
}
```

### 数组类型

rust 的数组类型和java相同

1. 创建数组 3种方法

```rust
let a = [1, 2, 3, 4, 5];
let a: [i32; 5] = [1, 2, 3, 4, 5];
let a = [3; 5];

```

# rust的表达式和语句

rust的语句没有返回值但是表达式是有的，调用函数是一个表达式。调用宏是一个表达式。作用域的块{}是一个表达式。 控制流（if else）也是表达式

比如这种赋值

```rust
fn main() {
    let x = 5;
    let y = {
        let x = 3;
        x + 1
    };
    println!("The value of y is: {},{}",x, y);
}
```

输出 5 3  作用域中的变量不影响外部的

> 注意 x+1 如果有;号 就是语句，没有就是表达式

# 函数

```rust
fn five(x:i32,y:i32,z:i32) -> i32 {
    x+y+z
}
```

注意rust不支持函数重载

# 控制流

1. if else

变量参数必须是boolean 类型

```rust
fn main() {
    let number = 6;
    if number % 4 == 0 {
        println!("number is divisible by 4");
    } else if number % 3 == 0 {
        println!("number is divisible by 3");
    } else if number % 2 == 0 {
        println!("number is divisible by 2");
    } else {
        println!("number is not divisible by 4, 3, or 2");
    }
    println!("ans : {}",number);
}
```

let if 判断表达式

```rust
fn main() {
    let condition = true;
    let number = if condition {
        5
    } else {
        6
    };
    println!("The value of number is: {}", number);
}
```

因为if else 可以变成一个语句所有，可以是有不带分号的表达式来返回结果

注意： 这种方法需要保证所有的返回结果要相同

2. loop

相当于死循环，一般和break-可返回结果的break连用

```rust
fn main() {
    let mut counter = 0;
    let result = loop {
        counter += 1;

        if counter == 10 {
            break counter * 2;
        }
    };
    println!("The result is {}", result);
}
```

3. while

```rust
fn main() {
    let a = [10, 20, 30, 40, 50];
    let mut index = 0;

    while index < 5 {
        println!("the value is: {}", a[index]);

        index += 1;
    }
}
```

和java相同

4. for 

和python类似

```rust
fn main() {
    let a = [10, 20, 30, 40, 50];
    for element in a.iter() {
        println!("the value is: {}", element);
    }
}
fn main() {
    for number in (1..4).rev() {
        println!("{}!", number);
    }
    println!("LIFTOFF!!!");
}
```

rust的for循环不是很好用，类似python ，官方鼓励迭代器模式，貌似迭代器比for循环强大的多。。。。

This is an [example link](https://zhuanlan.zhihu.com/p/74893652). 

