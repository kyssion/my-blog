### 1. 方法引用

Lambda 表达式有一个常见的用法：Lambda 表达式经常调用参数。比如想得到艺术家的姓名，Lambda 的表达式如下：

```java
artist -> artist.getName();
```

java 为这种写法提供了更加简单的实现

```java
Artist::getName
```

构造函数也有同样的缩写形式，如果你想使用 Lambda 表达式创建一个 Artist 对象，可能会写出如下代码：

```java
(name, nationality) -> new Artist(name, nationality)
```

使用方法引用，上述代码可写为：

```java
Artist::new
```


