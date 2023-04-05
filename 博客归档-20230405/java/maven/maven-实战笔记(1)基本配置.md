## maven 实战笔记（一）基本配置

在java世界中maven应该是应用最为广泛的项目构建工具，之前使用过maven但是没哟进行细致系统的学习，这次开一个专题进行一下系统的整理

### maven文件目录结构

- bin：maven的运行时目录，放置maven运行时的脚本，目录中还有一个mvnDebug文件，相比较mvn文件添加了调试功能，文件夹中的m2.conf，是classworlds的配置文件

- boot：中只有一个文件plexus-classworlds-2.5.2.jar（maven3.5）这个是maven自己的实现的类加载器（这个其实是实现jar下载等功能所必需的）

- conf：其中的settting.xml文件全局定义maven的行为，在使用上更加倾向于见此文件拷贝至~/.m2文件夹中进行私有化定制
lib：防止maven的各种依赖文件


> 一个命令：mvn help:system   打印出所有java系统属性和环境变量

### maven使用代理

> 有的时候需要进行配置相关的代理才能正常的访问外部仓库，maven提供这样的配置

```xml
<proxies>
    <!-- proxy
 Specification for one proxy, to be used in connecting to the network.
   -->
    <proxy>
      <id>optional</id>
      <active>true</active>
      <protocol>http</protocol>
      <username>proxyuser</username>
      <password>proxypass</password>
      <host>proxy.host.net</host>
      <port>80</port>
      <nonProxyHosts>local.net|some.host.com</nonProxyHosts>
    </proxy>
</proxies>
```

### maven pom 文件

> maven  项目的核心是 pom文件 定义了项目的基本信息例如下面的配置文件

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<groupId>com.kys</groupId>
	<artifactId>Demo</artifactId>
	<packaging>pom</packaging>
	<version>0.0.1-SNAPSHOT</version>
	<name>Demo Maven Webapp</name>
	<url>http://maven.apache.org</url>
	<properties>
		<java.version>1.8</java.version>
	</properties>
	<!-- 指定依赖坐标 -->
	<dependencies>
		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-context</artifactId>
			<version>5.0.0.RELEASE</version>
		</dependency>
	</dependencies>
	<build>
		<finalName>Demo</finalName>
		<plugins>
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-compiler-plugin</artifactId>
				<version>3.1</version>
				<configuration>
					<source>1.8</source>
					<target>1.8</target>
				</configuration>
			</plugin>
		</plugins>
	</build>
	<modules>
		<module>newDemo</module>
	</modules>
