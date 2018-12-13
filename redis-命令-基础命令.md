> append 

指定key 的value 字段填充字符的方法  语法 append key add_value
```shell
redis> EXISTS mykey
(integer) 0
redis> APPEND mykey "Hello"
(integer) 5
redis> APPEND mykey " World"
(integer) 11
redis> GET mykey
"Hello World"
redis> 
```
这个方法时间复杂度o(1) 如果key 不存在的时候将会先创建key value 映射 value为"" 然后再执行append 逻辑(redis底层的实现可能并不是这样的只是为了方便记忆)

---

> bitcount key start end

默认情况下，将检查字符串中包含的所有字节。可以仅在通过附加参数start和end的间隔中指定计数操作。
- 与GETRANGE命令一样，start和end可以包含负值，以便从字符串末尾开始索引字节，其中-1是最后一个字节，-2是倒数第二个，依此类推。
- 不存在的键被视为空字符串，因此该命令将返回零。

---

> BITFIELD key [GET type offset] [SET type offset value] [INCRBY type offset increment] [OVERFLOW WRAP|SAT|FAIL]

---

> BITOP operation destkey key [key ...]

---

> BITPOS key bit [start] [end]

---

> BLPOP key [key ...] timeout

阻塞出队列方法,这方法将会弹出key这个列表第一个非空值,如果key列表所有的都是空的,会将请求堵塞直到列表中存在数据,如果超过timeout时间将会返回nil

```shell
redis> DEL list1 list2
(integer) 0
redis> RPUSH list1 a b c
(integer) 3
redis> BLPOP list1 list2 0
1) "list1"
2) "a"
```

返回值是一个双元素体 1) 表示使用的列表 2) 表示的值

---

> BRPOP key [key ...] timeout

这个方法是BLPOP从列表尾部获取信息的变体

---
