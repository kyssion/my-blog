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
task ('mycopy',Copy){
    from (file('srcDir'))
    into(buildDir)
}
```

除此之外我们还能使用tasks组的方法创建对应的任务

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

## 定位到指定的任务

> 其实本质上，gradle将一个个任务抽象成一个一个的变量，这样我们就能在使用的时候直接使用变量名成引用就能实现

```groovy
task hello
task copy(type: Copy)

// Access tasks using Groovy dynamic properties on Project

println hello.name
println project.hello.name

println copy.destinationDir
println project.copy.destinationDir
```

> 或者使用按路径和名称的方法，获取一个task

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

> 使用组的方法获取一个变量

```groovy
task hello
task copy(type: Copy)

println tasks.hello.name
println tasks.named('hello').get().name

println tasks.copy.destinationDir
println tasks.named('copy').get().destinationDir
```

## gradle 任务的变量化操作

之前说过在gradle 中 所有的任务都可以抽象成变量，这里写一个例子来表明这个观点

```groovy
task ('myCopy',Copy){
    from (file('srcDir'))
    into(buildDir)
}

Copy myCopy = tasks.getByName("myCopy")
myCopy.from 'resources'
myCopy.into 'target'
myCopy.include('**/*.txt', '**/*.xml', '**/*.properties')
```

我们声明了一个类型是Copy，名称时myCopy的task，接下来使用方法动态的获取这个task并对他进行一定的修改操作

## 定义一个自定义任务

之前整理过，在gradle中我们其实可以生命一个task类型，方法如下

```groovy
class CustomTask extends DefaultTask {
    final String message
    final int number

    @Inject
    CustomTask(String message, int number) {
        this.message = message
        this.number = number
    }
}
```

通过继承DefaultTask类，我们可以动态的声明一个task

在使用的时候可以使用如下两种发法定义任务

```groovy
tasks.create('myTask', CustomTask, 'hello', 42)//使用task创建
```

我们指定了名称和类型，最后的两个参数将会传入构造函数中，但是在gradle中，如果要使用构造函数传递参数，那么必须使用@Inject注解

```groovy
task myTask(type: CustomTask, constructorArgs: ['hello', 42])
```

这个方法就很明确了,直接使用type和constructorArgs字段定义要使用的参数类型是啥

## gradle task的依赖

之前我们整理了task依赖，使用dependsOn字段，指明依赖见下面的例子

```groovy
//taskX 依赖 taskY
project('projectA') {
    task taskX {
        dependsOn ':projectB:taskY'
        doLast {
            println 'taskX'
        }
    }
}
project('projectB') {
    task taskY {
        doLast {
            println 'taskY'
        }
    }
}
//在外部使用编程的方式指定依赖
task taskX {
    doLast {
        println 'taskX'
    }
}

task taskY {
    doLast {
        println 'taskY'
    }
}

taskX.dependsOn taskY
```

这里扩展一个gradle 依赖处理的高级用法，动态添加依赖

```groovy
task taskX {
    doLast {
        println 'taskX'
    }
}
// Using a Groovy Closure
taskX.dependsOn {
    tasks.findAll { task -> task.name.startsWith('lib') }
}
task lib1 {
    doLast {
        println 'lib1'
    }
}
task lib2 {
    doLast {
        println 'lib2'
    }
}
task notALib {
    doLast {
        println 'notALib'
    }
}
```

这个方法通过groovy的扩展方法，指定了所有名称有lib前缀的task都是他的依赖

## gradle 任务运行时排序

两个关键字 shouldAfterRun mustAfterRun

一个例子：

```groovy
task taskX {
    doLast {
        println 'taskX'
    }
}
task taskY {
    doLast {
        println 'taskY'
    }
}
task taskZ {
    doLast {
        println 'taskZ'
    }
}
taskX.dependsOn taskY
taskY.dependsOn taskZ
taskZ.shouldRunAfter taskX
```

shouldRunAfter 指定的是这些任务应该按照指定的顺序执行
mustRunAfter 表示必须按照指定的顺序执行

上面的例子中会按照 taskz -> taskY->taskx 的顺序执行，如果使用了mustRunAfter将会报错

## gradle 最终任务

使用finalizedBy字段描述执行器的最终任务，这个任务将不论定义放是否执行成功，最终都将会执行

```groovy
task taskX {
    doLast {
        println 'taskX'
        throw new RuntimeException()
    }
}
task taskY {
    doLast {
        println 'taskY'
    }
}

taskX.finalizedBy taskY
```

## gradle task的描述，替换，和跳过执行，启用，禁用，超时时间操作

gradle 针对任务提供了大量的操作性功能

1. 使用description

```groovy
description 'Copies the resource directory to the target directory.'
```

2. 同名覆盖操作

如果自己命名的task与系统中或者自己定义的其他task重名，那么可以使用这种方法进行覆盖

```groovy
task copy(type: Copy)
task copy(overwrite: true) {
    doLast {
        println('I am the new one.')
    }
}
```

3. 跳过执行操作

> 在这里gradle 提供了两个方法跳过执行操作，第一种，使用哦onlyIf 关键字 指定只在什么情况下才会执行对应的任务

```groovy
task hello {
    doLast {
        println 'hello world'
    }
}
hello.onlyIf { !project.hasProperty('skipHello') }
```

> 第二种，在程序执行的过程中抛出 stopExecutionException异常，终止这个调用链操作

```groovy
task compile {
    doLast {
        println 'We are doing the compile.'
    }
}
compile.doFirst {
    // Here you would put arbitrary conditions in real life.
    // But this is used in an integration test so we want defined behavior.
    if (true) { throw new StopExecutionException() }
}
task myTask {
    dependsOn('compile')
    doLast {
        println 'I am not affected'
    }
}
```

4. 启用禁用设置超时时间这些gradle操作，我用一个例子来解释吧

> 启用禁用操作
```groovy
task disableMe {
    doLast {
        println 'This should not be printed if the task is disabled.'
    }
}
disableMe.enabled = false
```

> 超时时间

```groovy
task hangingTask() {
    doLast {
        Thread.sleep(100000)
    }
    timeout = Duration.ofMillis(500)
}
```

## gradle 任务组级别全局规则注入

```groovy
tasks.addRule("Pattern: ping<ID>") { String taskName ->
    if (taskName.startsWith("ping")) {
        task(taskName) {
            doLast {
                println "Pinging: " + (taskName - 'ping')
            }
        }
    }
}
task groupPing {
    dependsOn pingServer1, pingServer2
}
```

## gradle的project 和 其他信息



## 生命周期任务