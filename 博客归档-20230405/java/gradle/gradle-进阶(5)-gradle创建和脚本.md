通过之前的入门学习，一个gradle构建可以理解成有一个或者多个task组成，这里简单回顾一下gradle脚本如何构建一个简单的task

# 使用gradle脚本创建一个简单的task

在build.gradle 文件夹中写入一个任务

```groovy
task hello {
    doLast {
        println 'Hello world!'
    }
}
```

这个task的作用很简单就是输出一个hello world 字符串

> 引申:如果使用过ant的话那么可以理解gradle task就是ant中的目标

# gradle构建脚本高级玩法

## 1. 可以使用局部变量

其实就是在gradle的task脚本中可以声明变量供下面引用

```groovy
task upper {
    doLast {
        String someString = 'mY_nAmE'
        println "Original: $someString"
        println "Upper case: ${someString.toUpperCase()}"
    }
}
```

## gradle 依赖性脚本使用

如果使用依赖字段dependsOn 关键子的时候,系统将会先运行此字段对应的task

```groovy
task hello {
    doLast {
        println 'Hello world!'
    }
}
task intro {
    dependsOn hello 
    doLast {
        println "I'm Gradle"
    }
}
```

### gralde使用编程方法批量添加task，和动态添加依赖

```groovy
//使用time函数统一的批量添加处理函数
4.times { counter ->
    task "task$counter" {
        doLast {
            println "I'm task number $counter"
        }
    }
}
//动态以来添加
task0.dependsOn task2,task3
```

> 引申一下这个动态依赖添加 ： 在上面的例子中，如果运行了task0 将会先与性task2和task3 然后再运行task0，在更强大的方法见下面的例子

### gradle 使用api访问任务

```groovy
task hello {
    doLast {
        println 'Hello Earth'
    }
}
hello.doFirst {
    println 'Hello Venus'
}
hello.configure {
    doLast {
        println 'Hello Mars'
    }
}
hello.configure {
    doLast {
        println 'Hello Jupiter'
    }
}
```

运行的结果如下

```groovy
gradle -q hello
> gradle -q hello
Hello Venus
Hello Earth
Hello Mars
Hello Jupiter
```

### 动态获取tash属性的方法

这个方法的使用需要配合gradle api使用的

```groovy
task hello {
    ext.hhh="123123"
    doLast {
        println 'Hello world!'
    }
}
hello.doLast {
    println "Greetings from the $hello.name task. info is $hello.hhh"
}
```

在这个方法中，使用$hello.name获取到了这个任务的名称,使用ext.xxx 定义了一个变量的名称，兵使用hello.xxx 调用了这个变量的名称

### gradle build文件中使用方法

```groovy
task checksum {
    doLast {
        fileList('./antLoadfileResources').each { File file ->
            ant.checksum(file: file, property: "cs_$file.name")
            println "$file.name Checksum: ${ant.properties["cs_$file.name"]}"
        }
    }
}

task loadfile {
    doLast {
        fileList('./antLoadfileResources').each { File file ->
            ant.loadfile(srcFile: file, property: file.name)
            println "I'm fond of $file.name"
        }
    }
}

File[] fileList(String dir) {
    file(dir).listFiles({file -> file.isFile() } as FileFilter).sort()
}
```

我们这里使用了groovy与语法声明了一个函数，并且在我们自己定义的任务中使用这些函数

### 指定默认的task

默认的task 的使用方法就是调用 gradle 命令将会默认运行的方法，使用defaultTasks 定义

```groovy
defaultTasks 'clean', 'run'
task clean {
    doLast {
        println 'Default Cleaning!'
    }
}
task run {
    doLast {
        println 'Default Running!'
    }
}
task other {
    doLast {
        println "I'm not a default task!"
    }
}
```

### gradle控制执行阶段简单实例

```groovy
task distribution {
    doLast {
        println "We build the zip with version=$version"
    }
}

task release {
    dependsOn 'distribution'
    doLast {
        println 'We release now'
    }
}

gradle.taskGraph.whenReady { taskGraph ->
    if (taskGraph.hasTask(":release")) {
        version = '1.0'
    } else {
        version = '1.0-SNAPSHOT'
    }
}
```

输出信息

```groovy
root@gradle-demo$ gradle distribution

> Task :distribution
We build the zip with version=1.0-SNAPSHOT

BUILD SUCCESSFUL in 0s
1 actionable task: 1 executed

root@gradle-demo$ gradle release

> Task :distribution
We build the zip with version=1.0

> Task :release
We release now

BUILD SUCCESSFUL in 0s
2 actionable tasks: 2 executed
```

在上面的例子中我们使用了 taskGraph方法来在gradle的配置过程中（还有一个是运行过程）动态改变 变量（version）的方法

### 添加外部依赖的方法

这个点应该大家都很熟悉了

```groovy
import org.apache.commons.codec.binary.Base64

buildscript {
    repositories {
        mavenCentral()
    }
    dependencies {
        classpath group: 'commons-codec', name: 'commons-codec', version: '1.2'
    }
}

task encode {
    doLast {
        def byte[] encodedString = new Base64().encode('hello world\n'.getBytes())
        println new String(encodedString)
    }
}
```

> 这里groovy 提供了非常强大的功能，我们可以在代码中直接使用gradle 引用的代码（例子中的task定义）

> 我们这里里一定要注意import这个包，idea框架并不会自动提示

我们使用命令 gradle encode 将会有如下的输出

```
> Task :encode
aGVsbG8gd29ybGQK

BUILD SUCCESSFUL in 0s
1 actionable task: 1 executed
18:16:26: Task execution finished 'encode'.
```

