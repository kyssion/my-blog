这一篇文章是之前的一篇文章gradle命令行相关的记录的文章的延续,主要记录一下gradle的各种环境或者说属性的配置方法

# gradle 各种属性变量的优先级

gradle有五种属性构建优先级,这里将优先级从高到底排序

- 命令行标志如--build-cache.它们优先于属性和环境变量.

系统属性，例如systemProp.http.proxyHost=somehost.org存储在gradle.properties文件中.指的试一些有systemProp前缀的参数

- Gradle属性(例如org.gradle.caching=true通常存储在gradle.properties项目根目录或GRADLE_USER_HOME(linux 系统的$USER_HOME/.gradle目录)环境变量中的文件中).

- 环境变量，例如GRADLE_OPTS由执行Gradle的环境提供的,在环境变量中设置对应的参数,包括的环境变量有 GRADLE_OPTS GRADLE_USER_HOME JAVA_HOME (ps 这个一般不使用)

- 项目构建项目属性，如-PreleaseType=final,就是在gradle.properties中除了gradle.properties之外的参数

# 推荐用法使用gradle.properties

gradle.properties 承接了gradle 系统的很多属性,通过这种方法,我们可以统一gradle的环境信息配置

gradle.properties 中的参数具有一定的优先级,相同的参数如果配置在不同的位置上将会有覆盖效果,覆盖规则如下后者覆盖前者:

- gradle.properties 在项目根目录中.
- gradle.properties在GRADLE_USER_HOME目录中.
- 系统属性

下面的属性将会应用在gradle中

名称|参数
---|---
org.gradle.caching=(true,false)|设置为true时，Gradle将尽可能重用任何先前构建的任务输出，从而使构建速度更快.了解有关使用构建缓存的更多信息.
org.gradle.caching.debug=(true,false)|设置为true时，将在控制台上记录各个输入属性哈希值以及每个任务的构建缓存键.了解有关任务输出缓存的更多信息.
org.gradle.configureondemand=(true,false)|允许按需孵化配置，Gradle将尝试仅配置必要的项目.
org.gradle.console=(auto,plain,rich,verbose)|自定义控制台输出着色或详细程度.默认值取决于Gradle的调用方式.有关其他详细信息，请参阅命令行日志记
org.gradle.daemon=(true,false)|当设置true的摇篮守护进程来运行构建.默认是true.
org.gradle.daemon.idletimeout=(# of idle millis)|Gradle守护程序将在指定的空闲毫秒数后自行终止.默认为10800000(3小时)
org.gradle.debug=(true,false)|设置true为时，Gradle将在启用远程调试的情况下运行构建，侦听端口5005.请注意，这相当于添加-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005到JVM命令行，并将挂起虚拟机，直到连接调试器.默认是false.
org.gradle.java.home=(path to JDK home)|指定Gradle构建过程的Java主目录.可以将值设置为a jdk或jrelocation，但是，根据构建的功能，使用JDK会更安全.如果未指定设置，则使用合理的默认值.
org.gradle.jvmargs=(JVM arguments)|指定用于Gradle守护程序的JVM参数.该设置对于为构建性能配置JVM内存设置特别有用.
org.gradle.logging.level=(quiet,warn,lifecycle,info,debug)|当设置为quiet，warn，lifecycle，info或debug时，Gradle将使用此日志级别.值不区分大小写.该lifecycle级别是缺省值.请参阅选择日志级别.
org.gradle.parallel=(true,false)|配置完成后，Gradle将分叉到org.gradle.workers.maxJVM以并行执行项目.要了解有关并行任务执行的更多信息，请参阅Gradle性能指南.
org.gradle.warning.mode=(all,none,summary)|设置为all，summary或者none，Gradle将使用不同的警告类型显示.有关详细信息，请参阅命令行日志记录选
org.gradle.workers.max=(max # of worker processes)|配置后，Gradle将使用给定数量的工作者的最大值.默认值是CPU处理器数.另请参见性能命令行选项.

# gradle jvm 配置

gradle 使用org.gradle.jvmargs 可以配置jvm的各种运行参数

```
org.gradle.jvmargs = -Xmx2g -XX：MaxMetaspaceSize = 512m -XX：+ HeapDumpOnOutOfMemoryError -Dfile.encoding = UTF-8
```

也可以针对某一个task单独进行配置

```
plugins {
    id 'java'
}

tasks.withType(JavaCompile) {
    options.compilerArgs += ['-Xdoclint:none', '-Xlint:none', '-nowarn']
}
```

# gradle 编程设置参数信息

这我们先是声明了一个自定义的task,然后在内部使用if else 和 project.hasProperty 方法判断gradle 的运行环境中时候有isCI这个参数

```groovy
task performRelease {
    doLast {
        if (project.hasProperty("isCI")) {
            println("Performing release actions")
        } else {
            throw new InvalidUserDataException("Cannot perform release outside of CI")
        }
    }
}
```

# gradle通过http代理访问web

配置HTTP或HTTPS代理（例如，用于下载依赖项）是通过标准JVM系统属性完成的。这些属性可以直接在构建脚本中设置; 例如，设置HTTP代理主机将完成System.setProperty('http.proxyHost', 'www.somehost.org')。或者，可以在gradle.properties中指定属性。

使用配置HTTP代理 gradle.properties
```
systemProp.http.proxyHost = www.somehost.org 
systemProp.http.proxyPort = 8080 
systemProp.http.proxyUser = userid 
systemProp.http.proxyPassword = password 
systemProp.http.nonProxyHosts = *。nonproxyrepos.com | localhost
```

HTTPS有单独的设置。

使用配置HTTPS代理 gradle.properties
```
systemProp.https.proxyHost = www.somehost.org 
systemProp.https.proxyPort = 8080 
systemProp.https.proxyUser = userid 
systemProp.https.proxyPassword = password 
systemProp.https.nonProxyHosts = *。nonproxyrepos.com | localhost
```