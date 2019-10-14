
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


### netty 的 channelPipeLine 接口

channelPipline 其实是一个调度链处理器,用来处理channel和对应的handle的执行过程

每一个channel都被分配了一个唯一的pipeline,这项关联是永久性的；Channel既不能附加另外一个ChannelPipeline，也不能分离其当前的。

根据事件的起源，事件将会被ChannelInboundHandler或者ChannelOutboundHandler处理。随后，通过调用ChannelHandlerContext的实现，它将被转发给同一超类型的下一个ChannelHandler

> ChannelHandlerContext:ChannelHandlerContext使得ChannelHandler能够和它的ChannelPipeline以及其他的ChannelHandler交互。ChannelHandler可以通知其所属的ChannelPipeline中的下一个ChannelHandler，甚至可以动态修改它所属的ChannelPipeline。


当你完成了通过调用ChannelPipeline.add*()方法将入站处理器（ChannelInboundHandler）和出站处理器（ChannelOutboundHandler）混合添加到ChannelPipeline之后，每一个ChannelHandler从头部到尾端的顺序位置正如同我们添加的时候那样。

在ChannelPipeline传播事件时，它会测试ChannelPipeline中的下一个Channel- Handler的类型是否和事件的运动方向相匹配。如果不匹配，ChannelPipeline将跳过该ChannelHandler并前进到下一个，直到它找到和该事件所期望的方向相匹配的为止。

> channelPipeline接口的方法


|名　　称|描　　述|
|---|---|
|addFirst|将一个ChannelHandler添加到ChannelPipeline中|
|addBeforeaddAfteraddLast||
|remove|将一个ChannelHandler从ChannelPipeline中移除|
|replace|将ChannelPipeline中的一个ChannelHandler替换为另一个ChannelHandler|

```java
ChannelPipeline pipeline = ..;
FirstHandler firstHandler = new FirstHandler();   //  创建一个FirstHandler 的实例
pipeline.addLast("handler1", firstHandler);　 //  将该实例作为"handler1" 添加到ChannelPipeline 中
pipeline.addFirst("handler2", new SecondHandler());　 //  将一个SecondHandler的实例作为"handler2"添加到ChannelPipeline的第一个槽中。这意味着它将被放置在已有的"handler1"之前 
pipeline.addLast("handler3", new ThirdHandler());　 //  将一个ThirdHandler 的实例作为"handler3"添加到ChannelPipeline 的最后一个槽中　
...
pipeline.remove("handler3");　 //  通过名称移除"handler3"　 
pipeline.remove(firstHandler);　 //  通过引 用移除FirstHandler（它是唯一的，所以不需要它的名称）　
pipeline.replace("handler2", "handler4", new ForthHandler());  //  将SecondHandler("handler2")替换为FourthHandler:"handler4"
```

> 有时可能需要与那些使用阻塞API的遗留代码进行交互。对于这种情况，ChannelPipeline有一些接受一个EventExecutorGroup的add()方法。如果一个事件被传递给一个自定义的EventExecutor- Group，它将被包含在这个EventExecutorGroup中的某个EventExecutor所处理，从而被从该Channel本身的EventLoop中移除。对于这种用例，Netty提供了一个叫DefaultEventExecutor- Group的默认实现。

> channelPipeline 来访问ChannelHandler的方法

|名　　称|描　　述|
|---|---|
|get|通过类型或者名称返回ChannelHandler|
|context|返回和ChannelHandler绑定的ChannelHandlerContext|
|names|返回ChannelPipeline中所有ChannelHandler的名称|

> channelPipeline 事件触发方法

1. 入站事件

|方法名称|描　　述|
|---|---|
|fireChannelRegistered|调用ChannelPipeline中下一个ChannelInboundHandler的channelRegistered(ChannelHandlerContext)方法|
|fireChannelUnregistered|调用ChannelPipeline中下一个ChannelInboundHandler的channelUnregistered(ChannelHandlerContext)方法|
|fireChannelActive|调用ChannelPipeline中下一个ChannelInboundHandler的channelActive(ChannelHandlerContext)方法|
|fireChannelInactive|调用ChannelPipeline中下一个ChannelInboundHandler的channelInactive(ChannelHandlerContext)方法|
|fireExceptionCaught|调用ChannelPipeline中下一个ChannelInboundHandler的exceptionCaught(ChannelHandlerContext,Throwable)方法|
|fireUserEventTriggered|调用ChannelPipeline中下一个ChannelInboundHandler的userEventTriggered(ChannelHandlerContext,Object)方法|
|fireChannelRead|调用ChannelPipeline中下一个ChannelInboundHandler的channelRead(ChannelHandlerContext,Objectmsg)方法|
|fireChannelReadComplete|调用ChannelPipeline中下一个ChannelInboundHandler的channelReadComplete(ChannelHandlerContext)方法|
|fireChannelWritabilityChanged|调用ChannelPipeline中下一个ChannelInboundHandler的channelWritabilityChanged(ChannelHandlerContext)方法|

