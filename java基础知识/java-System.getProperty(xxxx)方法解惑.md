> System.getProperty("java.version") 方法是输出java的运行环境变量(系统属性)的方法

- 主要可以输出的数据有:

java.version   Java 运行时环境版本
java.vendor   Java 运行时环境供应商
java.vendor.url   Java 供应商的 URL
java.home   Java 安装目录
java.vm.specification.version   Java 虚拟机规范版本
java.vm.specification.vendor   Java 虚拟机规范供应
java.vm.specification.name   Java 虚拟机规范名称
java.vm.version   Java 虚拟机实现版本
java.vm.vendor   Java 虚拟机实现供应商
java.vm.name   Java 虚拟机实现名称
java.specification.version   Java 运行时环境规范版本
java.specification.vendor   Java 运行时环境规范供应商
java.specification.name   Java 运行时环境规范名称
java.class.version   Java 类格式版本号
java.class.path   Java 类路径
java.library.path   加载库时搜索的路径列表
java.io.tmpdir   默认的临时文件路径
java.compiler   要使用的 JIT 编译器的名称
java.ext.dirs   一个或多个扩展目录的路径
os.name   操作系统的名称
os.arch   操作系统的架构
os.version   操作系统的版本
file.separator   文件分隔符（在 UNIX 系统中是“/”）
path.separator   路径分隔符（在 UNIX 系统中是“:”）
line.separator   行分隔符（在 UNIX 系统中是“/n”）
user.name   用户的账户名称
user.home   用户的主目录
user.dir   用户的当前工作目录

### java运行环境的设置方法

其实本质上就是使用jvm虚拟机提供的-D参数

比如设置 **java -Done.xxx.yyy=123**

功能解析
**-D=value**
官网解释：
    Set a system property value. If value is
    a string that contains spaces, you must enclose the string in double quotes:
在虚拟机的系统属性中设置属性名/值对，运行在此虚拟机上的应用程序可用：
```java
System.getProperty("属性名")
```
得到value的值。
如果value中有空格，则需要用双引号将该值括起来，**如：-Dname=”kazaf f”**

该参数通常用于设置系统级全局变量值，如配置文件路径，保证该属性在程序中任何地方都可访问。


注意事项
1. 需要设置的是JVM参数而不是program参数；
2. 使用此参数的参数优先级最高，会覆盖项目中配置的此项；

