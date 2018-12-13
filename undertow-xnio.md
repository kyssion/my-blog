underttow 是redhat 开发的高性能服务器，具有jetty的易扩展和netty 高性能，之前阅读过部分undertow的源代码，发现undertow地成的异步框架使用的是xnio(并不是netty) 这里记录一下undertow 最底层xnio的使用方法

## XNIO有两个重要的概念： 

1. Channel，是传输管道的抽象概念，在NIO的Channel上进行的扩展加强，使用ChannelListener API进行事件通知。在创建Channel时，就赋予IO线程，用于执行所有的ChannelListener回调方法。 
2. 区分IO线程和工作线程，创建一个工作线程池可以用来执行阻塞任务。一般情况下，非阻塞的Handler由IO线程执行，而阻塞任务比如Servlet则被调度到工作线程池执行。这样就很好的区分了阻塞和非阻塞的两种情形。 (这一点和netty很类似)

> 引申：我们知道NIO的基本要求是不阻塞当前线程的执行，对于非阻塞请求的结果，可以用两种方式获得：一种是对于请求很快返回一个引用（如JDK中Future，XNIO中称为IoFuture，其中很多方法是类似的），过一段时间再查询结果；还有一种是当结果就绪时，调用事先注册的回调方法来通知（如NIO2的CompletionHandler，XNIO的ChannelListener）

> 重要概念： 在xnio中，有几个词出现频率很高，Source表示信息源头，Sink是信息目的地，Conduit是源头到目的地管道的抽象。

一个例子查看一下

```java
// 服务端
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.nio.charset.Charset;

import org.xnio.ChannelListener;
import org.xnio.IoUtils;
import org.xnio.OptionMap;
import org.xnio.Xnio;
import org.xnio.XnioWorker;
import org.xnio.channels.AcceptingChannel;
import org.xnio.channels.Channels;
import org.xnio.channels.ConnectedStreamChannel;

public final class SimpleEchoServer {

    public static void main(String[] args) throws Exception {

        // 定义读数据listener
        final ChannelListener<ConnectedStreamChannel> readListener =
                new ChannelListener<ConnectedStreamChannel>() {
                    public void handleEvent(ConnectedStreamChannel channel) {
                        //分配缓冲
                        final ByteBuffer buffer = ByteBuffer.allocate(512);
                        final Charset charset = Charset.forName("utf-8");
                        int res;
                        try {
                            while ((res = channel.read(buffer)) > 0) {
                                //切换到写的状态并用阻塞的方式写回
                                buffer.flip();
                                final CharBuffer chars = charset.decode(buffer);
                                System.out.print(chars);
                                buffer.flip();
                                Channels.writeBlocking(channel,buffer);
                            }
                            // 保证全部送出
                            Channels.flushBlocking(channel);
                            if (res == -1) {
                                channel.close();
                            } else {
                                channel.resumeReads();
                            }
                        } catch (IOException e) {
                            e.printStackTrace();
                            IoUtils.safeClose(channel);
                        }
                    }
                };
        // 创建接收 listener.
        final ChannelListener<AcceptingChannel<ConnectedStreamChannel>> acceptListener =
                new ChannelListener<AcceptingChannel<ConnectedStreamChannel>>() {
                    public void handleEvent(
                            final AcceptingChannel<ConnectedStreamChannel> channel) {
                        try {
                            ConnectedStreamChannel accepted;
                            // channel就绪，准备接收连接请求
                            while ((accepted = channel.accept()) != null) {
                                System.out.println("accepted " + accepted.getPeerAddress());
                                // 已经连接，设置读数据listener
                                accepted.getReadSetter().set(readListener);
                                // 恢复读的状态
                                accepted.resumeReads();
                            }
                        } catch (IOException ignored) {
                        }
                    }
                };

        //创建Xnio实例，并构造XnioWorker
        final XnioWorker worker = Xnio.getInstance().createWorker(OptionMap.EMPTY);
        // 创建server，在本地12345端口上侦听
        AcceptingChannel<? extends ConnectedStreamChannel> server = worker
                .createStreamServer(new InetSocketAddress(12345),
                        acceptListener, OptionMap.EMPTY);
        // 开始接受连接
        server.resumeAccepts();
        System.out.println("Listening on " + server.getLocalAddress());
    }
}

//请求端
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.nio.charset.Charset;

import org.xnio.IoFuture;
import org.xnio.IoUtils;
import org.xnio.OptionMap;
import org.xnio.Xnio;
import org.xnio.XnioWorker;
import org.xnio.channels.Channels;
import org.xnio.channels.ConnectedStreamChannel;

public final class SimpleHelloWorldBlockingClient {

    public static void main(String[] args) throws Exception {
        
        final Charset charset = Charset.forName("utf-8");
        //创建Xnio实例，并构造XnioWorker
        final Xnio xnio = Xnio.getInstance();
        final XnioWorker worker = xnio.createWorker(OptionMap.EMPTY);

        try {
            //连接服务器，本地12345端口，注意返回值是IoFuture类型，并不阻塞，返回后可以做些别的事情
            final IoFuture<ConnectedStreamChannel> futureConnection = worker.connectStream(
                    new InetSocketAddress("localhost", 12345), null, OptionMap.EMPTY);
            final ConnectedStreamChannel channel = futureConnection.get(); // get是阻塞调用
            try {
                // 发送消息
                Channels.writeBlocking(channel, ByteBuffer.wrap("Hello world!\n".getBytes(charset)));
                // 保证全部送出
                Channels.flushBlocking(channel);
                // 发送EOF
                channel.shutdownWrites();
                System.out.println("Sent greeting string! The response is...");
                ByteBuffer recvBuf = ByteBuffer.allocate(128);
                // 接收消息
                while (Channels.readBlocking(channel, recvBuf) != -1) {
                    recvBuf.flip();
                    final CharBuffer chars = charset.decode(recvBuf);
                    System.out.print(chars);
                    recvBuf.clear();
                }
            } finally {
                IoUtils.safeClose(channel);
            }
        } finally {
            worker.shutdown();
        }
    }
}
```

> 2018: ps - xnioworker 方法中的 connectStream 和 createStreamServer 已经被标记为过时, 建议采用