2. 出站事件

|方法名称|描　　述|
|---|---|
|bind|将Channel绑定到一个本地地址，这将调用ChannelPipeline中的下一个ChannelOutboundHandler的bind(ChannelHandlerContext,SocketAddress,ChannelPromise)方法|
|connect|将Channel连接到一个远程地址，这将调用ChannelPipeline中的下一个ChannelOutboundHandler的connect(ChannelHandlerContext,SocketAddress,ChannelPromise)方法|
|disconnect|将Channel断开连接。这将调用ChannelPipeline中的下一个ChannelOutboundHandler的disconnect(ChannelHandlerContext,ChannelPromise)方法|
|close|将Channel关闭。这将调用ChannelPipeline中的下一个ChannelOutboundHandler的close(ChannelHandlerContext,ChannelPromise)方法|
|deregister|将Channel从它先前所分配的EventExecutor（即EventLoop）中注销。这将调用ChannelPipeline中的下一个ChannelOutboundHandler的deregister(ChannelHandlerContext,ChannelPromise)方法|
|flush|冲刷Channel所有挂起的写入。这将调用ChannelPipeline中的下一个ChannelOutboundHandler的flush(ChannelHandlerContext)方法|
|write|将消息写入Channel。这将调用ChannelPipeline中的下一个ChannelOutboundHandler的write(ChannelHandlerContext,Objectmsg,ChannelPromise)方法。注意：这并不会将消息写入底层的Socket，而只会将它放入队列中。要将它写入Socket，需要调用flush()或者writeAndFlush()方法|
|writeAndFlush|这是一个先调用write()方法再接着调用flush()方法的便利方法|
|read|请求从Channel中读取更多的数据。这将调用ChannelPipeline中的下一个ChannelOutboundHandler的read(ChannelHandlerContext)方法|

总结一下：

- ChannelPipeline保存了与Channel相关联的ChannelHandler；
- ChannelPipeline可以根据需要，通过添加或者删除ChannelHandler来动态地修改；
- ChannelPipeline有着丰富的API用以被调用，以响应入站和出站事件。

### channelHandlerContext接口

ChannelHandlerContext代表了ChannelHandler和ChannelPipeline之间的关联，每当有ChannelHandler添加到ChannelPipeline中时，都会创建ChannelHandler- Context。ChannelHandlerContext的主要功能是管理它所关联的ChannelHandler和在同一个ChannelPipeline中的其他ChannelHandler之间的交互

ChannelHandlerContext有很多的方法，其中一些方法也存在于Channel和Channel- Pipeline本身上，但是有一点重要的不同。如果调用Channel或者ChannelPipeline上的这些方法，它们将沿着整个ChannelPipeline进行传播。而调用位于ChannelHandlerContext上的相同方法，则将从当前所关联的ChannelHandler开始，并且只会传播给位于该ChannelPipeline中的下一个能够处理该事件的ChannelHandler。

|方法名称|描　　述|
|---|---|
|alloc|返回和这个实例相关联的Channel所配置的ByteBufAllocator|
|bind|绑定到给定的SocketAddress，并返回ChannelFuture|
|channel|返回绑定到这个实例的Channel|
|close|关闭Channel，并返回ChannelFuture|
|connect|连接给定的SocketAddress，并返回ChannelFuture|
|deregister|从之前分配的EventExecutor注销，并返回ChannelFuture|
|disconnect|从远程节点断开，并返回ChannelFuture|
|executor|返回调度事件的EventExecutor|
|fireChannelActive|触发对下一个ChannelInboundHandler上的channelActive()方法（已连接）的调用|
|fireChannelInactive|触发对下一个ChannelInboundHandler上的channelInactive()方法（已关闭）的调用|
|fireChannelRead|触发对下一个ChannelInboundHandler上的channelRead()方法（已接收的消息）的调用|
|fireChannelReadComplete|触发对下一个ChannelInboundHandler上的channelReadComplete()方法的调用|
|fireChannelRegistered|触发对下一个ChannelInboundHandler上的fireChannelRegistered()方法的调用|
|fireChannelUnregistered|触发对下一个ChannelInboundHandler上的fireChannelUnregistered()方法的调用|
|fireChannelWritabilityChanged|触发对下一个ChannelInboundHandler上的fireChannelWritabilityChanged()方法的调用|
|fireExceptionCaught|触发对下一个ChannelInboundHandler上的fireExceptionCaught(Throwable)方法的调用|
|fireUserEventTriggered|触发对下一个ChannelInboundHandler上的fireUserEventTriggered(Objectevt)方法的调用|
|handler|返回绑定到这个实例的ChannelHandler|
|isRemoved|如果所关联的ChannelHandler已经被从ChannelPipeline中移除则返回true|
|name|返回这个实例的唯一名称|
|pipeline|返回这个实例所关联的ChannelPipeline|
|read|将数据从Channel读取到第一个入站缓冲区；如果读取成功则触发[5]一个channelRead事件，并（在最后一个消息被读取完成后）通知ChannelInboundHandler的channelReadComplete(ChannelHandlerContext)方法|
|write|通过这个实例写入消息并经过ChannelPipeline|
|writeAndFlush|通过这个实例写入并冲刷消息并经过ChannelPipeline|

