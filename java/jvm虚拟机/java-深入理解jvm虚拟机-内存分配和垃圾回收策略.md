> 内存的分配原则

1. **对象优先在Eden分配** : 大多数情况下,对象在新生代Eden区中分配。当Eden区没有足够空间进行分配时,虚拟机将发起一次Minor GC。

2. 大对象直接进入老年代

3. **长期存活的对象将进入老年代** : 对象在Eden出生并经过第一次**Minor GC**后仍然存活,并且能被Survivor容纳的话,将被移动到Survivor空间中,并且对象年龄设为1。对象在Survivor区中每“熬过”一次**Minor GC**,年龄就增加1岁,当它的年龄增加到一定程度(默认为15岁),就将会被晋升到老年代中。对象晋升老年代的年龄阈值,可以通过参数**-XX:MaxTenuringThreshold设置**

4. 动态对象年龄判定 : 虚拟机并不是永远地要求对象的年龄必须达到了**MaxTenuringThreshold**才能晋升老年代,如果在Survivor空间中相同年龄所有对象大小的总和大于Survivor空间的一半,年龄大于或等于该年龄的对象就可以直接进入老年代,无须等到MaxTenuringThreshold中要求的年龄

### java两种位置的gc

-**新生代GC(Minor GC)**:指发生在新生代的垃圾收集动作,因为Java对象大多都具备朝生夕灭的特性,所以Minor GC非常频繁,一般回收速度也比较快。
- **老年代GC(Major GC/Full GC)**:指发生在老年代的GC,出现了Major GC,经常会伴随至少一次的Minor GC(但非绝对的,在Parallel Scavenge收集器的收集策略里就有直接进行Major GC的策略选择过程)。Major GC的速度一般会比Minor GC慢10倍以上。

> Minor GC

大多数情况下,对象在新生代Eden区中分配。当Eden区没有足够空间进行分配时,虚拟机将发起一次Minor GC。   注意这次的gc只是将对象放入一个survive区中，使用标记整理方法，一个survive区空间为0 而另一个空间无碎片。当survive 没有空间的时候将会直接的放入老年代中

> Full gc

在发生Minor GC之前,虚拟机会先检查老年代最大可用的连续空间是否大于新生代所有对象总空间,如果这个条件成立,那么Minor GC可以确保是安全的。如果不成立,则虚拟机会查看HandlePromotionFailure设置值是否允许担保失败。如果允许,那么会继续检查老年代最大可用的连续空间是否大于历次晋升到老年代对象的平均大小,如果大于,将尝试着进行一次Minor GC,尽管这次Minor GC是有风险的;如果小于,或者HandlePromotionFailure设置不允许冒险,那这时也要改为进行一次Full GC。