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


