其实对于任何一种构建工具来说，针对文件操作的功能是必不可少的，这里整理一下gradle针对文件提供的功能

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

