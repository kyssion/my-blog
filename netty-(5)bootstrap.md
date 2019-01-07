其实对于任何框架来说,都会有一个公共的入口,在netty中这个入口被叫做 bootstrap 引导

引导类的层次结构包括一个抽象的父类和两个具体的引导子类

![](/blogimg/netty/13.png)

针对上图我们能看出来,特定于客户端或者服务器的引导步骤则分别由Bootstrap或ServerBootstrap处理

> 注意: 你有时可能会需要创建多个具有类似配置或者完全相同配置的Channel。为了支持这种模式而又不需要为每个Channel都创建并配置一个新的引导类实例，AbstractBootstrap被标记为了Cloneable[5]。在一个已经配置完成的引导类实例上调用clone()方法将返回另一个可以立即使用的引导类实例。

注意:这种方式只会创建引导类实例的EventLoopGroup的一个浅拷贝，所以，后者[6]将在所有克隆的Channel实例之间共享。这是可以接受的，因为通常这些克隆的Channel的生命周期都很短暂，一个典型的场景是——创建一个Channel以进行一次HTTP请求。

### 客户端引导程序

Bootstrap类负责为客户端和使用无连接协议的应用程序创建Channel

![](/blogimg/netty/14.png)

```java
EventLoopGroup group = new NioEventLoopGroup();
 Bootstrap bootstrap = new Bootstrap();   //  创建一个Bootstrap类的实例以创建和连接新的客户端Channel
 bootstrap.group(group)　 // 设置EventLoopGroup，提供用于处理Channel事件的EventLoop
　　 .channel(NioSocketChannel.class)　  //   指定要使用的Channel 实现
　　 .handler(new SimpleChannelInboundHandler<ByteBuf>() {  //  设置用于Channel 事件和数据的ChannelInboundHandler
　　　　　@Override
　　　　 protected void channeRead0(
　　　　　　 ChannelHandlerContext channelHandlerContext,
　　　　　　 ByteBuf byteBuf) throws Exception {
　　　　　　 System.out.println("Received data");
　　　　　}
　　 } );
ChannelFuture future = bootstrap.connect(
　　new InetSocketAddress("www.manning.com", 80));  //   连接到远程主机
future.addListener(new ChannelFutureListener() {
　　@Override
　　public void operationComplete(ChannelFuture channelFuture)
　　　　throws Exception {
　　　　if (channelFuture.isSuccess()) {
　　　　　 System.out.println("Connection established");
　　　　} else {
　　　　　 System.err.println("Connection attempt failed");
　　　　　 channelFuture.cause().printStackTrace();
　　　　}
　　 }
} );
```

### 服务端引导程序

下图展示了ServerBootstrap在bind()方法被调用时创建了一个ServerChannel，并且该ServerChannel管理了多个子Channel。

![](/blogimg/netty/15.png)

```java
NioEventLoopGroup group = new NioEventLoopGroup();
ServerBootstrap bootstrap = new ServerBootstrap();   //  创建ServerBootstrap
bootstrap.group(group)　 //  设置EventLoopGroup，其提供了用于处理Channel 事件的EventLoop
　　.channel(NioServerSocketChannel.class)　 //  指定要使用的Channel 实现 
　　.childHandler(new SimpleChannelInboundHandler<ByteBuf>() {   //  设 置用于处理已被接受的子Channel的I/O及数据的ChannelInbound-Handler
　　　　@Override
　　　　protected void channelRead0(ChannelHandlerContext ctx,
　　　　　　ByteBuf byteBuf) throws Exception {
　　　　　　System.out.println("Received data");
　　　　}
　　} );
ChannelFuture future = bootstrap.bind(new InetSocketAddress(8080));    // 通过配置好的ServerBootstrap的实例绑定该Channel
future.addListener(new ChannelFutureListener() {
　　@Override
　　public void operationComplete(ChannelFuture channelFuture)
　　　　throws Exception {
　　　　if (channelFuture.isSuccess()) {
　　　　　　System.out.println("Server bound");
　　　　} else {
　　　　　　System.err.println("Bound attempt failed");
　　　　　　channelFuture.cause().printStackTrace();
　　　　}
　　}
} );
```

