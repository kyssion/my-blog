## netty(0)-netty demo 和netty的基本组建

### 一.首先展示这个demo的目录结构

![](blogimg/netty/4.png)
EchoClient 和 EchoServer 分别表示 客户端和服务端的运行程序，对应的Handler 数据调用的时候相关的操作方法

### 二.代码

- choClient.class

```java
public class EchoClient {
    private final String host;
    private final int port;
    public EchoClient(String host, int port) {
        this.host = host;
        this.port = port;
    }
    public static void main(String[] args) throws Exception {
        new EchoClient("127.0.0.1",3330).start();
    }
    public void start() throws Exception{
        EventLoopGroup group = new NioEventLoopGroup();
        try {
            Bootstrap bootstrap = new Bootstrap();
            bootstrap.group(group)
                    .channel(NioSocketChannel.class)
                    .remoteAddress(new InetSocketAddress(host,port))
                    .handler(new ChannelInitializer<SocketChannel>() {
                        protected void initChannel(SocketChannel ch) throws Exception {
                            ch.pipeline().addLast(new EchoClientHandler());
                        }
                    });
            ChannelFuture future = bootstrap.connect().sync();
            future.channel().closeFuture().sync();
        } finally {
            group.shutdownGracefully().sync();
        }
    }
}
```

- EchoClientHandler.class

```java
public class EchoClientHandler extends SimpleChannelInboundHandler<ByteBuf> {
    protected void channelRead0(ChannelHandlerContext ctx, ByteBuf msg) throws Exception {
        System.out.println("client received: "+ msg.toString(CharsetUtil.UTF_8));
    }
    @Override
    public void channelActive(ChannelHandlerContext ctx) throws Exception {
        ctx.writeAndFlush(Unpooled.copiedBuffer("Netty rocks!",CharsetUtil.UTF_8));
    }
    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {
        cause.printStackTrace();
        ctx.close();
    }
}
```

- EchoServer.class

```java
public class EchoServer {
    private final int port;//帮顶相关的接口
    public EchoServer(int port) {
        this.port = port;
    }
    public static void main(String[] args) throws Exception {
        new EchoServer(3330).start();
    }
    public void start() throws Exception {
        final EchoServerHandler serverHandler = new EchoServerHandler();
        EventLoopGroup group = new NioEventLoopGroup();
        try {
            ServerBootstrap b = new ServerBootstrap();
            b.group(group).channel(NioServerSocketChannel.class)
                    .localAddress(new InetSocketAddress(port))
                    .childHandler(new ChannelInitializer<SocketChannel>() {
                        @Override
                        protected void initChannel(SocketChannel ch) throws Exception {
                            ch.pipeline().addLast(serverHandler);
                        }
                    });
            ChannelFuture f = b.bind().sync();
            f.channel().closeFuture().sync();
        } finally {
            group.shutdownGracefully().sync();
        }
    }
}
```

- EchoServerHandler.class

```java
@ChannelHandler.Sharable//表示一个ChannelHandler 可以被多个Channel安全的共享
public class EchoServerHandler extends ChannelInboundHandlerAdapter{
    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        ByteBuf in= (ByteBuf) msg;
        System.out.println("server received: " + in.toString(CharsetUtil.UTF_8));
        ctx.write(in);//表示相关的写法写给发送这而不冲刷相关的消息
    }
    @Override
    public void channelReadComplete(ChannelHandlerContext ctx) throws Exception {
        //将未觉消息冲刷到远程节点，并且关闭该Channel
        ctx.writeAndFlush(Unpooled.EMPTY_BUFFER).addListener(ChannelFutureListener.CLOSE);
    }
    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) throws Exception {
        cause.printStackTrace();
        ctx.close();
    }
}
```

## 介绍一下netty的基本组成有那些

### Bootstrap

这个基本类是一个便利的基本工厂用来实现netty 快速配置的方法类

bootstrap实现netty快速配置的过程是这样的

![](blogimg/netty/16.png)

