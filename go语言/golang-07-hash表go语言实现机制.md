> todo 底层实现原理

# golang map 使用注意事项

1. golang 赋值的时候必须要初始化

```golang
var hash map[int]int
hash[123] =123 // panic 这里会报错
```

2. golang 支持 nil 的map 取值 ， 虽然会返回nil

```golang
v, ok := map[key]
```

3. golang  map 实现底层原理