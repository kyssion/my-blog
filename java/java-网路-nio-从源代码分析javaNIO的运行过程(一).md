### 这一节解析一下 java NIO中 ServerSocketChannel创建的过程

> channel  在java中表示通道，是用来进行数据的有效传输

广义上来说通道可以被分为两类：**File I/O和Stream I/O，也就是文件通道和套接字通道**

如果分的更细致一点则是：

- FileChannel 从文件读写数据
- SocketChannel 通过TCP读写网络数据
- ServerSocketChannel 可以监听新进来的TCP连接，并对每个链接创建对应的SocketChannel
- DatagramChannel 通过UDP读写网络中的数据
- Pipe

通道既可以是单向的也可以是双向的。只实现ReadableByteChannel接口中的read()方法或者只实现WriteableByteChannel接口中的write()方法的通道皆为单向通道，同时实现ReadableByteChannel和WriteableByteChannel为双向通道，比如ByteChannel。对于socket通道来说，它们一直是双向的，而对于FileChannel来说，它同样实现了ByteChannel，但是我们知道**通过FileInputStream的getChannel（）获取的FileChannel只具有文件的只读权限**，那此时的在该通道调用write（）会出现什么情况？不出意外的抛出了NonWriteChannelException异常。
通过以上，我们得出结论：**通道都与特定的I/O服务挂钩，并且通道的性能受限于所连接的I/O服务的性质。**

通道的工作模式有两种：阻塞或非阻塞。在非阻塞模式下，调用的线程不会休眠，请求的操作会立刻返回结果；在阻塞模式下，调用的线程会产生休眠。**另外除FileChannel不能运行在非阻塞模式下，其余的通道都可阻塞运行也可以以非阻塞的方式运行。**

另外从SelectableChannel引申出的类可以和支持有条件选择的Selector结合使用，进而充分利用多路复用的I/O（multiplexed I/O）来提高性能.对于Socket通道类来说，通常与Selector共同使用以提高性能。需要**注意的是通道不能被重复使用，一个打开的通道代表着与一个特定I/O服务进行连接并封装了该连接的状态，通道一旦关闭，该连接便会断开。**通道的close（）比较特殊，无论在通道时在阻塞模式下还是非阻塞模式下，由于close（）方法的调用而导致底层I/O的关闭都可能会造成线程的暂时阻塞。在一个已关闭的通道上调用close（）并没有任何意义，只会立即返回。

###  现在进入正题，讨论一下ServerSocketChannel

Java NIO中的 ServerSocketChannel 是一个可以监听新进来的TCP连接的通道, 类似ServerSocket一样。要注意的是和DatagramChannel和SocketChannel不同，ServerSocketChannel本身不具备传输数据的能力，而只是负责监听传入的连接和创建新的SocketChannel。

![](/blogimg/nio/1.png)

#### 创建一个ServerSocket很简单，代码如下

```java
ServerSocketChannel channel= ServerSocketChannel.open();
```


#### 深入研究一下， 进入ServerSocketChannel的open方法

> ServerSocketChannel类 open方法

```java
public static ServerSocketChannel open() throws IOException {
	return SelectorProvider.provider().openServerSocketChannel();
}
```

这里首先将会调用SelectorProvider的provider方法,这一局将会返回一个SelectorProvider实例,主要作用就是使用spi或者-Dxxx参数传入的SelectorProvider的类url地址（类的包名加类名）返回一个imp实例

> SelectorProvider类  provider() 方法

```java
public static SelectorProvider provider() {
    synchronized (lock) {
        if (provider != null)
           return provider;
        return AccessController.doPrivileged(
            new PrivilegedAction<SelectorProvider>() {
                public SelectorProvider run() {
                        if (loadProviderFromProperty())
                            return provider;
                        if (loadProviderAsService())
                            return provider;
                        provider = sun.nio.ch.DefaultSelectorProvider.create();
                        return provider;
                    }
                });
    }
}
```

> 然后会调用实例的 openServerSocketChannel()方法

```java
public ServerSocketChannel openServerSocketChannel() throws IOException {
    return new ServerSocketChannelImpl(this);
}
```

这个方法将会真正的返回一个ServerSocketChannelImpl实例，这个类一般就是由虚拟机的厂商提供的，这里就不进行深入的研究了

### 最后看一下这个serversocketchannel个人觉得有用的方法

1. **public static ServerSocketChannel open() throws IOException** 开启一个serversocketchannel
2. **public final int validOps()**：返回这个通道支持的SelectionKey值，应为这个通道只是开启一个SocketChannel并没有信息交换的功能，只是监听功能，所有只能返回SelectionKey.OP_ACCEPT
3. **public final ServerSocketChannel bind(SocketAddress local)和public final ServerSocketChannel bind(SocketAddress local，int backlog)**：字如其意将一个套接字和本地地址链接，有一个重构方法提供最大链接数支持
4. **public ServerSocket socket()**：返回一个ServerSocket 
5. **public SocketChannel accept() throws IOException**：和传统的网络编程相同，如果使用的Nio那么将会立即的返回null否则将会阻塞住直到有链接建立
6. **public SocketAddress getLocalAddress() throws IOException**：返回这里绑定的地址
7. **public final SelectableChannel configureBlocking(boolean block) throws IOException**: 指定这个接口是阻塞的还是非阻塞的





