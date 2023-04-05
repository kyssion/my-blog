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

gradle推荐使用 ProjectLayout.files（java.lang.Object ...）方法获取文件集合，本方法返回一个FileCollection实例，此方法非常灵活，允许您传递多个字符串，File实例，字符串集合，Files 集合等

```groovy
FileCollection collection = layout.files('src/file1.txt',
                                  new File('src/file2.txt'),
                                  ['src/file3.csv', 'src/file4.csv'],
                                  Paths.get('src', 'file5.txt'))
```

这里写一个例子在指定的目录下寻找文件

```groovy
task list {
    doLast {
        File srcDir
        // Create a file collection using a closure
        FileCollection collection = layout.files { srcDir.listFiles() }

        srcDir = file('src')
        println "Contents of $srcDir.name"
        collection.collect { relativePath(it) }.sort().each { println it }

        srcDir = file('src2')
        println "Contents of $srcDir.name"
        collection.collect { relativePath(it) }.sort().each { println it }
    }
}
```

> 文件集合的一些操作

1. 改变集合类型

```groovy
Set set = collection.files
Set set2 = collection as Set
List list = collection as List
String path = collection.asPath
File file = collection.singleFile
```

2. 集合间进行集合操作

```groovy
def union = collection + layout.files('src/file2.txt')
def difference = collection - layout.files('src/file2.txt')
```

groovy 使用+ 表示union操作 使用 - 表示 defference操作

注意如果使用这些集合方法无法满足要求，需要使用filter方法来对集合进行过滤操作

```groovy
FileCollection textFiles = collection.filter { File f ->
    f.name.endsWith(".txt")
}
```

## 文件树

和文件的区别，其实本质上文件树是文件集合的一种延伸，不过文件树保留了树状结构

1. 创建文件树

简单方法

```groovy
// Create a file tree with a base directory
ConfigurableFileTree tree = fileTree(dir: 'src/main')
// Add include and exclude patterns to the tree
tree.include '**/*.java'
tree.exclude '**/Abstract*'
// Create a tree using closure
tree = fileTree('src') {
    include '**/*.java'
}
// Create a tree using a map
tree = fileTree(dir: 'src', include: '**/*.java')
tree = fileTree(dir: 'src', includes: ['**/*.java', '**/*.xml'])
tree = fileTree(dir: 'src', include: '**/*.java', exclude: '**/*test*/**')
```

从zip或者tar中创建文件树

```groovy
// Create a ZIP file tree using path
FileTree zip = zipTree('someFile.zip')
// Create a TAR file tree using path
FileTree tar = tarTree('someFile.tar')
//tar tree attempts to guess the compression based on the file extension
//however if you must specify the compression explicitly you can:
FileTree someTar = tarTree(resources.gzip('someTar.ext'))
```

> 引申：文件集合（包括文件树，作为参数进行传递的时候的处理方法）

在gradle 中，很多时候source——资源被解释称一个文件目录或者一个文件集合，如果传入的参数是一个文件集合如JavaCompile任务有一个source属性

在gradle中souce属性可以有很多不同的表现形式，比如下面的例子

```groovy
task compile(type: JavaCompile) {

    // Use a File object to specify the source directory
    source = file('src/main/java')

    // Use a String path to specify the source directory
    source = 'src/main/java'

    // Use a collection to specify multiple source directories
    source = ['src/main/java', '../shared/java']

    // Use a FileCollection (or FileTree in this case) to specify the source files
    source = fileTree(dir: 'src/main/java').matching { include 'org/gradle/api/**' }

    // Using a closure to specify the source files.
    source = {
        // Use the contents of each zip file in the src dir
        file('src').listFiles().findAll {it.name.endsWith('.zip')}.collect { zipTree(it) }
    }
}
```





2. 使用文件树

```groovy
// Iterate over the contents of a tree
tree.each {File file ->
    println file
}
// Filter a tree
FileTree filtered = tree.matching {
    include 'org/gradle/api/**'
}
// Add trees together
FileTree sum = tree + fileTree(dir: 'src/test')
// Visit the elements of the tree
tree.visit {element ->
    println "$element.relativePath => $element.file"
}
```