### 当从channel中生成引导使用新的EventLoop

在netty中一个EventLoop对应一个线程,为了降低系统的性能损耗,在netty中使用了Bootstrap的group方法来重用EventLoop

```java
ServerBootstrap bootstrap = new ServerBootstrap();   //  创建ServerBootstrap 以创建ServerSocketChannel，并绑定它
bootstrap.group(new NioEventLoopGroup(), new NioEventLoopGroup())　 //  设置EventLoopGroup，其将提供用以处理Channel 事件的EventLoop
　　.channel(NioServerSocketChannel.class)　 //  指定要使用的Channel 实现 
　　.childHandler(　 //  设置用于处理已被接受的子Channel 的I/O 和数据的ChannelInboundHandler　
　　　　new SimpleChannelInboundHandler<ByteBuf>() {
　　　　　　ChannelFuture connectFuture;
　　　　　　@Override
　　　　　　public void channelActive(ChannelHandlerContext ctx)
　　　　　　　　throws Exception {
　　　　　　　　Bootstrap bootstrap = new Bootstrap();　 //  创建一个Bootstrap类的实例以连接到远程主机
　　　　　　　　bootstrap.channel(NioSocketChannel.class).handler(  //  指定Channel的实现　
　　　　　　　　　　new SimpleChannelInboundHandler<ByteBuf>() {   // 为入站I/O 设置ChannelInboundHandler
　　　　　　　　　　　　@Override
　　　　　　　　　　　　protected void channelRead0(
　　　　　　　　　　　　　　ChannelHandlerContext ctx, ByteBuf in)
　　　　　　　　　　　　　　throws Exception {
　　　　　　　　　　　　　　System.out.println("Received data");
　　　　　　　　　　　　}
　　　　　　　　　　} );
　　　　　　　　bootstrap.group(ctx.channel().eventLoop());　 //  使用与分配给已被接受的子Channel 相同的EventLoop
　　　　　　　　connectFuture = bootstrap.connect(
　　　　　　　　　　new InetSocketAddress("www.manning.com", 80));   //  连接到远程节点
　　　　　　}
　　　　　　@Override
　　　　　　protected void channelRead0(
　　　　　　　　ChannelHandlerContext channelHandlerContext,
　　　　　　　　　　ByteBuf byteBuf) throws Exception {
　　　　　　　　if (connectFuture.isDone()) {
　　　　　　　　　　// do something with the data　 //  当连接完成时，执行一些数据操作（如代理）
　　　　　　　　}
　　　　　　}
　　　　} );
ChannelFuture future = bootstrap.bind(new InetSocketAddress(8080));　 //  通过配置好的ServerBootstrap绑定该Server-SocketChannel
future.addListener(new ChannelFutureListener() {
　　@Override
　　public void operationComplete(ChannelFuture channelFuture)
　　　　throws Exception {
　　　　if (channelFuture.isSuccess()) {
　　　　　　System.out.println("Server bound");
　　　　} else {
　　　　　　System.err.println("Bind attempt failed");
　　　　　　channelFuture.cause().printStackTrace();
　　　　}
　　}
} );
```

### netty handle的初始化操作

Netty提供了一个特殊的ChannelInboundHandlerAdapter子类
```java
public abstract class ChannelInitializer<C extends Channel>
　　extends ChannelInboundHandlerAdapter
```
提实现了一个特殊方法

```java
protected abstract void initChannel(C ch) throws Exception;
```

这个子类或者说handle 一旦被注册到了它的EventLoop之后，就会调用你的initChannel()方法。在该方法返回之后，ChannelInitializer的实例将会从Channel-Pipeline中移除它自己。


