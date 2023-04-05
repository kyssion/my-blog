作为一个最基本的入门，这里只是打一个最简单的jar包

# 打jar包三个重要的gradle的参数 name，build.gradle的version和jar

```groovy
version '1.0-SNAPSHOT'
```

## 通过jar 命令构建jar包中MANIFSET.MF文件中的参数信息

jar 配置的方法

```groovy
jar {
    manifest {
        attributes('Implementation-Title': project.name,
                'Implementation-Version': project.version)
    }
}
```

然后使用jar 命令的时候，将会在build文件夹中的libs子文件夹里生成对应的jar包，这里摘出他的MANIFSET.MF文件中的内容

```java
Manifest-Version: 1.0
Implementation-Title: create-java-library
Implementation-Version: 1.0-SNAPSHOT
```

##  version 制定生成的jar包版本号

我们配置一个参数

```groovy
version '1.0-SNAPSHOT'
```

然后当执行gradle jar 的task的时候将会在lib文件夹中生成后缀为1.0-SNAPSHOT的jar包