```java
try {   //1 设置reactor 线程
    b.group(bossLoopGroup, workerLoopGroup);
    //2 设置nio类型的channel
    b.channel(NioServerSocketChannel.class);
    //3 设置监听端口
    b.localAddress(new InetSocketAddress(port));
    //4 设置通道选项
    b.option(ChannelOption.SO_KEEPALIVE, true);
    b.option(ChannelOption.ALLOCATOR, PooledByteBufAllocator.DEFAULT);

    //5 装配流水线
    b.childHandler(new ChannelInitializer<SocketChannel>()
    {
        //有连接到达时会创建一个channel
        protected void initChannel(SocketChannel ch) throws Exception
        {
            ch.pipeline().addLast(new ProtobufDecoder());
            ch.pipeline().addLast(new ProtobufEncoder());
            // pipeline管理channel中的Handler
            // 在channel队列中添加一个handler来处理业务
            ch.pipeline().addLast("serverHandler", serverHandler);
        }
    });
    // 6 开始绑定server
    // 通过调用sync同步方法阻塞直到绑定成功

    ChannelFuture channelFuture = b.bind().sync();
    LOGGER.info(ChatServer.class.getName() +
            " started and listen on " + 
            channelFuture.channel().localAddress());

    // 7 监听通道关闭事件
    // 应用程序会一直等待，直到channel关闭
    ChannelFuture closeFuture=  channelFuture.channel().closeFuture();
    closeFuture.sync();
} catch (Exception e){
    e.printStackTrace();
} finally{
    // 8 优雅关闭EventLoopGroup，
    // 释放掉所有资源包括创建的线程
    workerLoopGroup.shutdownGracefully();
    bossLoopGroup.shutdownGracefully();
}
```

> netty 其实提供了两组的bootstrap ， 和serverBootstrap 分别对应client端和server端

### eventloop group 

netty 是基于事件循环的，并且是muilt-eventLoop （多线程版eventloop）

在服务端，netty提供了两套线程组类来供eventloop使用 bossloopGroup 和 wordloopGroup

！[](blogimg/netty/17.png)

分离的取决于netty的架构设计，之前我们说过netty的服务端channel分为parent channel 和childern channel，分别负责创建链接和使用链接

loopGroup也是这样进行分组的

- bossLoopGroup 表示服务器连接监听线程组，专门接受 accept 新的客户端client 连接

- workerGroup 表示处理每一条连接的数据收发的线程组

在线程组和启动器都创建完成后，就可以开始设置线程组：通过 b.group(bossGroup, workerGroup) 方法，给引导器配置两大线程组。
配置完成之后，整个引导类的 reactor 线程正式确定。这里确定的工作模式，为父子线程的模型。

如果只设置一个线程组，具体的方法为 —— b.group( workerGroup) 。
配置完成一个线程组，则所有的 channel ，包括服务监听通道父亲channel 和所有的子channel ，都工作在同一个线程组中。

### channel Channelhandle ChannelHandleContext ChannelPipeline

channel在netty中其实是对应一种链接类型（或者说socket的类型）

netty 目前的链接类型大约是如下的几种

- NioSocketChannel, 代表异步的客户端 TCP Socket 连接.
- NioServerSocketChannel, 异步的服务器端 TCP Socket 连接.
- NioDatagramChannel, 异步的 UDP 连接
- NioSctpChannel, 异步的客户端 Sctp 连接.
- NioSctpServerChannel, 异步的 Sctp 服务器端连接.
- OioSocketChannel, 同步的客户端 TCP Socket 连接.
- OioServerSocketChannel, 同步的服务器端 TCP Socket 连接.
- OioDatagramChannel, 同步的 UDP 连接
- OioSctpChannel, 同步的 Sctp 服务器端连接.
- OioSctpServerChannel, 同步的客户端 TCP Socket 连接.

netty 其实可以说90%以上的设计点都是在channel方法上，这里说明一下netty的chanel有那些

#### 1. netty channel

netty在设计的时候其实channel分为parent channel和childern channel

> parent channel:服务器连接监听的channel,用来坚监听服务器链接和创建链接
> childern channel:一个socket 对应的channel,由parent channel 创建的channel

总结channel其实就是netty实际链接的一种抽象

#### 2. channelhandle
ChannelHandler用于处理Channel对应的事件 （netty定义了大量的事件，通过这些事件调用对应的handle方法）
ChannelHandler接口里面只定义了三个生命周期方法，我们主要实现它的子接口ChannelInboundHandler和ChannelOutboundHandler，为了便利，框架提供了ChannelInboundHandlerAdapter，ChannelOutboundHandlerAdapter和ChannelDuplexHandler这三个适配类，在使用的时候只需要实现你关注的方法即可

ChannelInboundHandler 事件：

