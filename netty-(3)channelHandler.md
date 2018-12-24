
之前有一个netty的数据流处理图

![](/blogimg/netty/8.png)

在这张图中可以体现出在ChannelPipeline中将ChannelHandler链接在一起以组织处理逻辑,并且使用ChannelHandlerContext传递参数

### ChannelHandler家族

1. channnel的生命周期

|状　　态|描　　述|
|---|---|
|ChannelUnregistered|Channel已经被创建，但还未注册到EventLoop|
|ChannelRegistered|Channel已经被注册到了EventLoop|
|ChannelActive|Channel处于活动状态（已经连接到它的远程节点）。它现在可以接收和发送数据了|
|ChannelInactive|Channel没有连接到远程节点|

channelHandler的状态扭转如下

![](/blogimg/netty/9.png)

2. channelHandler生命周期

在ChannelHandler被添加到ChannelPipeline中或者被从ChannelPipeline中移除时会调用这些操作。这些方法中的每一个都接受一个ChannelHandlerContext参数

channelHandlerContext在生命周期中的回调方法

|类　　型|描　　述|
|---|---|
|handlerAdded|当把ChannelHandler添加到ChannelPipeline中时被调用|
|handlerRemoved|当从ChannelPipeline中移除ChannelHandler时被调用|
|exceptionCaught|当处理过程中在ChannelPipeline中有错误产生时被调用|
|ChannelInactive|Channel没有连接到远程节点|

Netty定义了下面两个重要的ChannelHandler子接口：

- ChannelInboundHandler——处理入站数据以及各种状态变化；
- ChannelOutboundHandler——处理出站数据并且允许拦截所有的操作。

> channelInBoundHandler

用来处理输入流的处理方法,相比较原始的channelhandler接口,本方法扩展了一写一channel状态相关的方法,这些方法将会在数据被接收时或者与其对应的Channel状态发生改变时被调用。正如我们前面所提到的，这些方法和Channel的生命周期密切相关

|类　　型|描　　述|
|----|----|
|channelRegistered|当Channel已经注册到它的EventLoop并且能够处理I/O时被调用|
|channelUnregistered|当Channel从它的EventLoop注销并且无法处理任何I/O时被调用|
|channelActive|当Channel处于活动状态时被调用；Channel已经连接/绑定并且已经就绪|
|channelInactive|当Channel离开活动状态并且不再连接它的远程节点时被调用|
|channelReadComplete|当Channel上的一个读操作完成时被调用[1]|
|channelRead|当从Channel读取数据时被调用|
|ChannelWritabilityChanged|当Channel的可写状态发生改变时被调用。用户可以确保写操作不会完成得太快（以避免发生OutOfMemoryError）或者可以在Channel变为再次可写时恢复写入。可以通过调用Channel的isWritable()方法来检测Channel的可写性。与可写性相关的阈值可以通过Channel.config().setWriteHighWaterMark()和Channel.config().setWriteLowWaterMark()方法来设置|
|userEventTriggered|当ChannelnboundHandler.fireUserEventTriggered()方法被调用时被调用，因为一个POJO被传经了ChannelPipeline|

当某个ChannelInboundHandler的实现重写channelRead()方法时，它将负责显式地释放与池化的ByteBuf实例相关的内存。Netty为此提供了一个实用方法ReferenceCount-Util.release()

```java
@Sharable
public class DiscardHandler extends ChannelInboundHandlerAdapter {   // 扩展了Channel-InboundHandler-Adapter
　　@Override
　　public void channelRead(ChannelHandlerContext ctx, Object msg) {  // 丢弃已接收的消息
　　　　ReferenceCountUtil.release(msg);　
　　}
}
```

这样手动的进行资源的释放是比较麻烦的,netty提供了SimpleChannelInboundHandler可以自动的释放资源

```java
@Sharable
public class SimpleDiscardHandler
　　extends SimpleChannelInboundHandler<Object> {  //  扩展了SimpleChannelInboundHandler
　　@Override
　　public void channelRead0(ChannelHandlerContext ctx,
　　　　Object msg) {
　　　　// No need to do anything special　 // 不需要任何显式的资源释放
　　}
}
```

