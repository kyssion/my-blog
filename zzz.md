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