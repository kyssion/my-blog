# 堆

- －Xms和—Xmx

堆的最小值 & 堆的最大值
默认值是物理内存的1/4(<1GB) & 默认值是物理内存的1/64(<1GB)
空余堆内存小于40%时，JVM就会增大堆直到-Xmx的最大限制;
空余堆内存大于70%时，JVM会减少堆直到 -Xms的最小限制;
通常会将 -Xms 与 -Xmx两个参数配置相同的值，目的是为了能够在java垃圾回收机制清理完堆区后不需要重新分隔计算堆区的大小而浪费资源。

# 新生代

- -Xmn

设置新生代大小。值＝eden+ 2 survivor

sun公司推荐大小
整个java堆的3/8

- -XX:NewRatio

新生代（eden+2*Survivor）和老年代（不包含永久区）的比值

- -XX:SurvivorRatio（幸存代）

设置Eden:1个Survivor内存空间大小的比值

- -XX:NewSize

设置年轻代大小

- -XX:MaxNewSize

设置年轻代最大值

# 栈

- －Xss

栈容量（ps：－Xoss用于设定本地方法栈大小，但是对于HotSpot来说不起作用，因为其不区分本地方法栈和虚拟机栈）
JDK5.0以后每个线程堆栈大小为1M

# 方法区

- －XX：PermSize

方法区大小

- －XX：MaxPermSize

最大方法区大小

ps：方法区大小和最大方法区大小限制了常量池的容量

# 其它

- －XX：＋PrintGCDetails

打印GC日志

- －XX：＋/-UseTLAB

是否使用本地线程分配缓存

# 了解参数

- -XXThreadStackSize

设置线程栈的大小(0 means use default stack size)

- -XXThreadStackSize

设置内存页的大小，不可设置过大，会影响Perm的大小

- -XX:+UseFastAccessorMethods

设置原始类型的快速优化

- -XX:+DisableExplicitGC
设置关闭System.gc()(这个参数需要严格的测试)
-XX:MaxTenuringThreshold
设置垃圾最大年龄。如果设置为0的话,则年轻代对象不经过Survivor区,直接进入年老代. 对于年老代比较多的应用,可以提高效率。如果将此值设置为一个较大值,则年轻代对象会在Survivor区进行多次复制,这样可以增加对象再年轻代的存活时间,增加在年轻代即被回收的概率。该参数只有在串行GC时才有效.
-XX:+AggressiveOpts
加快编译
-XX:+UseBiasedLocking
锁机制的性能改善
-Xnoclassgc
禁用垃圾回收
-XX:SoftRefLRUPolicyMSPerMB
设置每兆堆空闲空间中SoftReference的存活时间，默认值是1s 。（softly reachable objects will remain alive for some amount of time after the last time they were referenced. The default value is one second of lifetime per free megabyte in the heap）
-XX:PretenureSizeThreshold
设置对象超过多大时直接在旧生代分配，默认值是0。
-XX:TLABWasteTargetPercent
设置TLAB占eden区的百分比，默认值是1% 。
-XX:+CollectGen0First
设置FullGC时是否先YGC，默认值是false。

————————————————

版权声明：本文为CSDN博主「iCoding91」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。

原文链接：https://blog.csdn.net/caoxiaohong1005/article/details/82931474