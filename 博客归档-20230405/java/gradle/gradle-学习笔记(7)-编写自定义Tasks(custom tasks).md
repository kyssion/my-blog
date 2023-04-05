好了终于到了重头戏了,gradel最为强大的地方就是可以非常方便的定义task并集成到开发环境中

# 简单的临时任务

gradle 提供在build中直接编写临时task的方法,像下面这样

```groovy
tasks.register("hello") {
    group "task group"
    description "a simple demo task"
    doLast {
        println 'Hello, World!'
    }
}
```

这段代码注册了一个hello task,分配到了task group组里 描述为a simple demo task,作用是打印一个hello,world 到控制台

使用gradle task 命令可以看到我们自定义的task group组下的 hello task

```
Task group tasks
----------------
hello - a simple demo task
```

运行gradle hello 命令可以打印出 hello,world

```
$ gradle hello
> Task :customTask:hello
Hello, World!
BUILD SUCCESSFUL in 1s
1 actionable task: 1 executed
```

# 使用gradle 编程实现任务

其实本质上和简单任务相同,只过使用了gradle声明了一个对象罢了

```groovy
class Greeting extends DefaultTask {  
    String message 
    String recipient
    @TaskAction 
    void sayGreeting() {
        println "${message}, ${recipient}!" 
    }
}
tasks.register("hello", Greeting) { 
    group = 'Welcome'
    description = 'Produces a world greeting'
    message = 'Hello' 
    recipient = 'World'
}
```

> 具体的一看代码就明白了,说两点1.@TaskAction 表明这个是默认的任务方法,如果没有指明就默认使用这个方法  2. DefaultTask 是gradle的默认扩展,gradle还提供了其他的方法,这里不做展开了