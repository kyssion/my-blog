这里记录一下gradle的详细使用信息

# gradle 命令的组成

> gradle的命令总体上只有两个点 taskname 和 option

```
gradle [task-Name...] [--option-name...]
```

如果不带-- 就是task 带的话就是option

> option可能带有参数,这里使用=号来为他赋值

```
--console=plain
```

> 可以使用 --no- 来命名反转,表示不进行什么操作

```
--build-cache 
--no-build-cache
```

> option具有等价形式比如

```
--help
等价
-h
```

# gradle 执行task

> 在子项目环境下可以使用[:子项目名称]...[:子项目名称][:taskName] 来运行指定的task(只是在root项目中可以运行)

```
gradle :mySubproject:taskName
```

> 如果没有指定子项目名称将会从当前目录的项目中向下寻找task

```
gradle taskName
```

> 多task运行

应用上面的规则,使用空格可开就可以指定多个子task顺序执行了

```
gradle test deploy
```

> 移除一个task

使用 --exclude-task 移除gradle运行过程中的一个task

```
gradle dist --exclude-task test
```

> 重新运行

不会保留之前运行的结果而是重新执行

```
gradle test --rerun-tasks
```

> 非中断执行

--continue 这个参数将会覆盖之前gradle运行是如果有一个task失败接下来的都不会执行,而变为跳过失败的task在其他非依赖本失败task的task执行完后打印错误

```
gradle test --continue
```

# gradle中一些常用的task

名称|作用
---|---
build|组装所有输出并运行所有检查
run|执行某些脚本或二进制文件
check|使用该任务执行所有验证任务（包括测试和linting）
clean|删除构建目录的内容
projects|列出所有的项目报告,子项目树
tasks|主要task列表,可以使用--all 打印出更多的信息
gradle help --task someTas|显示指定任务的详细信息
gradle myTask --scan|构建扫描提供了关于哪些配置，传递依赖关系和依赖关系版本选择存在哪些依赖关系的完整可视报告
gradle dependencies|提供所选项目的依赖关系列表，按配置细分。对于每个配置，该配置的直接和传递依赖关系都显示在树中
gradle buildEnvironment|通上面的依赖配置,这个展示的是父子项目或者其他形式的配置依赖
gradle properties|为您提供所选项目的属性列表
gradle model|


# gradle中一些常用的option

> DEBUG相关的参数

名称|作用
---|---
-?, -h, --help|帮助文档
-v, --version|输出整个环境的版本信息groovy java gradle等等
-S, --full-stacktrace|打印出任何异常的完整（非常详细）堆栈跟踪。 另请参阅日志记录选项
-s, --stacktrace|打印堆栈跟踪也用于用户异常（例如编译错误）。另请参阅日志记录选项
--scan|创建一个构建扫描，其中包含有关Gradle构建的所有方面的细粒度信息
-Dorg.gradle.debug=true|Debug Gradle client (non-Daemon) process. Gradle will wait for you to attach a debugger at localhost:5005 by default.
-Dorg.gradle.daemon.debug=true|Debug Gradle Daemon进程

> 性能选择参数(Performance options)

这里的很多性能优化参数其实可以在gradle.properties中指定的

名称|作用|properties文件中的参数
---|---|---
--build-cache, --no-build-cache|切换Gradle构建缓存.Gradle将尝试重用以前版本的输出.默认为关闭|
--configure-on-demand, --no-configure-on-demand|切换按需配置。在此构建运行中仅配置相关项目。默认为关闭。|
--max-workers|设置Gradle可以使用的最大工作数。默认值是处理器数量|
--parallel, --no-parallel|并行构建项目。有关此选项的限制，请参阅并行项目执行。默认为关闭。|
--profile|在$ buildDir / reports / profile目录中生成高级性能报告。 --scan是首选。|
--scan|使用详细的性能诊断生成构建扫描。|

# Gradle守护程序选项