```java
ServerBootstrap bootstrap = new ServerBootstrap();　 //  创建ServerBootstrap 以创建和绑定新的Channel 
bootstrap.group(new NioEventLoopGroup(), new NioEventLoopGroup())　 //  设置EventLoopGroup，其将提供用以处理Channel 事件的EventLoop
　　.channel(NioServerSocketChannel.class)　 //   指定Channel 的实现
　　.childHandler(new ChannelInitializerImpl());　  // 注册一个ChannelInitializerImpl 的实例来设置ChannelPipeline 
 ChannelFuture future = bootstrap.bind(new InetSocketAddress(8080));  // 绑定到地址
future.sync();
final class ChannelInitializerImpl extends ChannelInitializer {[10]  // 用以设置ChannelPipeline 的自定义ChannelInitializerImpl 实现
　　@Override
　　protected void initChannel(Channel ch) throws Exception { // 将所需的ChannelHandler添加到ChannelPipeline
　　　　ChannelPipeline pipeline = ch.pipeline();
　　　　pipeline.addLast(new HttpClientCodec());
　　　　pipeline.addLast(new HttpObjectAggregator(Integer.MAX_VALUE));
　　}
}
```

### netty 的配置属性和传递性参数属性

netty的bootstrap 提供了 option() 方法来将ChannelOption 配置进系统中,提供了方便的配置方法

并且netty的引导还提供了AttributeMap(一个由Channel和引导类提供的集合)和AttributeKey<T>(一个用于插入和获取属性值的泛型类),通过这种方法,就可以将相关的属性传递到服务中的channel中去了

```java
final AttributeKey id = AttributeKey.newInstance("ID");  [11] //  创建一个AttributeKey以标识该属性
Bootstrap bootstrap = new Bootstrap();　 //  创建一个Bootstrap 类的实例以创建客户端Channel 并连接它们
bootstrap.group(new NioEventLoopGroup())　  //  设置EventLoopGroup，其提供了用以处理Channel事件的EventLoop
.channel(NioSocketChannel.class)　 //  指定Channel的实现
.handler(
　　new SimpleChannelInboundHandler() {　 // 设置用以处理Channel 的I/O 以及数据的Channel-InboundHandler 
　　　　@Override
　　　　public void channelRegistered(ChannelHandlerContext ctx)
　　　　　　throws Exception {
　　　　　　Integer idValue = ctx.channel().attr(id).get();　 // 使用AttributeKey 检索属性以及它的值
　　　　　　// do something with the idValue
　　　　}
　　　　@Override
　　　　protected void channelRead0(
　　　　　　ChannelHandlerContext channelHandlerContext,
　　　　　　ByteBuf byteBuf) throws Exception {
　　　　　　System.out.println("Received data");
　　　　}
　　}
);
bootstrap.option(ChannelOption.SO_KEEPALIVE,true)
　　.option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 5000);　 //  设置ChannelOption，其将在connect()或者bind()方法被调用时被设置到已经创建的Channel 上
bootstrap.attr(id, 123456);　 //  存储该id 属性　
ChannelFuture future = bootstrap.connect(
　　new InetSocketAddress("www.manning.com", 80));  //  使用配置好的Bootstrap实例连接到远程主机
future.syncUninterruptibly();
```

### netty的关闭

netty的优雅关闭

```java
EventLoopGroup group = new NioEventLoopGroup();  //  创建处理I/O 的EventLoopGroup
Bootstrap bootstrap = new Bootstrap();　 //  创建一个Bootstrap类的实例并配置它
bootstrap.group(group)
　　.channel(NioSocketChannel.class);
...
Future<?> future = group.shutdownGracefully();　 //  shutdownGracefully()方法将释放所有的资源，并且关闭所有的当前正在使用中的Channel
// block until the group has shutdown
future.syncUninterruptibly();
```

你需要关闭EventLoopGroup，它将处理任何挂起的事件和任务，并且随后释放所有活动的线程。这就是调用EventLoopGroup.shutdownGracefully()方法的作用。这个方法调用将会返回一个Future，这个Future将在关闭完成时接收到通知。需要注意的是，shutdownGracefully()方法也是一个异步的操作，所以你需要阻塞等待直到它完成，或者向所返回的Future注册一个监听器以在关闭完成时获得通知。

或者，你也可以在调用EventLoopGroup.shutdownGracefully()方法之前，显式地在所有活动的Channel上调用Channel.close()方法。但是在任何情况下，都请记得关闭EventLoopGroup本身。