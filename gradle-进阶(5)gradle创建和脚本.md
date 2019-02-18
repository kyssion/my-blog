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

