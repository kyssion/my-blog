> 针对jdk11+ 

> map类型操作最核心的就是这些方法get(),put(),contain(),computeIfAbsent(), 我们只解析这些方法如何实现

> map类型有一些通用的逻辑操作,统一梳理

> 最为解析的map类型是 HashMap Hashtable TreeMap WeakHashMap LinkedHashMap ConcurrentHashMap

# map类型散列值计算

典型Map类型|hash计算逻辑|下表计算逻辑
---|---|---
HashTable| key的hash| (hash & 0x7FFFFFFF) % tab.length
HashMap| (h = key.hashCode()) ^ (h >>> 16)| hash^(table长度-1)
ConurrentHashMap| (h ^ (h >>> 16)) & 0x7FFFFFFFTS|hash^(table长度-1)

为啥 & 0x7FFFFFFFTS 呢 ,  为了获得一个整形

> 没啥道理

# map类型扩张



# concurrenthashmap

