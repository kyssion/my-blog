java io 操作是一个非常重要的工具包,同样也是网络编程和各种框架编写的基本函数库,这里做一下整理

## java io的层次结构

![](blogimg/java/javaIO.png)

这里就先整理一下我最长用的吧

BufferReader和BufferWriter 这两个提供了writer 和 readLine 的功能
InputStreamReader和OutputStreamWriter 这两个提供了字节流转字符流的方法
PrintWriter 可以 象System.out.println() 那样的输入流
