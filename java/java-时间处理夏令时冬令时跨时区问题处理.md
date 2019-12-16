作为一个成熟的编程语言，java自然有一堆方法来解决的时间的问题。有的时候我们会因为对java一些内置的api不是太熟悉，对某个场景不熟悉，导致遇到了棘手的问题。比如这个场景夏令时和冬令时

# 夏令时和冬令时

在做全球性的功能时绝对少不了遇到时区转化，一般情况下使用时间戳+java内置的api就能解决99%的问题，但是如果遇到夏令时或者冬令时的时候这个问题就可能变得不是这么容易。

> 首先记录一下什么是夏令时和冬令时：简单的说在这个世界上的某些国家会规定在某个日期将本国所在的时区发生改变，然后在某个时间将他改回来，进行改变的日期就是夏令时或者冬令时

> 注意：这个概念深层次的东西可以自行用搜索引擎查找相关内容，我这里没有用其他人的那种解释比如夏令时就是把表调快一小时，而是使用修正时区这个概念，这么做是为了方便做下面的解释


# 夏令时和冬令时产生的业务场景

举个例子： 一个实行了夏令时和冬令时的国家在夏令有一个活动，每天11点到1一点参加，为期七天，而这7天正好过了令时变化的这一天， 这样会导致什么问题呢？

因为跨过令时所以跨令时之前一天的12点20分和后一天的12点20分之间相隔的并不是24小时，因为令时的变化携带的时区的变化，因为时区变化了，所以相同的12点20分对应的毫秒数是不同的（毫秒没有时区问题）

所以为期七天这个过程不能简单使用+24小时来处理了，因为这样就可能导致跨令时前是11点到1点，跨令时之后就是12点到2点了

# 怎么解决

java提供了一个非常牛逼的api TimeZone ，专门用来处理时区问题

有两个api

```
TimeZone itemTimeZone = TimeZone.getTimeZone(时区名);
itemTimeZone.getOffset(long data);//显示当前时区和0时区的偏移量,和令时制相关
itemTimeZone.getRawOffset();//显示当前时区和0时区的偏移量,和令时制无关
```

这样就很简单了,使用这两个api如果返回的值不相等,就说明当前时间处于某一个令时中

# 进阶一下,解决一下上面的需求,跨令时的时候保证日期是+1的

这里就不说这么做了,直接上代码,其实就是一个很简单的算法题了

```java

public class ScopeTimeDO {
    //开始时间
    private Long startTime;
    // 结束时间
    private Long endTime;
    // 循环次数 , 活动持续天数
    private Integer cycleCount;
}

/**
* 
* @param scopeTimeDO 活动时间数据
* @param timeZeno 时区信息 比如"Europe/Madrid"
* @return 返回活动基于持续天数构造的毫秒时间序列
*/
public List<long[]> createTimeInterval(ScopeTimeDO scopeTimeDO,String timeZeno) {
    long startTime = scopeTimeDO.getStartTime();
    long endTime = scopeTimeDO.getEndTime();
    int cycleCount = scopeTimeDO.getCycleCount();
    int speed = 0;
    TimeZone itemTimeZone = TimeZone.getTimeZone(timeZeno);
    List<long[]> timeList = new ArrayList<>();
    while (cycleCount >=TIME_SCOPE_CYCLE_COUNT_DEFAULT_VALUE) {
        long[] item = new long[2];
        if(speed==0){
            item[0] = startTime;
            item[1] = endTime;
            speed = 1;
        }else{
            long[] last = timeList.get(timeList.size()-1);
            long beforeStartP = itemTimeZone.getOffset(last[0]);
            long beforeEndP = itemTimeZone.getOffset(last[1]);
            item[0] = last[0]+DAY;
            item[1] = last[1]+DAY;
            long nowStartP = itemTimeZone.getOffset(item[0]);
            long nowEndP = itemTimeZone.getOffset(item[1]);
            item[0] = item[0] + (beforeStartP-nowStartP);
            item[1] = item[1] + (beforeEndP-nowEndP);
        }
        cycleCount--;
        timeList.add(item);
    }
    return timeList;
}
```

