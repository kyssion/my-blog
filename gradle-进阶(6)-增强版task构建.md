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

除此之外我们还能使用tasks的方法创建对应的任务

```groovy
tasks.create('hello') {
    doLast {
        println "hello"
    }
}
tasks.create('copy', Copy) {
    from(file('srcDir'))
    into(buildDir)
}
```



## 定位到指定的任务44
其实本质上，gradle将一个个任务抽象成一个一个的变量，这样我们就能在使用的时候直接使用变量名成引用就能实现

```groovy
task hello
task copy(type: Copy)

// Access tasks using Groovy dynamic properties on Project

println hello.name
println project.hello.name

println copy.destinationDir
println project.copy.destinationDir
```

或者使用按路径和名称的方法，获取一个task

```groovy
task testProject{
    println "test item"
}

project(':java-web') {
    task testProject {
        println "sdfsdf"
    }
}
println tasks.getByPath('testProject').path
println tasks.getByPath(':testProject').path
println tasks.getByPath('java-web:testProject').path
println tasks.getByPath(':java-web:testProject').path
```

这里要注意两个地方 首先 project 中指定的路径必须是一个已经定义的gradle子路径，如果没有的话，gradle将会报错。其次是输出的方法就是按照定义的方法进行执行