</project>
```
### pom 文件核心标签

#### project标签-表示一个maven项目的最外层标签

**子标签**
|标签名称|作用|
|--|--|
modelversion|指定POM模型的版本现在只能使用4.0.0。gounpId,artifactId,version,packaging,classifier	三要素，定义了一个项目的坐标，groupId定义项目属于哪一个组，artifactId定义当前项目在组中的唯一id，version指定当前的项目的版本号，packaging指定打包的方式默认使用jar包，classifier用来昂住定义构建输出一些附属构建
name|声名一个对用户友好的名称，不是必须的
dependencies dependenc|标签的副标签，可以包含多个dependency标签，相对于dependencyManagement，所有生命在dependencies里的依赖都会自动引入，并默认被所有的子项目继承。
dependencyManagement|一个依赖管理者一般都是不是在顶层的maven 模块上面，子模块通过继承父maven项目，可以在自己的依赖中不用指明版本号而直接使用父maven项目中的dependencyManagement配置的版本号。在我们项目顶层的POM文件中，我们会看到dependencyManagement元素。通过它元素来管理jar包的版本，让子项目中引用一个依赖而不用显示的列出版本号。

> dependencyManagement和dependencies区别

**dependencies**:即使在子项目中不写该依赖项，那么子项目仍然会从父项目中继承该依赖项（全部继承）

**dependencyManagement**:里只是声明依赖，并不实现引入，因此子项目需要显示的声明需要用的依赖。如果不在子项目中声明依赖，是不会从父项目中继承下来的；只有在子项目中写了该依赖项，并且没有指定具体版本，才会从父项目中继承该项，并且version和scope都读取自父pom;另外如果子项目中指定了版本号，那么会使用子项目中指定的jar版本。

#### dependency标签-表示一个依赖坐标

子标签
|标签名称|作用|
|--|--|
gounpId,artifactId,version|三要素，定义了一个项目的坐标，groupId定义项目属于哪一个组，artifactId定义当前项目在组中的唯一id，version指定当前的项目的版本号
scope|（编译指的是maven进行编译项目）表示依赖范围 1.compile：编译依赖范围  编译测试运行都有效2.test：测试依赖范围 编译和运行时无法使用，测试下使用（junit）3.provided 已提供依赖范围 运行时无效（各种web service依赖） 4.runtime  编译时无效 （如jdbc）5.system  系统依赖范围和provided类似但是 需要使用systenPath标签手动指定依赖范围6,import：一般和dependencyManagement组合使用
type|声名依赖类型，默认是使用jar
optional|标记依赖是否可选
exclusions|排除传递性依赖  是定groupId和artifactId将会将指定的依赖驱除掉，见下面例子

```xml
<dependencies>
    <dependency>
        <groupId>org.mydemo</groupId>
        <artifactId>demo-context</artifactId>
        <version>1.0.0.RELEASE</version>
        <exclusions>
            <exclusion>
                <groupId>org.mydemo</groupId>
                <artifactId>two</artifactId>
            </exclusion>
        </exclusions>
    </dependency>
</dependencies>
```

#### repositories标签-添加远程仓库到指定的位置中

```xml
<project ...>
    <repositories>
      <repository>
	<id>JBoss repository</id>
	<url>http://repository.jboss.org/nexus/content/groups/public/</url>
      </repository>
    </repositories>
</project>
```

### 聚合与继承（一般一起使用因为父级打包方式强制要求pom方式）

**聚合**：聚合，顾名思义，就是把多个模块或项目聚合到一起，我们可以建立一个专门负责聚合工作的Maven project —  aggregator。

建立该project的时候，我们要注意以下几点：

1. 该aggregator本身也做为一个Maven项目，它必须有自己的POM,它的打包方式必须为： pom
2. 引入了新的元素：modules—module    <module>中 写的是地址
3. 版本：聚合模块的版本和被聚合模块版本一致  <version>中指定的版本号
4. relative path：每个module的值都是一个当前POM的相对目录
5. 目录名称：为了方便的快速定位内容，模块所处的目录应当与其artifactId一致(Maven约定而不是硬性要求)，总之，模块所处的目录必须和<module>模块所处的目录</module>相一致。 也就是说子模块应该在父模块pom.xml文件所在目录的下面的<module>指定的相关目录地址
6. 习惯约定：为了方便构建，通常将聚合模块放在项目目录层的最顶层，其它聚合模块作为子目录存在。这样当我们打开项目的时候，第一个看到的就是聚合模块的POM
7. 聚合模块减少的内容：聚合模块的内容仅仅是一个pom.xml文件，它不包含src/main/java、src/test/java等目录，因为它只是用来帮助其它模块构建的工具，本身并没有实质的内容。
8. 聚合模块和子模块的目录：他们可以是父子类，也可以是平行结构，当然如果使用平行结构，那么聚合模块的POM也需要做出相应的更改。


```xml
<modules>
    <module>billing-dao</module>
    <module>billing-schedule</module>
    <module>billing-service</module>
    <module>billing-utils</module>
    <module>billing-web</module>
    <module>billing-object</module>
    <module>billing-client</module>
