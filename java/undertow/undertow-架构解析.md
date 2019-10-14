undertow 是在国外评测网站[techempower](https://www.techempower.com/benchmarks/#section=data-r17&hw=ph&test=json) 中评测排行头10高性能框架,同时也是spring boot 可以使用的web容器之一. 这里记录一下undertow的学习和使用的记录

### 基础列子 简单服务器构建和手动服务起构建

1. 简单服务器构建

>　其实通过源代码可知，简单服务器构建其实相当于使用了默认值的复杂服务器构建

```java
public class HelloWorldServer {
    public static void main(final String[] args) {
        Undertow server = Undertow.builder()
                .addHttpListener(8080, "localhost")
                .setHandler(new HttpHandler() {
                    @Override
                    public void handleRequest(final HttpServerExchange exchange) throws Exception {
                        exchange.getResponseHeaders().put(Headers.CONTENT_TYPE, "text/plain");
                        exchange.getResponseSender().send("Hello World");
                    }
                }).build();
        server.start();
    }
}
```

2. 手动组装服务器

```java
Xnio xnio = Xnio.getInstance();

XnioWorker worker = xnio.createWorker(OptionMap.builder()
        .set(Options.WORKER_IO_THREADS, ioThreads)
        .set(Options.WORKER_TASK_CORE_THREADS, workerThreads)
        .set(Options.WORKER_TASK_MAX_THREADS, workerThreads)
        .set(Options.TCP_NODELAY, true)
        .getMap());

OptionMap socketOptions = OptionMap.builder()
        .set(Options.WORKER_IO_THREADS, ioThreads)
        .set(Options.TCP_NODELAY, true)
        .set(Options.REUSE_ADDRESSES, true)
        .getMap();

Pool<ByteBuffer> buffers = new ByteBufferSlicePool(BufferAllocator.DIRECT_BYTE_BUFFER_ALLOCATOR,bufferSize, bufferSize * buffersPerRegion);


if (listener.type == ListenerType.AJP) {
    AjpOpenListener openListener = new AjpOpenListener(buffers, serverOptions, bufferSize);
    openListener.setRootHandler(rootHandler);
    ChannelListener<AcceptingChannel<StreamConnection>> acceptListener = ChannelListeners.openListenerAdapter(openListener);
    AcceptingChannel<? extends StreamConnection> server = worker.createStreamConnectionServer(new InetSocketAddress(Inet4Address.getByName(listener.host), listener.port), acceptListener, socketOptions);
    server.resumeAccepts();
} else if (listener.type == ListenerType.HTTP) {
    HttpOpenListener openListener = new HttpOpenListener(buffers, OptionMap.builder().set(UndertowOptions.BUFFER_PIPELINED_DATA, true).addAll(serverOptions).getMap(), bufferSize);
    openListener.setRootHandler(rootHandler);
    ChannelListener<AcceptingChannel<StreamConnection>> acceptListener = ChannelListeners.openListenerAdapter(openListener);
    AcceptingChannel<? extends StreamConnection> server = worker.createStreamConnectionServer(new InetSocketAddress(Inet4Address.getByName(listener.host), listener.port), acceptListener, socketOptions);
    server.resumeAccepts();
} else if (listener.type == ListenerType.HTTPS){
    HttpOpenListener openListener = new HttpOpenListener(buffers, OptionMap.builder().set(UndertowOptions.BUFFER_PIPELINED_DATA, true).addAll(serverOptions).getMap(), bufferSize);
    openListener.setRootHandler(rootHandler);
    ChannelListener<AcceptingChannel<StreamConnection>> acceptListener = ChannelListeners.openListenerAdapter(openListener);
    XnioSsl xnioSsl;
    if(listener.sslContext != null) {
        xnioSsl = new JsseXnioSsl(xnio, OptionMap.create(Options.USE_DIRECT_BUFFERS, true), listener.sslContext);
    } else {
        xnioSsl = xnio.getSslProvider(listener.keyManagers, listener.trustManagers, OptionMap.create(Options.USE_DIRECT_BUFFERS, true));
    }
    AcceptingChannel <SslConnection> sslServer = xnioSsl.createSslConnectionServer(worker, new InetSocketAddress(Inet4Address.getByName(listener.host), listener.port), (ChannelListener) acceptListener, socketOptions);
    sslServer.resumeAccepts();
}
```

> 这里其实是自己手动了设置了undertow(xnio)体系中各种组件, 具体的各个步骤的意义如下

- 创建一个XNIO工作者。此worker管理服务器的IO和Worker线程。

- 创建XNIO SSL实例（可选，仅在使用HTTPS时才需要）

- 创建相关Undertow侦听器类的实例

- 使用XNIO打开服务器套接字并设置其accept侦听器

### undertow的架构设计

首先说明一下undertwo的架构非常简单,大致拆分成如下的几个部分

1. xnio层

这个是undertow 底层使用的nio框架,比netty更加的轻量级

2. 管理IO和工作线程

在undertow 体系统中可以手动设置ThreadPool 而不适用java自己线程池

3. channel API 和 Listeners

undertow 是基于 java 的nio, channel api 本质上其实是 nio通道的一种封装.
listeners在undertow中最为channel api的监听表示,channel api将listener感兴趣的请求派发到listener中进行处理

> Undertow附带5个不同的监听器：HTTP / 1.1,HTTPS,AJP,HTTP / 2

4. 处理程序 handle

这个方法也就是我们需要实现的方法, 表示接受到请求后进行处理时的处理方法

### undertow 一些参数控制

1. xnio 主干参数

这个方法的参数主要是在

```java
org.xnio.Options
```

2. listener参数 

这个参数是用来配置listener的各种各种配置信息的参数主要在

```java
io.undertow.UndertowOptions
```

### undertow 的生命周期的交换结束

#### 请求生命周期

当客户端连接到服务器时，Undertow会创建一个io.undertow.server.HttpServerConnection。当客户端发送请求时，它由Undertow解析器解析，然后将结果io.undertow.server.HttpServerExchange传递给根处理程序。当根处理程序完成时，可能会发生以下四种情况之一：

> 交换可以完成

- 如果请求和响应通道都已完全读/写，则认为交换完成。对于没有内容的请求（例如GET和HEAD），请求方自动被视为完全读取。当处理程序写出完整响应并关闭并完全刷新响应通道时，读取端被视为完成。如果交易已经完成，那么在交易完成后不会采取任何行动。

> 根处理程序正常返回而不完成交换

- 在这种情况下，交换将通过呼叫完成HttpServerExchange.endExchange()。语义endExchange() 将在后面讨论。

> 根处理程序返回一个Exception

- 在这种情况下，500将设置响应代码，并且将使用结束交换HttpServerExchange.endExchange()。

> 根处理程序可以在HttpServerExchange.dispatch()调用之后或启动异步IO之后返回

- 在这种情况下，已调度的任务将提交给调度执行程序，或者如果已在请求或响应通道上启动了异步IO，则将启动此任务。在这种情况下，交换将不会完成，完成交换完成交换取决于您的异步任务。

到目前为止，最常见的用途HttpServerExchange.dispatch()是将执行从不允许阻塞的IO线程移动到工作线程，这允许阻塞操作。这种模式通常看起来像：

调度到工作线程

```java
public void handleRequest(final HttpServerExchange exchange) throws Exception {
    if (exchange.isInIoThread()) {
      exchange.dispatch(this);
      return;
    }
    //handler code
}
```

因为在调用堆栈返回之前实际上并不调度exchange，所以可以确保一次交换中的一个线程永远不会
活动。交换不是线程安全的，但是它可以在多个线程之间传递，只要两个线程不会立即尝试修改它，并且在第一个和第二个之间的操作（例如线程池调度）之前发生线程访问。

#### 结束交换

如上所述，一旦请求和响应通道都已关闭并刷新，则认为交换已完成。

有两种方法可以通过完全读取请求通道
1. 调用shutdownWrites()响应通道然后刷新它
2. 通过调用来结束交换HttpServerExchange.endExchange()。

当endExchange()调用时，Undertow将检查是否已生成内容，如果已生成，则它将简单地消耗请求通道，并关闭并刷新响应通道。如果没有，并且在交换机上注册了任何默认响应侦听器，那么Undertow将为每个人提供生成默认响应的机会。此机制是生成默认错误页面的方式。

endExchange() 会在内部调用 shutdownWrties方法

### undertow 阻塞流支持

HttpServerExchange(undertow对一次请求的抽象) 调用startBlocking() 返回一个BlockingHttpServerExchange  通过这个类可以正常调用HttpServerExchange.getInputStream()和 HttpServerExchange.getOutputStream()向他们写入数据

```java
BlockingHttpServerExchange blockingExchange=exchange.startBlocking();
```

### undertow 错误处理方法

处理异常的最简单方法是在外部处理程序中捕获它们。例如：

```java
public class ErrorHandler implements HttpHandler {

    @Override
    public void handleRequest(final HttpServerExchange exchange) throws Exception {
        try {
            next.handleRequest(exchange);
        } catch (Exception e) {
            if(exchange.isResponseChannelAvailable()) {
                //handle error
                //这里可以设置 hander.endExchange();
            }
        }
    }
}
```

### 响应监听器

undertow因为各个请求都是使用的异步操作,所有在监听响应的时候需要使用异步回调的方法来进行监听操作

```java
public class SimpleErrorPageHandler implements HttpHandler {

    private final HttpHandler next;

    public SimpleErrorPageHandler(final HttpHandler next) {
        this.next = next;
    }

    @Override
    public void handleRequest(final HttpServerExchange exchange) throws Exception {
        exchange.addDefaultResponseListener(new DefaultResponseListener() {
            @Override
            public boolean handleDefaultResponse(final HttpServerExchange exchange) {
                if (!exchange.isResponseChannelAvailable()) {
                    return false;
                }
                Set<Integer> codes = responseCodes;
                if (exchange.getResponseCode() == 500) {
                    final String errorPage = "<html><head><title>Error</title></head><body>Internal Error</body></html>";
                    exchange.getResponseHeaders().put(Headers.CONTENT_LENGTH, "" + errorPage.length());
                    exchange.getResponseHeaders().put(Headers.CONTENT_TYPE, "text/html");
                    Sender sender = exchange.getResponseSender();
                    sender.send(errorPage);
                    return true;
                }
                return false;
            }
        });
        next.handleRequest(exchange);
    }
}
```

### 各种内置hander

见 undertow 官方handle支持

[undertow handle](http://undertow.io/undertow-docs/undertow-docs-2.0.0/index.html#built-in-handlers-2)


### undertow servlet 支持

暂时略过以后有时间的时候再看这个不重要 只写一个例子吧

```java
public class ServletServer {
    public static final String MYAPP = "/myapp222";
    public static void main(final String[] args) {
        try {
            DeploymentInfo servletBuilder = deployment()
                    .setClassLoader(ServletServer.class.getClassLoader())
                    .setContextPath(MYAPP)
                    .setDeploymentName("test.war")
                    .addServlets(
                            servlet("MessageServlet", MessageServlet.class)
                                    .addInitParam("message", "Hello World")
                                    .addMapping("/my"),
                            servlet("MyServlet", MessageServlet.class)
                                    .addInitParam("message", "MyServlet")
                                    .addMapping("/myservlet"));

            DeploymentManager manager = Servlets.defaultContainer().addDeployment(servletBuilder);
            manager.deploy();
            HttpHandler servletHandler = manager.start();
            PathHandler path = Handlers.path()
                    .addPrefixPath("sdfsdfsdf", servletHandler);
            Undertow server = Undertow.builder()
                    .addHttpListener(8080, "localhost")
                    .setHandler(path)
                    .build();
            server.start();
        } catch (ServletException e) {
            throw new RuntimeException(e);
        }
    }
```