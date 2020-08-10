> 针对jdk11+ 

> map类型操作最核心的就是这些方法get(),put(),contain(),computeIfAbsent(), 我们只解析这些方法如何实现

> 有一些核心点逻辑 , resize()(扩容逻辑) 散列值计算获取逻辑

> map类型有一些通用的逻辑操作,统一梳理

> 最为解析的map类型是 HashMap Hashtable TreeMap WeakHashMap LinkedHashMap ConcurrentHashMap

# map类型散列值计算

典型Map类型|hash计算逻辑|下标计算逻辑
---|---|---
HashTable| key的hash| (hash & 0x7FFFFFFF) % tab.length
HashMap| (h = key.hashCode()) ^ (h >>> 16)| hash&(table长度-1)
ConurrentHashMap| (h ^ (h >>> 16)) & 0x7FFFFFFFTS|hash&(table长度-1)

为啥 & 0x7FFFFFFFTS 呢 ,  为了获得一个整形

> 没啥道理


# map类型get方法

> hashMap

```java
final Node<K,V> getNode(int hash, Object key) {
    Node<K,V>[] tab; Node<K,V> first, e; int n; K k;
    if ((tab = table) != null && (n = tab.length) > 0 &&
        (first = tab[(n - 1) & hash]) != null) {
        // 如果本hashkey命中了第一个地方并且hashcode 相同 , 并且key 命中了
        //其中 first.hash 一定等于 hash -> 因为添加的逻辑中就是这么指定的
        if (first.hash == hash && // always check first node
            ((k = first.key) == key || (key != null && key.equals(k))))
            return first;
        if ((e = first.next) != null) {
            //如果是红黑树(链表长度大于8 自动变成红黑树)-> 使用红黑树遍历
            if (first instanceof TreeNode)
                return ((TreeNode<K,V>)first).getTreeNode(hash, key);
            //否则使用的for循环遍历链表
            do {
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    return e;
            } while ((e = e.next) != null);
        }
    }
    return null;
}
```
# map类型put方法

```java
final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
                boolean evict) {
    Node<K,V>[] tab; Node<K,V> p; int n, i;
    if ((tab = table) == null || (n = tab.length) == 0)
        n = (tab = resize()).length;
    if ((p = tab[i = (n - 1) & hash]) == null)
        tab[i] = newNode(hash, key, value, null);
    else {
        Node<K,V> e; K k;
        if (p.hash == hash &&
            ((k = p.key) == key || (key != null && key.equals(k))))
            e = p;
        else if (p instanceof TreeNode)
            e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
        else {
            for (int binCount = 0; ; ++binCount) {
                if ((e = p.next) == null) {
                    p.next = newNode(hash, key, value, null);
                    if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                        treeifyBin(tab, hash);
                    break;
                }
                if (e.hash == hash &&
                    ((k = e.key) == key || (key != null && key.equals(k))))
                    break;
                p = e;
            }
        }
        if (e != null) { // existing mapping for key
            V oldValue = e.value;
            if (!onlyIfAbsent || oldValue == null)
                e.value = value;
            afterNodeAccess(e);
            return oldValue;
        }
    }
    ++modCount;
    // 超过阀值就是 扩张
    if (++size > threshold)
        resize();
    afterNodeInsertion(evict);
    return null;
}
```




# map类型扩张

因为hash散列的问题 , 所有基于table构建的hashmap 都是按照2的N次方进行扩容 , 之所以是2的N次方是方便hash散列 , 让散列更加均匀

> hashMap 的扩张逻辑

两个变量 , 1. DEFAULT_INITIAL_CAPACITY -> 默认容量 2. threshold -> 默认的阀值(这个是值是默认的容量*负载系数)

```java
final Node<K,V>[] resize() {
    Node<K,V>[] oldTab = table;
    //老数组的容量
    int oldCap = (oldTab == null) ? 0 : oldTab.length;
    //之前的容量系数
    int oldThr = threshold;
    int newCap, newThr = 0;
    if (oldCap > 0) {
        if (oldCap >= MAXIMUM_CAPACITY) {
            threshold = Integer.MAX_VALUE;
            return oldTab;
        }
        else if ((newCap = oldCap << 1) < MAXIMUM_CAPACITY &&
                    oldCap >= DEFAULT_INITIAL_CAPACITY)
            newThr = oldThr << 1; // double threshold
    }

    // 这段逻辑是为了如果指定了 默认的容量的情况下会 将newCap赋值成默认的oldThr(2的次幂)
    else if (oldThr > 0) // initial capacity was placed in threshold
        newCap = oldThr;
    else {               // zero initial threshold signifies using defaults
        newCap = DEFAULT_INITIAL_CAPACITY;
        newThr = (int)(DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY);
    }
    // 配合指定的了默认容积的逻辑 , 用于初始化默认的容量上限
    if (newThr == 0) {
        float ft = (float)newCap * loadFactor;
        newThr = (newCap < MAXIMUM_CAPACITY && ft < (float)MAXIMUM_CAPACITY ?
                    (int)ft : Integer.MAX_VALUE);
    }
    threshold = newThr;
    @SuppressWarnings({"rawtypes","unchecked"})
    Node<K,V>[] newTab = (Node<K,V>[])new Node[newCap];
    table = newTab;
    @SuppressWarnings({"rawtypes","unchecked"})
    Node<K,V>[] newTab = (Node<K,V>[])new Node[newCap];
    table = newTab;
    if (oldTab != null) {
        for (int j = 0; j < oldCap; ++j) {
            Node<K,V> e;
            if ((e = oldTab[j]) != null) {
                oldTab[j] = null;
                if (e.next == null)
                    newTab[e.hash & (newCap - 1)] = e;
                else if (e instanceof TreeNode)
                    ((TreeNode<K,V>)e).split(this, newTab, j, oldCap);
                // todo 这个地方就是两点
                else { // preserve order
                //扩张之后 ,如果一个节点是node类型的时候 , 会有两种情况
                // 1. 还是在原来的位置 2. 在原来的位置偏移的位置
                // 量中情况取决于 oldCap位置时候是1
                // 如果是1 的 情况下, 新的节点必然是 j+oldCap 反之就是当前位置
                // 这个原因是因为下标的计算逻辑
                    Node<K,V> loHead = null, loTail = null;
                    Node<K,V> hiHead = null, hiTail = null;
                    Node<K,V> next;
                    do {
                        next = e.next;
                        if ((e.hash & oldCap) == 0) {
                            if (loTail == null)
                                loHead = e;
                            else
                                loTail.next = e;
                            loTail = e;
                        }
                        else {
                            if (hiTail == null)
                                hiHead = e;
                            else
                                hiTail.next = e;
                            hiTail = e;
                        }
                    } while ((e = next) != null);
                    if (loTail != null) {
                        loTail.next = null;
                        newTab[j] = loHead;
                    }
                    if (hiTail != null) {
                        hiTail.next = null;
                        newTab[j + oldCap] = hiHead;
                    }
                }
            }
        }
    }
    return newTab;
}
```

> ConcurrentHashMap 扩张逻辑