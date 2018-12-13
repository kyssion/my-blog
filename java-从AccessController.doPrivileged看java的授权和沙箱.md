> 这里主要是介绍java以代码为核心的授权方法(还有基于用户的jaas授权方法不做讨论),这个还是比较重要的(其实是看很多源代码框架使用了这个方法,为了保证代码在沙盒环境中可以运行).

### 权限

在Java平台安全体系结构中，所有访问权限都是类型化的并且有层次结构，其根是抽象类 java.security.Permission 。标准的权限类大约有如下的这些(使用类来标记权限)

| 　 | 类型 | 权限名 | 操作 | 例子 |
| --- | --- | --- | --- | --- |
| 文件权限 | java.io.FilePermission | 文件名（平台依赖） | 读、写、删除、执行 | 允许所有问价的读写删除执行：permission java.io.FilePermission "<< ALL FILES>>", "read,write,delete,execute";。允许对用户主目录的读：permission java.io.FilePermission "${user.home}/-", "read";。 |
| 套接字权限 | java.net.SocketPermission | 主机名:端口 | 接收、监听、连接、解析 | 允许实现所有套接字操作：permission java.net.SocketPermission "_:1-", "accept,listen,connect,resolve";。允许建立到特定网站的连接：permission java.net.SocketPermission "_.abc.com:1-", "connect,resolve";。 |
| 属性权限 | java.util.PropertyPermission | 需要访问的jvm属性名 | 读、写 | 读标准Java属性：permission java.util.PropertyPermission "java._", "read";。在sdo包中创建属性：permission java.util.PropertyPermission "sdo._", "read,write";。 |
| 运行时权限 | java.lang.RuntimePermission | 多种权限名[见附录A] | 无 | 允许代码初始化打印任务：permission java.lang.RuntimePermission "queuePrintJob" |
| AWT权限 | java.awt.AWTPermission | 6种权限名[见附录B] | 无 | 允许代码充分使用robot类：permission java.awt.AWTPermission "createRobot"; permission java.awt.AWTPermission "readDisplayPixels";。 |
| 网络权限 | java.net.NetPermission | 3种权限名[见附录C] | 无 | 允许安装流处理器：permission java.net.NetPermission "specifyStreamHandler";。 |
| 安全权限 | java.security.SecurityPermission | 多种权限名[见附录D] | 无 ||
| 序列化权限 | java.io.SerializablePermission | 2种权限名[见附录E] | 无 ||
| 反射权限 | java.lang.reflect.ReflectPermission | suppressAccessChecks（允许利用反射检查任意类的私有变量） | 无 ||
| 完全权限 | java.security.AllPermission | 无（拥有执行任何操作的权限） | 无 | |

> 在这种模式下 jvm的权限是给代码的(可以说类反正就代码的),一个类(代码)可以有多个权限(在$JREHOME/lib/security/java.policy文件中进行配置下面说),使用PermissionCollection这样的类进行封装(jvm在运行的时候通过文件自动生成好了,然后通过反射进行校验这些东西都被隐藏起来了,研究下去意义不大,就没有接着研究)

### 保护域和代码源

> java2 是针对代码(对象类)添加保护区,有一个内部类ProtectionDomain,通过这个类授权访问权限,如果多个类使用同一个ProtectionDomain将会认为这个权限是相同的

> 显然，一定要能惟一地标识一段运行代码以保证它的访问权限没有冲突。运行代码的惟一标识属性共有两项：代码的来源（代码装载到内存所用的 URL）和代码的 signer 实体（由对应于运行代码的数字签名的一组公共密钥指定）。这两种特性的组合在 Java 2 平台安全体系结构中编写为给定运行代码的 CodeSource (在ProtectionDomain内部可以看见这个对象)。

### 权限生成的具体过程

1. Java 运行时通过名为 java.security.Policy 的类（的具体扩展）设置 ProtectionDomain 与授予它的权限之间的映射。
2. 这个类的默认扩展是 sun.security.provider.PolicyFile 。正如其名字所表明的， sun.security.provider.PolicyFile 从一个文件中获得 CodeSource （由位置 URL 和 signer 标识别名）与授予它的权限之间的映射。
3. 可以通过环境变量 java.security.policy 将这个文件的位置作为输入提供给 JVM。 Policy 类提供了一个名为 getPermissions() 的方法，可以调用它以获得授予特定 CodeSource 的一组权限。

### 权限加载的过程

