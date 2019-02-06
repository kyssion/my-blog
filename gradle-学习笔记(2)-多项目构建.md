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

而在gradle中,我们并不需要指定父元素的标签,我们只需要指定相关的