</modules>
```
------

**继承**：做面向对象编程的人都会觉得这是一个没意义的问题，是的，继承就是避免重复，maven的继承也是这样，它还有一个好处就是让项目更加安全

配置继承：

1. 继承肯定是一个父子结构，那么我们在aggregator中来创建一个parent project 使用 <parent>标签
2. <packaging>: 作为父模块的POM，其打包类型也必须为POM
结构：父模块只是为了帮助我们消除重复，所以它也不需要src/main/java、src/test/java等目录
3. 新的元素：<parent> ， 它是被用在子模块中的
<parent>元素的属性：<relativePath>: 表示父模块POM的相对路径，在构建的时候，Maven会先根据relativePath检查父POM，如果找不到，再从本地仓库查找  指定去那里寻找 父pom.xml
4. relativePath的默认值： ../pom.xml
5. 子模块省略groupId和version： 使用了继承的子模块中可以不声明groupId和version, 子模块将隐式的继承父模块的这两个元素

```xml
<parent>
    <artifactId>parent-all</artifactId>
    <groupId>com.dfire</groupId>
    <version>1.0.3</version>
</parent>
```

继承的POM元素

- groupId:项目组ID,项目坐标的核心元素
- version: 项目版本, 项目坐标的核心元素
- description: 项目的描述信息
- organization: 项目的组织信息
- inceptionYear: 项目的创始年份
- url: 项目的URL地址
- developers: 项目开发者信息
- contributors: 项目的贡献者信息
- distributionManagement: 项目的部署配置
- issueManagement: 项目的缺陷跟踪系统信息
- ciManagement: 项目的持续集成系统信息
- scm: 项目的版本控制系统信息
- mailingLists: 项目的邮件列表信息
- properties: 自定义的maven属性
- dependencies: 项目的依赖配置
- dependencyManagement: 项目的依赖管理配置
- repositories: 项目的仓库配置
- build: 包括项目的源码目录配置、输出目录配置、插件配置、插件管理配置等
- reporting: 包括项目的报告输出目录配置、报告插件配置等

### 聚合继承下的依赖管理

**依赖继承管理**：dependencyManagement

**dependencyManagement的特性**：在dependencyManagement中配置的元素既不会给parent引入依赖，也不会给它的子模块引入依赖，仅仅是它的配置是可继承的

父pom 配置依赖的版本

```xml
<properties>  
    <target.version>2.5.6</target.version>  
</properties>    
<dependencyManagement>  
    <dependencies>  
        <dependency>  
            <groupId>your groupId</groupId>  
            <artifactId>your artifactId</artifactId>  
            <version>${target.version}</version>  
        </dependency>  
    </dependencies>  
</dependencyManagement>
```

子pom 选择性的继承

```xml
<dependencies>  
    <dependency>  
        <groupId>your groupId</groupId>  
        <artifactId>your artifactId</artifactId>  
    </dependency>  
</dependencies>  
```

**插件继承管理**：<pluginManagement>

这个元素和<dependencyManagement>相类似，它是用来进行插件管理的。在我们项目开发的过程中，也会频繁的引入插件，所以解决这些复杂配置的方法就是使用插件管理

父pom 配置插件依赖

```xml
<pluginManagement>
    <plugins>
        <plugin>
            <groupId></groupId>
            <artifactId></artifactId>
            <version></version>
            <executions>
                <execution>
                    <id></id>
                    <goals>
                        <goal></goal>
                    </goals>
                    <phase></phase>
                    <configuration>
                        <source></source>
                        <target></target>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</pluginManagement>
```

子pom 选择插件继承

```xml
<plugins>
    <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
    </plugin>
</plugins>
```

聚合与继承的总结当我们明白聚合与继承的细节之后，我们会发现：对于聚合模块来说，它知道有哪些被聚合的模块，而对于被聚合的模块来说，它们不知道被谁聚合了，也不知道它的存在对于继承关系的父POM来说，它不知道自己被哪些子模块继承了，对于子POM来说，它必须知道自己的父POM是谁在一些最佳实践中我们会发现：一个POM既是聚合POM，又是父POM，这么做主要是为了方便。