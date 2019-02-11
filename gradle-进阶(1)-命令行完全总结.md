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