1. 一个类与 其 ProtectionDomain 之间的映射是在类第一次装载时设置的，并在类被垃圾收集之前不会改变。
2. 一个类通常是由一个名为 SecureClassLoader 的特殊类装载的。 SecureClassLoader 首先从相应 URL 处装载字节，如果需要还会验证包围文档文件的数字签名。然后它调用上述 getPermissions() 方法获得授予类的 CodeSource 的一个填充了静态绑定权限的异类 PermissionCollection 。
3. 然后 SecureClassLoader 创建新的 ProtectionDomain ，传递 CodeSource 及其相关的权限作为其构造函数的参数（当然，这假定对于给定 CodeSource 还不存在 ProtectionDomain 。如果用一个现有的 CodeSource 装载类，那么就会重复使用它已经建立的 ProtectionDomain ） 。 
4. 最后，用装载的类字节向 JVM 定义一个类，并在关联的 ProtectionDomain 中维护一个引用指针。

### 执行过程

一个名为 SecurityManager 的类负责实施系统安全策略。在默认情况下不安装安全管理器，必须通过一个在启动时传递给 JVM 的、名为 java.security.manager 的环境变量显式地指定。任何应用程序都可找到安装的 SecurityManager 并调用它相应的 check<XXX> 方法。如果所要求的权限在给定运行时上下文中是授予的，那么调用将无声地返回。如果权限没有授予，那么将抛出一个 java.security.AccessControlException 。

Java 2 平台安全体系结构通过引入一个名为 AccessController 的新类使这一切变得简单了，并更具有可扩展性。这个类的目的与 SecurityManager 是一样的，即它负责做出访问决定。当然， 为了向后兼容性保留了 SecurityManager 类，但是其更新的实现委派给了底层的 AccessController 。对 SecurityManager 类进行的所有 check<XXX> 方法调用都解释为相应的 Permission 对象，并将它作为输入参数传递给 AccessController 类的 checkPermission() 方法。

### 权限的继承和优化问题

> 如果说类A调用了类B,B调用了类C,那么C的权限就是ABC权限的交集

### 最终节-> 看java的AccessController.doPrivileged

- 通过上面的引子,终于了解的这个方法是干啥的了,这个方法就是解决这样一个问题,**如果A调用了B,但是A的权限太小,B的权限太大导致,A影响了B的功能,这个使用使用上面的方法,这个方法将会让jvm进行权限计算的时候将会使用B最为最顶层的权限,这个样A或者A之前的权限就对B和B之后的不起作用了**

### 一个简单的小例子

#### 策略文件$JREHOME/lib/security/java.policy

```java
// Standard extensions get all permissions by default

grant codeBase "file:${{java.ext.dirs}}/*" {
        permission java.security.AllPermission;
```

#### 参数文件$JREHOME/lib/security/java.security-用来指定运行安全模式下的各种参数(比如在哪里加载策略文件)\

```java
# The default is to have a single system-wide policy file,
# and a policy file in the user's home directory.
policy.url.1=file:${java.home}/lib/security/java.policy
policy.url.2=file:${user.home}/.java.policy
# whether or not we expand properties in the policy file
# if this is set to false, properties (${...}) will not be expanded in policy
# files.
policy.expandProperties=true
# whether or not we allow an extra policy to be passed on the command line
# with -Djava.security.policy=somefile. Comment out this line to disable
# this feature.
policy.allowSystemProperty=true
```

#### 代码

```java
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
public class PolicyTest {
    public static void file() {
        File f = new File("r.txt");
        InputStream is;
        try {
            is = new FileInputStream(f);
            byte[] content = new byte[1024];
            while (is.read(content) != -1) {
                System.out.println(new String(content));
            }
        } catch (FileNotFoundException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
    public static void main(String[] args) {
        // test read file.
        file();
    }
}
```

> 启动参数加入-Djava.security.manager使用安全沙箱模式运行,将会报错

```java
Exception in thread "main" java.security.AccessControlException: access denied("java.io.FilePermission" "D:githubCDLibsrcmainresourcessecurityr.txt" "read")
at java.security.AccessControlContext.checkPermission(Unknown Source)
at java.security.AccessController.checkPermission(Unknown Source)
at java.lang.SecurityManager.checkPermission(Unknown Source)
at java.lang.SecurityManager.checkRead(Unknown Source)
at java.io.FileInputStream.<init>(Unknown Source)
at com.taobao.cd.security.PolicyTest.main(PolicyTest.java:15)
```

这样,在权限文件中添加一条这样的规则

```java
grant {
    permission java.io.FilePermission "D:\\github\\CDLib\\src\\main\\resources\\security\\*", "read";
};
```

然后代码就通过了

### 结语

> 这个特性感觉使用的应该不多,框架里用的挺多,比较冷门记录一下





