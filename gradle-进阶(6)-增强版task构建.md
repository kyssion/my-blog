# 增强版task构建

之前的一篇文章整理gradle task的一个简单创建，这里整理一下task的高级应用方法

# 任务的定义方法

## 如果是简单的任务我们可以这样进行定义

```groovy
task hello{
    doLast{
        println "hello world!"
    }
}
task ("hello"){
    println "hello world!"
}
```

## 或者指定任务的类型（继承原有的任务）

```groovy
task('copy', type: Copy) {
    from(file('srcDir'))
    into(buildDir)
}
```

这种方法，后面的type 字段其实是可以省略的

```groovy
task ('copy',Copy){
    from (file('srcDir'))
    into(buildDir)
}
```

## 使用api 搜索到任务

