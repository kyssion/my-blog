一开始其实用这个题目作为文章的标题很难受，但是没有办法java的文件获取就是这么负载:cold_sweat:

# java获取数据获取文件系统的api

这个就不罗嗦了，就是java的文件操作FileInputStream等等

# java如果获取jar中的文件怎么做

java 有一个特殊的api的ClassLoader.getResource()与getResources()

简单的说这个api是干嘛的,加载类路径资源文件,也就是classPath中的东西（也就是可以拿到classpath中的所有东西包括jar中的东西）

直接上源码

```java
package org.mirror.reflection.io;

import java.io.File;
import java.net.JarURLConnection;
import java.net.URL;
import java.util.Enumeration;
import java.util.HashSet;
import java.util.Set;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;

public class ClassFindUtil {

    /**
     * 获取类加载器
     */
    public static ClassLoader getClassLoader() {
        return Thread.currentThread().getContextClassLoader();
    }

    /**
     * 加载类
     */
    public static Class<?> loadClass(String className, boolean isInitialized) {
        Class<?> cls;
        try {
            cls = Class.forName(className, isInitialized, getClassLoader());
        } catch (ClassNotFoundException e) {
            throw new RuntimeException(e);
        }
        return cls;
    }

    /**
     * 加载类（默认将初始化类）
     */
    public static Class<?> loadClass(String className) {
        return loadClass(className, true);
    }

    /**
     * 获取指定包名下的所有类
     */
    public static Set<Class<?>> getClassSet(String packageName) {
        Set<Class<?>> classSet = new HashSet<Class<?>>();
        try {
            Enumeration<URL> urls = getClassLoader().getResources(packageName.replace(".", "/"));
            while (urls.hasMoreElements()) {
                URL url = urls.nextElement();
                if (url != null) {
                    String protocol = url.getProtocol();
                    if (protocol.equals("file")) {
                        String packagePath = url.getPath().replaceAll("%20", " ");
                        addClass(classSet, packagePath, packageName);
                    } else if (protocol.equals("jar")) {
                        JarURLConnection jarURLConnection = (JarURLConnection) url.openConnection();
                        if (jarURLConnection != null) {
                            JarFile jarFile = jarURLConnection.getJarFile();
                            if (jarFile != null) {
                                Enumeration<JarEntry> jarEntries = jarFile.entries();
                                while (jarEntries.hasMoreElements()) {
                                    JarEntry jarEntry = jarEntries.nextElement();
                                    String jarEntryName = jarEntry.getName();
                                    if (jarEntryName.endsWith(".class")) {
                                        String className = jarEntryName.substring(0, jarEntryName.lastIndexOf(".")).replaceAll("/", ".");
                                        if(className.startsWith(packageName)){
                                            doAddClass(classSet, className);
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        return classSet;
    }

    private static void addClass(Set<Class<?>> classSet, String packagePath, String packageName) {
        File[] files = new File(packagePath).
                listFiles(file -> (file.isFile() && file.getName().endsWith(".class")) || file.isDirectory());
        if(files==null){
            return;
        }
        for (File file : files) {
            String fileName = file.getName();
            if (file.isFile()) {
                String className = fileName.substring(0, fileName.lastIndexOf("."));
                if (isNotEmpty(packageName)) {
                    className = packageName + "." + className;
                }
                doAddClass(classSet, className);
            } else {
                String subPackagePath = fileName;
                if (isNotEmpty(packagePath)) {
                    subPackagePath = packagePath + "/" + subPackagePath;
                }
                String subPackageName = fileName;
                if (isNotEmpty(packageName)) {
                    subPackageName = packageName + "." + subPackageName;
                }
                addClass(classSet, subPackagePath, subPackageName);
            }
        }
    }

    private static void doAddClass(Set<Class<?>> classSet, String className) {
        Class<?> cls = loadClass(className, false);
        classSet.add(cls);
    }
    /**
     * 判断字符串是否为空
     */
    public static boolean isEmpty(String str) {
        if (str != null) {
            str = str.trim();
        }
        return null==str||"".equals(str);
    }

    /**
     * 判断字符串是否非空
     */
    public static boolean isNotEmpty(String str) {
        return !isEmpty(str);
    }

    /**
     * 分割固定格式的字符串
     */
    public static String[] splitString(String str, String separator) {
        if(str==null){
            return new String[0];
        }
        return str.split(separator);
    }
}
```

注意代码这一段Enumeration<URL> urls = getClassLoader().getResources(packageName.replace(".", "/"));

返回值石URL类型，注意在java中这个url其实有多种协议构成的，file前缀表示在classpath文件路径中的资源，而jar前缀表示在jar中的资源

> 如果是file前缀的资源

这种情况下就当成基本的文件数据流来处理就好了其实很简单

> 如果石jar前缀的资源

这个地方要注意一下，有一个坑，就是如果jvm发现这个地方有我们需要的资源我们需要通过JarURLConnection jarURLConnection = (JarURLConnection) url.openConnection();这个api来获取资源的引用，但是呢这个引用会将这个jar中所有的文件都加载进来，所以在使用的时候需要做一个过滤。

# 总结一下

上面的代码已经实现了一个java jar中文件的搜索，网络上有类似的代码，但是实际情况是有一些bug的，这里我做了一些修改（因为我们传入的是指定的包，但是jar加载会把整个jar文件全部加载进来，所以我在里面加了一个过滤操作），现在已经可以稳定运行了。