| 回调方法                  | 触发时机                                                   | client | server |
|---------------------------|------------------------------------------------------------|--------|--------|
| channelRegistered         | 当前channel注册到EventLoop                                 | true   | true   |
| channelUnregistered       | 当前channel从EventLoop取消注册                             | true   | true   |
| channelActive             | 当前channel激活的时候                                      | true   | true   |
| channelInactive           | 当前channel不活跃的时候，也就是当前channel到了它生命周期末 | true   | true   |
| channelRead               | 当前channel从远端读取到数据                                | true   | true   |
| channelReadComplete       | channel read消费完读取的数据的时候被触发                   | true   | true   |
| userEventTriggered        | 用户事件触发的时候                                         | FALSE  | FALSE  |
| channelWritabilityChanged | channel的写状态变化的时候触发                              | FALSE  | FALSE  |

ChannelOutboundHandler：

| 回调方法   | 触发时机                  | client | server |
|------------|------------------------|--------|--------|
| bind       | bind操作执行前触发        | false  | true   |
| connect    | connect 操作执行前触发    | true   | false  |
| disconnect | disconnect 操作执行前触发 | true   | false  |
| close      | close操作执行前触发       | false  | true   |
| deregister | deregister操作执行前触发  |        |        |
| read       | read操作执行前触发        | true   | true   |
| write      | write操作执行前触发       | true   | true   |
| flush      | flush操作执行前触发       | true   | true   |



#### 3. channelhandlecontext

这个是 channelhandle的一种封装，可以理解为中间层，相当于netty的数据层和调度层的中间层

当一个channelHandle 加入到netty中的时候，netty将会自动的将这个channelhandle包装成 channelhandlecontext，供上方使用

> 注意channelhandleContext的数据其实非常封闭的，他只能处理自己的和之后的数据 并不能应修改这个流程中的所有数据，如果进行修改的是channel或者channlePipeline 的话，从头重新掉用数据

#### 3. ChannelPipeline

这个就是一个channelhandlecontext处理节点的一个集合， 一个channel（数据源）对应一个channelPopeline，一个channelPipeline对应一组channelhandleContext.

channelPipeline > 其实就是eventloop处理队列的一个抽象，修改channelPipeline中的数据将会影响整个netty对应这个channel的处理方式

#### 4 .整体总结

![](blogimg/netty/18.png)

![](blogimg/netty/19.webp)

![](blogimg/netty/20.webp)

![](blogimg/netty/21.jpg)

1. 一个channel对应一个channelPopeline 一个channelPipeline 对应一组 channelContext 一个channelContext承载一个channelhandle

2. 处理进入的时候走的是ChannelInboundHandler接口的处理实现类，吐出的时候走的是ChannelOutboundHandler接口的实现类

3. netty提供了两个通用的handle

> HeadContext

HeadContext实现了ChannelOutboundHandler，ChannelInboundHandler这两个接口
```java
class HeadContext extends AbstractChannelHandlerContext
            implements ChannelOutboundHandler, ChannelInboundHandler
```

因为在头部，所以说HeadContext中关于in和out的回调方法都会触发
关于ChannelInboundHandler，HeadContext的作用是进行一些前置操作，以及把事件传递到下一个ChannelHandlerContext的ChannelInboundHandler中去

>   TailContext
TailContext实现了ChannelInboundHandler接口，会在ChannelInboundHandler调用链最后执行，只要是对调用链完成处理的情况进行处理，看下channelRead实现
```java
public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
    onUnhandledInboundMessage(msg);
}
protected void onUnhandledInboundMessage(Object msg) {
    try {
        logger.debug(
                "Discarded inbound message {} that reached at the tail of the pipeline. " +
                        "Please check your pipeline configuration.", msg);
    } finally {
        ReferenceCountUtil.release(msg);
    }
}
```

###  ChannelFuture

这个已经是netty最后一个组建，这个方法用来通知netty中channel的状态，因为netty是异步的，所以通过这种方法来实现一个监控

> ps 从这里我们也可以明白了其实如果netty需要增加一个链接一定会再实现上面的这一套操作创建一个新的future

```java
// 6 开始绑定server
// 通过调用sync同步方法阻塞直到绑定成功

ChannelFuture channelFuture = b.bind().sync();
LOGGER.info(ChatServer.class.getName() +
        " started and listen on " + 
        channelFuture.channel().localAddress());

// 7 监听通道关闭事件
// 应用程序会一直等待，直到channel关闭
ChannelFuture closeFuture=  channelFuture.channel().closeFuture();
closeFuture.sync();
```
