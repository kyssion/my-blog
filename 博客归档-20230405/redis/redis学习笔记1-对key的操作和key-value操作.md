# 对键的操作

## KEYS

获得redis在这个实例的数据字典中所有的key列表 支持 glob风格的通配符定义
|符号|含义
---|---
?|匹配一个字符
*|匹配任意个字符包括0
[]|匹配括号间任意一个字符，可以使用-表示范围，比如[a-c] 表示匹配 a 或 b 或 c
\x| 转译字符，比如要匹配？ 就需要使用\?

```
keys abs*
```

## DEL

redis的del命令可以删除一批键，并且返回删除的数量

```
del [key]
```

## EXISTS

判读一个key是否存在

如果存在就返回1反之返回0

```
exists bar
```

## TYPE

返回这个键对应的类型
返回的结果可以能是string,list,hash,set,zset

# key value 操作（value的默认类型就是string）

## SET和GET

 相当于对map类型的数据进行取值

```
set key value
get key
```

## MGET和MSET

同时获取或者设置多个

```
mget key key2 key3
1)value1
2)value2
3)value3

mset key value key1 value1
OK
```

## INCR

incr是redis提供的一个特殊的key value结构

这个结构强制将value制定成integer类型，每次调用key的时候，将会自动的将value+1,并且返回+1 之后的结果

```
incr num
1 #这里返回1是因为默认是0
incr num
2
```

> 注意

incr命令可以是用get和set命令模拟，但是不能保证在分布式环境中的原子性问题，所以这种累加的方法要使用incr保证原子性

## DECR

和incr相反，让value-1

```
decr num
```

## INCRBY

相当于incr命令的进化版
这个命令可以制定每次进行叠加的次数

```
incrby num 3
# 指定每次叠加3
```

## DECRBY

和INCRBY相反，将指定的value - 指定值

```
DECRBY num 3
```

## INCRBYFLOAT

和incr意义相同，指定的key增加一个双精度浮点数

## APPEND

向键值末尾追加value，如果键不存在就将该键设置成value的值

```
append key " value"
```

> 注意如果插入的value拥有空格则需要使用""包裹

## STRLEN

获取字符串UTF-8编码后长度

```
strlen key
123
```

# 二进制操作

## GETBIT和SETBIT

redis提供的位操作方法

redis 使用位操作的使用将会将value进行ascill编码，然后操作对应的二进制值

```
getbit key index
setbit key index 0
```

## BITCOUNT

返回指定key的value中1的个数（使用acill编码后）

```
BITCOUNT key
12
```

## BITOP

提供了AND OR XOR NOT 四种位逻辑操作运算符
通过这些方法可以快速的对key的value进行位运算， 并将结果出存在一个新的key中

```
BITOP and res key1 key2
```