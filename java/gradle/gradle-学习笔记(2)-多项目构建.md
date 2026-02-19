记得在maven中支持多个子项目的构建方法,同样的在gradle 中也会支持多项目的构建方法

还记得在maven中如何配置多项目工程吗, 这里回忆一下

1. 首先我们需要一个父元素pom文件比如这样

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.kyssion</groupId>
    <artifactId>maven-demo</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>pom</packaging>
</project>
```

而在gradle中,我们并不需要指定父元素的标签,我们只需要编写好对应的文件夹名称，并且将文件夹名称和对应的目录结构对应清，gradle 就能自动的识别这个子项目

比如我创建这样一个子项目名称是greeting-library

子项目中的配置未见build.gradle

```groovy
plugins {
    id 'groovy'
}

group 'com.kyssion'
version '1.0-SNAPSHOT'

repositories {
    mavenCentral()
}

dependencies {
    compile 'org.codehaus.groovy:groovy-all:2.5.6'
    testCompile group: 'junit', name: 'junit', version: '4.12'
}
```

父项目中的setting.gradle中添加这样一条配置

```groovy
include 'greeting-library'
```

这样就能使用greeting-library目录下的gradle子项目了

# 一个简单的项目

这使用一个简单的项目介绍一下这个如何使用gradle 实现整合打包

## 项目结构和模块划分

```
├── build.gradle
├── greeter
│   ├── build
│   │   ├── classes
│   │   │   └── java
│   │   │       └── main
│   │   │           └── greeter
│   │   │               └── Greeter.class
│   │   ├── distributions
│   │   │   ├── greeter-1.0-SNAPSHOT.tar
│   │   │   └── greeter-1.0-SNAPSHOT.zip
│   │   ├── generated
│   │   │   └── sources
│   │   │       └── annotationProcessor
│   │   │           └── java
│   │   │               └── main
│   │   ├── libs
│   │   │   └── greeter-1.0-SNAPSHOT.jar
│   │   ├── scripts
│   │   │   ├── greeter
│   │   │   └── greeter.bat
│   │   └── tmp
│   │       ├── compileJava
│   │       └── jar
│   │           └── MANIFEST.MF
│   ├── build.gradle
│   └── src
│       ├── main
│       │   ├── java
│       │   │   └── greeter
│       │   │       └── Greeter.java
│       │   └── resources
│       └── test
│           ├── java
│           └── resources
├── greeting-library
│   ├── build
│   │   ├── classes
│   │   │   └── groovy
│   │   │       ├── main
│   │   │       │   └── greeter
│   │   │       │       └── GreetingFormatter.class
│   │   │       └── test
│   │   │           └── greeter
│   │   │               └── GreetingFormatterSpec.class
│   │   ├── generated
│   │   │   └── sources
│   │   │       └── annotationProcessor
│   │   │           └── groovy
│   │   │               ├── main
│   │   │               └── test
│   │   ├── libs
│   │   │   └── greeting-library-1.0-SNAPSHOT.jar
│   │   ├── reports
│   │   │   └── tests
│   │   │       └── test
│   │   │           ├── classes
│   │   │           │   └── greeter.GreetingFormatterSpec.html
│   │   │           ├── css
│   │   │           │   ├── base-style.css
│   │   │           │   └── style.css
│   │   │           ├── index.html
│   │   │           ├── js
│   │   │           │   └── report.js
│   │   │           └── packages
│   │   │               └── greeter.html
│   │   ├── test-results
│   │   │   └── test
│   │   │       ├── binary
│   │   │       │   ├── output.bin
│   │   │       │   ├── output.bin.idx
│   │   │       │   └── results.bin
│   │   │       └── TEST-greeter.GreetingFormatterSpec.xml
│   │   └── tmp
│   │       ├── compileGroovy
│   │       │   └── groovy-java-stubs
│   │       ├── compileTestGroovy
│   │       │   └── groovy-java-stubs
│   │       ├── jar
│   │       │   └── MANIFEST.MF
│   │       └── test
│   │           └── jar_extract_15307722744227685163_tmp
│   ├── build.gradle
│   └── src
│       ├── main
│       │   ├── groovy
│       │   │   └── greeter
│       │   │       └── GreetingFormatter.groovy
│       │   ├── java
│       │   └── resources
│       └── test
│           ├── groovy
│           │   └── greeter
│           │       └── GreetingFormatterSpec.groovy
│           ├── java
│           └── resources
└── settings.gradle
```

这个项目中划分为根项目gradle-demo，包项目greeting-library，core可运行项目greeter。

注意： 通过上面的例子我们可以得出，在gradle 中不同的子项目的命名规则是使用文件夹的
注意：在java 项目中，gradle 要求 必须指定项目的main函数具体方法见下方

> 这里针对gradle的多语言的编程的目录结构做一下补充，gradle中源代码同意放置在这样的位置中src->main/test->编程语言名称文件夹 下

```groovy
plugins {
    id 'java'
    id 'application'
}

group 'com.kyssion'
version '1.0-SNAPSHOT'

sourceCompatibility = 1.8

mainClassName = "greeter.Greeter"  //这一句指定了main函数
repositories {
    mavenCentral()
}

dependencies {
    compile project(':greeting-library')
    testCompile group: 'junit', name: 'junit', version: '4.12'
}
```

# 总结

在构建gradle 多模块项目的时候,一定要注意多模块的之间的引用，模块中main函数的编写，父模块的include