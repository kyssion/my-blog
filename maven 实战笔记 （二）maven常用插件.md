### maven 实战笔记 （二）maven常用插件

#### maven-source-plugin

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-source-plugin</artifactId>
    <version>2.2.1</version>
    <executions>
        <execution>
            <id>attach-source</id><!-- 名称随意指定 -->
            <phase>package</phase><!-- 要绑定到的生命周期的阶段 -->
            <goals>
                <goal>jar-no-fork</goal><!-- 要绑定的插件的目标 -->
            </goals>
        </execution>
    </executions>
</plugin>
```

这样在mvn package后便会在target目录下生成*-sources.jar源码包。

#### maven-javadoc-plugin

```xml
<plugin>
	<groupId>org.apache.maven.plugins</groupId>
	<artifactId>maven-javadoc-plugin</artifactId>
	<version>2.7</version>
	<executions>
		<execution>
			<id>attach-javadocs</id>
			<phase>package</phase>
			<goals>
				<goal>jar</goal>
			</goals>
		</execution>
	</executions>
</plugin>
```

这样在mvn package后便会在target目录下生成*-javadoc.jar文档包。

#### maven-compiler-plugin

指定JDK版本和编码
maven 2.1默认用jdk 1.3来编译，maven3 貌似是用jdk 1.5，如果项目用的jdk 1.6也会有问题，compiler插件可以指定JDK版本为1.6。
windows默认使用GBK编码，java项目经常编码为utf8，也需要在compiler插件中指出，否则中文乱码可能会出现编译错误。

```xml
<plugin> 
	<groupId>org.apache.maven.plugins</groupId> 
	<artifactId>maven-compiler-plugin</artifactId>
	<version>3.1</version> 
	<configuration> 
		<source>1.6</source> 
		<target>1.6</target> 
		<encoding>UTF8</encoding> 
	</configuration> 
</plugin> 
```
#### maven-shade-plugin

mvn clean package后，target下可以看到mvn-test-0.0.1-SNAPSHOT.jar和original-mvn-test-0.0.1-SNAPSHOT.jar两个jar包，前者是带有依赖包(会解压)和Main-Class信息的可运行jar包，后者是原始的jar包(不包含依赖及Main-Class信息)。
打开mvn-test-0.0.1-SNAPSHOT.jar/META-INF/MANIFEST.MF可看到Main-Class: com.adu.mvn_test.HelloWorld信息。
可运行jar包的执行：$java -jar mvn-test-0.0.1-SNAPSHOT.jar 或者直接双击。

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-shade-plugin</artifactId>
    <version>1.4</version>
    <executions>
        <execution>
            <phase>package</phase><!-- 要绑定到的生命周期的阶段 -->
            <goals>
                <goal>shade</goal><!-- 要绑定的插件的目标 -->
            </goals>
            <configuration>
                <transformers>
                    <transformer
                            implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                        <mainClass>com.adu.mvn_test.HelloWorld</mainClass><!-- 指定可执行jar包的主程序入口 -->
                    </transformer>
                </transformers>
            </configuration>
        </execution>
    </executions>
</plugin>
```





