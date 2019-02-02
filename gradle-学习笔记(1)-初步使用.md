最近想深入的学习一下工程化方面相关的东西，在maven和gradle直接纠结不已，因为maven的扩展性太差劲了，学习成本颇高，所以最后投入了gradle的怀抱中，以后有时间再重新学习一下maven吧

最近的学习笔记是基于gradle 5 系列，其中各种教程和例子大都是来源于官方文档或者网络上的博客。内容涵盖我在学习gradle过程中的各种心得和gradle的一些使用方法

# gradle创建项目

一个命令 

```shell
gradle init
```

用户可以通过这个命令创建一个基本的gradle项目包括gradle项目的目录结构

```shell
├── build.gradle (1)
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar (2)
│       └── gradle-wrapper.properties (3)
├── gradlew (4)
├── gradlew.bat (5)  
└── settings.gradle (6)  
```

- (1) gradle 的构建脚本用来构建当前的gradle项目,最核心的配置文件
- (2) (3) 一个gradle副本和配置文件，用来当如果系统中的gradle版本和项目使用的gradle版本不同，将会在这里下载一个项目中的版本
- (4) (5) 配套使用的命令行工具 没有.bat后缀的是unix系统命令有的是windowns系统，可以用来执行gradle中定义的各种task 任务
- (6) 用于配置Gradle构建的Gradle设置脚本 

# gradle的task

gradle 方便用户进行配置的特性是源于gradle提供了方便使用task参数
这里编写一个很基本的copy文件的权限，在路径中添加一个src文件夹和dest文件夹，在src文件中添加一个文件markfile.txt 并且里面有一个内容hello world！

然后在build.gradle 中编写一个任务

```groovy
task copy(type:Copy,group:"custom",description:"test one"){
    from "src"
    into "dest"
}
```

其中的type 字段将会调用系统总的Copy函数，而group和description 只是描述这个过程的描述符，只会影响系统的log输出，并不会影响实际的效果


