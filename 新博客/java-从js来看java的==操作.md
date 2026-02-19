在风中凌乱... ...

最近看了一个问题如何在js中让下面的这个表达式返回true

```JavaScript
a==1&&a==2
```

答案

```javaScript
let a={
    index : 0,
    valueOf:function(){
        this.index++;
        return this.index;
    }
};
```

其实这个方法是利用了js的语法规则, js应为是弱类型编程语言,所以它的== 操作其实是需要进行数值导出的
默认的过程是先valueOf 然后是 toString

# java是不是类似的呢?

答案是否定的... java对非基本类型直接使用内存地址进行比较

如果需要特殊的比较方法,需要重写equel方法来达到目的
