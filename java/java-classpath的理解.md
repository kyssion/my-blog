
这次写这一片篇文章的起因是对老大搭建的底层框架存在怀疑结果然后自己照着老大的方法运行竟然可以成功原因的费解。因此在这里记录一下自己的疑问解惑过程。

### classpath到底是啥

我的理解classpath 其实是 java 的一种虚拟的文件目录结构，java通过包名（相当于路径名称），针对每一个classpath地址（java支持多个classpath地址）进行资源管理的一种抽象路径

#### 1. 针对于资源加载

最直观是我在mybatis中配置map xml文件路径的时候会加上

```
classpath:map/*.xml
```

这么做将会让mybati所有所有的classpat路径下的对应的map/目录中的文件

也就是说如果jar包1 中有map/目录，并且jar2 中也有这个目录 jar1 引用了jar2，当jar1运行的时候并且jar2又在classpath当中的时候将会自动的搜索两个jar包classpath相对路径下的，map/目录下的信息

> 注意如果两个文件名称是相同的（包括classpath对应的相对路径），将会以先加载的文件优先

#### 2. 对与和class对象加载

jvm的类加载分三中方式：

1. 系统级别：rt.jar
2. 扩展级别：java_home/jre/lib/ext/目录下的jar文件
3. 应用级别：环境变量中的classpath或javac   java中的参数指定java   -classpath        …
4. 或者自己写ClassLoader加载。

 前面2中是JVM自动处理。其中第二种是为了处理Java的classpath灾难而提供的解决方案。

实际上java虚拟机是由java luncher初始化的，也就是java（或java.exe）这个程序来做的。

虚拟机按以下顺序搜索并装载所有需要的类：

1. 引导类:组成java平台的类，包含rt.jar和i18n.jar中的类。
2. 扩展类：使用java扩展机制的类，都是位于扩展目录（$JAVA_HOME/jre/lib/ext）中的。jar档案包。
3. 用户类:开发者定义的类或者没有使用java扩展机制的第三方产品。你必须在命令行中使用-classpath 选项或者使用CLASSPATH环境变量来确定这些类的位置。我们在上面所说的用户自己的类就是特指这些类。

这样，一般来说,用户只需指定用户类的位置，引导类和扩展类是 "自动 "寻找的。
当你的程序需要第三方的类库支持，而且比较常用，就可以采用此种方法。比如常用的数据库驱动程序，写servlet需要的servlet包等等。设置方法就是在环境变量中加入CLASSPATH.然后就可以直接编译运行了。而你的程序只用了些基础类，寻找时，就用不着必须设定它。

在执行Java程序的时候，会自动加载程序用中需要的在rt.jar和其他java_home\jre\lib中包含的。jar文件中包含的Java基础类库和一些扩展类库。这些都是JVM自动处理的，对用户来说是透明的。

如果Java程序中使用到了一些应用级别的类（如第三方的类），可以在javac和java中的-classpath选项中指定它们的搜索路径，或者是自己写ClassLoader加载，另外也可以设置ClassPath环境变量，在里面指定那些蝶阀应用级别的类的搜索路径。

设置ClassPath环境变量不是必须的，只是为了方便使用，设置了ClassPath，JDK就会按ClassPath制定的路径去搜索需要的应用级别的类，而不必每一次都使用-classpath选项或自己写ClassLoader。

还有需要注意的就是：如果相关的类就在当前工作目录下的话，上面3种方法都可以不要，因为JDK系统会首先搜索会在当前的工作目录中搜索程序相关的类。

> 注意如果在class系统中两个类称是相同的（包名+类名），将会以先加载的类优先