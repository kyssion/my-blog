其实对于任何一种构建工具来说，针对文件操作的功能是必不可少的，这里整理一下gradle针对文件提供的功能

# gradle 中的文件路径

1. gradle 的 Project.file方法

作用： 指定单个文件或者目录的位置，解析规则（相对路径相对于项目目录进行解析，而绝对路径保持不变）。

例子：
```groovy
// 使用相对路径
File configFile = file('src/config.xml')

//使用绝对路径
configFile = file(configFile.absolutePath)

```

> 注意：gradle不可使用new File(relative path) 这个方法，），因为new File（relative）会创建相对与运行时的（当时的）路径，gradle不能保证运行时路径相同（内部的守护任务可能会切换路径）

2. Project.getRootDir 

作用： 获取项目的根路径

例子：

```groovy
File configFile = file("$rootDir/shared/config.xml")
```

# gradle 文件操作

## 文件集合

gradle这么定义文件集合的-就是一组文件，不考虑目录什么

获取文件集合

gradle推荐使用 ProjectLayout.files（java.lang.Object ...）方法获取文件集合，本方法返回一个FileCollection实例





# 文件复制

gradle 提供copy task 实现文件复制的相关功能

1. 单文件复制

```groovy
//标准写法
task copyReport(type: Copy) {
    from file("$buildDir/reports/my-report.pdf")
    into file("$buildDir/toArchive")
}

//省略一定的标记
task copyReport2(type: Copy) {
    from "$buildDir/reports/my-report.pdf"
    into "$buildDir/toArchive"
}

//可以使用使用变量
task copyReport3(type: Copy) {
    from myReportTask.outputFile
    into archiveReportsTask.dirToArchive
}
```

2. 多文件复制

```groovy
//简单的多文件添加
task copyReportsForArchiving(type: Copy) {
    from "$buildDir/reports/my-report.pdf", "src/docs/manual.pdf"
    into "$buildDir/toArchive"
}

//--------
// 使用include指定复制规则
//指定目录下所有标记开始的文件（不递归查询）
task copyPdfReportsForArchiving(type: Copy) {
    from "$buildDir/reports"
    include "*.pdf"
    into "$buildDir/toArchive"
}
//指定目录下的所有文件（符合模糊表达式就复制，携带目录）
task copyAllPdfReportsForArchiving(type: Copy) {
    from "$buildDir/reports"
    include "**/*.pdf"
    into "$buildDir/toArchive"
}
//--------
//使用内连include 指定复制格式（之前的方法不会复制reports目录使用这种方法可以复制reports目录）
//使用exclude剔除 exe后缀的文件
task copyReportsDirForArchiving2(type: Copy) {
    from("$buildDir") {
        include "reports/**"
        exclude "**/*.exe"
    }
    into "$buildDir/toArchive"
}
```

> 注意一点，使用**/*.java的时候会复制目录结构，包括不包含指定文件的目录结构

> include 指令，如果写在外面就是针对整个copy过程都适用，如果是在from中编写，就只针对这个from语句适用

# zip 压缩文件

```groovy
plugins {
    id 'base'
}

version = "1.0.0"

task packageDistribution(type: Zip) {
    archiveFileName = "my-distribution.zip"//压缩的名称
    destinationDirectory = file("$buildDir/dist")//打包目的地
    // 文件过滤添加逻辑
    from("$buildDir/toArchive") {
        exclude "**/*.pdf"
    }

    from("$buildDir/toArchive") {
        include "**/*.pdf"
        into "docs"
    }
}
```

> 注意一点，使用**/*.java的时候会复制目录结构，包括不包含指定文件的目录结构
> include 指令，不同于copy，只能在from中编写，针对这个from语句适用

## 解压缩

```groovy
task unpackFiles(type: Copy) {
    from zipTree("src/resources/thirdPartyResources.zip")//压缩包的地址
    into "$buildDir/resources"// 解压到
}
```

> 普通副本一样，您可以控制哪些文件通过过滤器解压缩，甚至在解压缩时重命名文件。
> 注意zipTree 方法同样适用 Jar 和 war ear

> 能力提升，将环境中所有的jar class 文件都统一到编译之后的jar包中方法很简单（jar任务使用zipTree打包）

> ps暂时没有成功

```groovy
plugins {
    id 'java'
}

version = '1.0.0'

repositories {
    mavenCentral()
}

dependencies {
    implementation 'commons-io:commons-io:2.6'
}

task uberJar(type: Jar) {
    archiveClassifier = 'uber'

    from sourceSets.main.output

    dependsOn configurations.runtimeClasspath
    from {
        configurations.runtimeClasspath.findAll { it.name.endsWith('jar') }.collect { zipTree(it) }
    }
}
```

## 文件移动

> Gradle没有用于移动文件和目录的API，但您可以使用Apache Ant集成轻松地执行此操作，如以下示例所示：

```groovy
task moveReports {
    doLast {
        ant.move file: "${buildDir}/reports",
                 todir: "${buildDir}/toArchive"
    }
}
```

## 重新命名方法

```groovy
task copyFromStaging(type: Copy) {
    from "src/main/webapp"
    into "$buildDir/explodedWar"

    rename '(.+)-staging(.+)', '$1$2'
}
//gradle 一切皆可编程，看自己的喜欢了
task copyWithTruncate(type: Copy) {
    from "$buildDir/reports"
    rename { String filename ->
        if (filename.size() > 10) {
            return filename[0..7] + "~" + filename.size()
        }
        else return filename
    }
    into "$buildDir/toArchive"
}
```

## 文件删除

```groovy
task myClean(type: Delete) {
    delete buildDir //删除指定目录下的文件
}
//创建删除的过滤逻辑
task cleanTempFiles(type: Delete) {
    delete fileTree("src").matching {
        include "**/*.tmp"
    }
}
```