当使用ChannelHandlerContext的API的时候，请牢记以下两点：

- ChannelHandlerContext和ChannelHandler之间的关联（绑定）是永远不会改变的，所以缓存对它的引用是安全的；
- 如同我们在本节开头所解释的一样，相对于其他类的同名方法，ChannelHandlerContext的方法将产生更短的事件流，应该尽可能地利用这个特性来获得最大的性能。


### netty 的异常处理

异常处理是任何真实应用程序的重要组成部分，它也可以通过多种方式来实现。因此，Netty提供了几种方式用于处理入站或者出站处理过程中所抛出的异常。

> 如果在处理入站事件的过程中有异常被抛出，那么它将从它在ChannelInboundHandler里被触发的那一点开始流经ChannelPipeline。要想处理这种类型的入站异常，你需要在你的ChannelInboundHandler实现中重写下面的方法。

```java
public class InboundExceptionHandler extends ChannelInboundHandlerAdapter {
　　@Override
　　public void exceptionCaught(ChannelHandlerContext ctx,
　　　　Throwable cause) {
　　　　cause.printStackTrace();
　　　　ctx.close();
　　}
}
```

因为异常会向入站方向流动,，所以实现了前面所示逻辑的ChannelInboundHandler通常位于ChannelPipeline的最后,确保了所有的入站异常都总是会被处理，无论它们可能会发生在ChannelPipeline中的什么位置

你应该如何响应异常，可能很大程度上取决于你的应用程序。你可能想要关闭Channel（和连接），也可能会尝试进行恢复。如果你不实现任何处理入站异常的逻辑（或者没有消费该异常），那么Netty将会记录该异常没有被处理的事实[7]。

总结一下：

- ChannelHandler.exceptionCaught()的默认实现是简单地将当前异常转发给ChannelPipeline中的下一个ChannelHandler；
- 如果异常到达了ChannelPipeline的尾端，它将会被记录为未被处理；
- 要想定义自定义的处理逻辑，你需要重写exceptionCaught()方法。然后你需要决定是否需要将该异常传播出去。

> 用于处理出站操作中的正常完成以及异常的选项，都基于以下的通知机制。

- 每个出站操作都将返回一个ChannelFuture。注册到ChannelFuture的Channel- FutureListener将在操作完成时被通知该操作是成功了还是出错了。
- 几乎所有的ChannelOutboundHandler上的方法都会传入一个ChannelPromise的实例。作为ChannelFuture的子类，ChannelPromise也可以被分配用于异步通知的监听器。但是，ChannelPromise还具有提供立即通知的可写方法：

```java
ChannelPromise setSuccess();
ChannelPromise setFailure(Throwable cause);
```

添加ChannelFutureListener只需要调用ChannelFuture实例上的addListener(ChannelFutureListener)方法，并且有两种不同的方式可以做到这一点。

方法一是，调用出站操作（如write()方法）所返回的ChannelFuture上的addListener()方法。

```java
ChannelFuture future = channel.write(someMessage);
future.addListener(new ChannelFutureListener() {
　　@Override
　　public void operationComplete(ChannelFuture f) {
　　　　if (!f.isSuccess()) {
　　　　　　f.cause().printStackTrace();
　　　　　　f.channel().close();
　　　　}
　　}
});
```

第二种方式是将ChannelFutureListener添加到即将作为参数传递给ChannelOut- boundHandler的方法的ChannelPromise

```java
public class OutboundExceptionHandler extends ChannelOutboundHandlerAdapter {
　　@Override
　　public void write(ChannelHandlerContext ctx, Object msg,
　　　　ChannelPromise promise) {
　　　　promise.addListener(new ChannelFutureListener() {
　　　　　　@Override
　　　　　　public void operationComplete(ChannelFuture f) {
　　　　　　　　if (!f.isSuccess()) {
　　　　　　　　　　f.cause().printStackTrace();
　　　　　　　　　　f.channel().close();
　　　　　　　　}
　　　　　　}
　　　　});
　　}
}
```

> 这种方式可以在全局上做了监听,也就是说如果整个ChannelOutboundHandler出现了问题,将会在ChannelPromise注册的监听其中进行监听