名称|作用
---|---
--daemon, --no-daemon|使用Gradle Daemon运行构建。如果未运行守护程序或现有守护程序繁忙，则启动守护程序。默认打开。
--foreground|在前台进程中启动Gradle守护程序
--status (Standalone command)|运行gradle --status列出正在运行且最近停止的Gradle守护进程。仅显示相同Gradle版本的守护程序。
--stop (Standalone command)|运行gradle --stop以停止相同版本的所有Gradle守护进程。
-Dorg.gradle.daemon.idletimeout=(number of milliseconds)|Gradle守护程序将在此毫秒的空闲时间后停止运行。默认值为10800000（3小时）

# gradle 日志参数

-Dorg.gradle.logging.level=(quiet,warn,lifecycle,info,debug)|通过Gradle属性设置日志记录级别。
-q, --quiet|仅记录错误。
-w, --warn|将日志级别设置为警告
-i, --info|Set log level to info.
-d, --debug|登录调试模式（包括正常的堆栈跟踪）。

# gradle自定义日志样式

您可以通过以下方式指定“控制台”模式来控制丰富输出（颜色和字体变体）的使用

-Dorg.gradle.console=(auto,plain,rich,verbose),--console=(auto,plain,rich,verbose)|通过Gradle属性指定控制台模式。下面描述了不同的模式

- plain : 设置为plain以仅生成纯文本。此选项禁用控制台输出中的所有颜色和其他丰富输出。当Gradle未连接到终端时，这是默认设置

- auto : 设置为auto（默认值）以在构建过程附加到控制台时在控制台输出中启用颜色和其他丰富输出，或仅在未连接到控制台时生成纯文本。 这是Gradle连接到终端时的默认设置。

- rich : 设置为rich以在控制台输出中启用颜色和其他丰富输出，无论构建过程是否未附加到控制台。 如果未连接到控制台，则构建输出将使用ANSI控制字符来生成丰富的输出。

- verbose : 设置为verbose以启用颜色和其他丰富输出，如富，但在生命周期日志级别输出任务名称和结果，如Gradle 3.5及更早版本中默认执行

# gradle 警告提示级别

默认情况下，Gradle不会显示所有警告（例如，弃用警告）。相反，Gradle将收集它们并在构建结束时呈现摘要

-Dorg.gradle.warning.mode=(all,none,summary)
通过Gradle属性指定警告模式。 下面描述了不同的模式。

--warning-mode=(all,none,summary)
指定如何记录警告。 默认为摘要。

- 设置为all以记录所有警告。

- 设置为summary以禁止所有警告并在构建结束时记录摘要。

- 设置为none以禁止所有警告，包括构建结束时的摘要。

# 执行时设置option

> ps 感觉没少啥用,具体可以看文档这里不记录了

# gradle 配置参数(这些其实可以在配置文件中指定的对应的方法)

名称|作用
---|---
-b,-build-file|指定构建文件。例如：gradle --build-file = foo.gradle。默认值为build.gradle，然后是build.gradle.kts，然后是myProjectName.gradle。
-c,-setting-fil|指定设置文件。例如：gradle --settings-file = somewhere/else/settings.gradle
-g,-gradle-user-home|指定Gradle用户主目录。默认值是用户主目录中的.gradle目录。
-p,-project-dir|指定Gradle的起始目录。默认为当前目录。
--project-缓存目录|指定项目特定的缓存目录。根项目目录中的默认值为.gradle。
-u,-no-search-upward（不建议使用）|不要在父目录中搜索settings.gradle文件。
-D,-system-prop|设置JVM的系统属性，例如-Dmyprop = myvalue。请参阅系统属性。
-I,-init-script|指定初始化脚本。请参阅Init Scripts。
-P,-project-prop|设置根项目的项目属性，例如-Pmyprop = myvalue。请参阅系统属性。
-Dorg.gradle.jvmargs|设置JVM参数。

# gradle 初始化构建

主要就是一个命令

```
gradle init
```

这个命令可以附带一些参数,比如

--type java-library : 指定构建的项目类型
--gradle-version : 指定gradle的版本

等等

# gradle 的持续构建目前是一项测试功能 应用参数是--continuous

java9 的更新太大了,现在很多框架都是应用的java8构建的,java9 扯到蛋了.......
java11 真的很强大,学了gradle准备开始造轮子了,那些框架没有更新是因为用的人少,社区也没有去推动....................