# 文件复制

gradle 提供copy task 实现文件复制的相关功能

> copy需要的参数信息

1. from into方法表示文件的复制来源和输出来源，注意这些属性的参数都可以是集合或者文件目录
```groovy
task anotherCopyTask (type: Copy) {
    // Copy everything under src/main/webapp
    from 'src/main/webapp'
    // Copy a single file
    from 'src/staging/index.html'
    // Copy the output of a task
    from copyTask
    // Copy the output of a task using Task outputs explicitly.
    from copyTaskWithPatterns.outputs
    // Copy the contents of a Zip file
    from zipTree('src/main/assets.zip')
    // Determine the destination directory later
    into { getDestDir() }
}
```

2. include exclude 选择性过滤方法

```groovy
task copyTaskWithPatterns (type: Copy) {
    from 'src/main/webapp'
    into "$buildDir/explodedWar"
    include '**/*.html'
    include '**/*.jsp' //包含文件
    exclude { FileTreeElement details -> // 剔除文件
        details.file.name.endsWith('.html') &&
            details.file.text.contains('DRAFT')
    }
}
```

3. 重命名文件 rename方法

gradle 提供了两种方法，进行重命名文件

-  使用过滤器

```groovy
// Use a closure to convert all file names to upper case
rename { String fileName ->
    fileName.toUpperCase()
}
```

- 使用正则表达式

```groovy
// Use a regular expression to map the file name
rename '(.+)-staging-(.+)', '$1$2'
rename(/(.+)-staging-(.+)/, '$1$2')
```

> copy文件使用模板方法

Gradle提供的一个解决方案是Project.copySpec（org.gradle.api.Action）方法。这允许您在任务之外创建复制规范，然后可以使用CopySpec.with（org.gradle.api.file.CopySpec ...）方法将其附加到适当的任务。

```groovy
CopySpec webAssetsSpec = copySpec {
    from 'src/main/webapp'
    include '**/*.html', '**/*.png', '**/*.jpg'
    rename '(.+)-staging(.+)', '$1$2'
}

task copyAssets (type: Copy) {
    into "$buildDir/inPlaceApp"
    with webAssetsSpec
}

task distApp(type: Zip) {
    archiveFileName = 'my-app-dist.zip'
    destinationDirectory = file("$buildDir/dists")

    from appClasses
    with webAssetsSpec
}
//共享使用内置模式

task copyAppAssets(type: Copy) {
    into "$buildDir/inPlaceApp"
    from 'src/main/webapp', webAssetPatterns
}
```

> 任务中添加复制功能

```groovy
task copyMethodWithExplicitDependencies {
    // up-to-date check for inputs, plus add copyTask as dependency
    inputs.files copyTask
    outputs.dir 'some-dir' // up-to-date check for outputs
    doLast{
        copy {
            // Copy the output of copyTask
            from copyTask
            into 'some-dir'
        }
    }
}
```

> sync方法将复制目录和被copy目录同步

简单点说就是如果复制的时候少了几个文件，那么复制结束后，被复制的文集夹将会删除这些文件，其他的用法和gradle相同

```groovy
task libs(type: Sync) {
    from configurations.runtime
    into "$buildDir/libs"
}
```

> 其实这个方法是继承自copy中的，和copy的使用方法相同

> 常见用法例子

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

> 一个复杂的复制构建例子

```groovy
task nestedSpecs(type: Copy) {
    into "$buildDir/explodedWar"
    exclude '**/*staging*'
    from('src/dist') {
        include '**/*.html', '**/*.png', '**/*.jpg'
    }
    from(sourceSets.main.output) {
        into 'WEB-INF/classes'
    }
    into('WEB-INF/lib') {
        from configurations.runtimeClasspath
    }
}
```

> 这个例子是将 src/dist中的所有html png jpg文件 添加到 $buildDir/explodeWar文件夹中，而output和 classpath中的所有文件将会考到指定的文件夹中

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