在java8的函数式编程中,处理流式处理还提供了空值的流式处理Optional

```java
Optional<String> string = new Optional<>("sdfsdf");
string.orElse("sdf");
string.orElseGet(()->{return "sdfsdf";});
string.isEmpty();
string.isPresent();
```

这个方法几个重要的方法

### 1. orElse(value) 和 orElseGet(function) 和 orElseThrow

获取一个值, 如果没有将会 将会使用value替代,如果传入的函数将会运行函数返回指定的值,如果式异常将会跑出空值

### 2. isEmpty isPresent

前者如果optional为空将会返回true 后者将会返回false