由于SimpleChannelInboundHandler会自动释放资源，所以你不应该存储指向任何消息的引用供将来使用，因为这些引用都将会失效。

> ChannelOutBoundHandler

出站操作和数据将由ChannelOutboundHandler处理。它的方法将被Channel、Channel- Pipeline以及ChannelHandlerContext调用。

ChannelOutboundHandler的一个强大的功能是可以按需推迟操作或者事件，这使得可以通过一些复杂的方法来处理请求。例如，如果到远程节点的写入被暂停了，那么你可以推迟冲刷操作并在稍后继续。

|类　　型|描　　述|
|---|---|
|bind(ChannelHandlerContext,SocketAddress,ChannelPromise)|当请求将Channel绑定到本地地址时被调用|
|connect(ChannelHandlerContext,|当请求将Channel连接到远程节点时被调用|
|SocketAddress,SocketAddress,ChannelPromise)||
|disconnect(ChannelHandlerContext,ChannelPromise)|当请求将Channel从远程节点断开时被调用|
|close(ChannelHandlerContext,ChannelPromise)|当请求关闭Channel时被调用|
|deregister(ChannelHandlerContext,ChannelPromise)|当请求将Channel从它的EventLoop注销时被调用|
|read(ChannelHandlerContext)|当请求从Channel读取更多的数据时被调用|
|flush(ChannelHandlerContext)|当请求通过Channel将入队数据冲刷到远程节点时被调用|
|write(ChannelHandlerContext,Object,ChannelPromise)|当请求通过Channel将数据写到远程节点时被调用|

> ChannelPromise与ChannelFuture　ChannelOutboundHandler中的大部分方法都需要一个ChannelPromise参数，以便在操作完成时得到通知。ChannelPromise是ChannelFuture的一个子类，其定义了一些可写的方法，如setSuccess()和setFailure()，从而使ChannelFuture不可变[2]。


### netty 内置处理器实现类ChannelInboundHandlerAdapter和ChannelOutboundHandlerAdapter

你可以使用ChannelInboundHandlerAdapter和ChannelOutboundHandlerAdapter类作为自己的ChannelHandler的起始点。这两个适配器分别提供了ChannelInboundHandler和ChannelOutboundHandler的基本实现。通过扩展抽象类ChannelHandlerAdapter，它们获得了它们共同的超接口ChannelHandler的方法。

![](/blogimg/netty/10.png)

ChannelHandlerAdapter还提供了实用方法isSharable()

如果其对应的实现被标注为Sharable，那么这个方法将返回true，表示它可以被添加到多个ChannelPipeline中

> 在ChannelInboundHandlerAdapter和ChannelOutboundHandlerAdapter中所提供的方法体调用了其相关联的ChannelHandlerContext上的等效方法，从而将事件转发到了ChannelPipeline中的下一个ChannelHandler中。

### netty资源的标准写法

```java
@Sharable
public class DiscardOutboundHandler
　　extends ChannelOutboundHandlerAdapter {  //  扩展了ChannelOutboundHandlerAdapter
　　@Override
　　public void write(ChannelHandlerContext ctx,
　　　　Object msg, ChannelPromise promise) {
　　　　ReferenceCountUtil.release(msg);　// 通过使用R eferenceCountUtil.realse(...)方法释放资源
　　　　promise.setSuccess();　 // 通知ChannelPromise数据已经被处理了
　　}
}
```

注意点:

1. 使用ReferenceCountUtil.release(msg); 释放资源
2. 使用promise.setSuccess();通知ChannelPromise数据已经被处理了

### netty 内置资源泄漏检测工具

每当通过调用ChannelInboundHandler.channelRead()或者ChannelOutbound- Handler.write()方法来处理数据时，你都需要确保没有任何的资源泄漏。你可能还记得在前面的章节中所提到的，Netty使用引用计数来处理池化的ByteBuf。所以在完全使用完某个ByteBuf后，调整其引用计数是很重要的。

为了帮助你诊断潜在的（资源泄漏）问题，Netty提供了class ResourceLeakDetector[3]，它将对你应用程序的缓冲区分配做大约1%的采样来检测内存泄露。

