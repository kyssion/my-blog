## vert.x 创建一个TCP服务器是超级简单的

### 创建一个server端服务器

```java
import io.vertx.core.Vertx;
import io.vertx.core.buffer.Buffer;
import io.vertx.core.net.NetServer;

public class SocketServer {
    public static void main(String[] args) {
        Vertx vertx = Vertx.vertx();//开启一个vert.x
        NetServerOptions options = new NetServerOptions()
                    .setLogActivity(true);//开启网络监听日志
        NetServer netServer = vertx.createNetServer(options);//从vert.x中生成一个网络服务处理类
        netServer.connectHandler(socket -> {//添加链接成功的时候的回调函数,这个时候socket就是链接
            socket.handler(b -> {
                System.out.println("I received some bytes: " + b.length());
                System.out.println(b.toString());
                //发送请求的时候,新建缓冲池
                Buffer buffer = Buffer.buffer().appendFloat(12.34f).appendInt(123);
                socket.write(buffer);
                // Write a string in UTF-8 encoding
                socket.write("some data");
                // Write a string using the specified encoding
                socket.write("some data", "UTF-8");
            });
            //如果链接关闭了的会掉函数
            socket.closeHandler(v -> {
                System.out.println("The socket has been closed");
            });
            //针对异常的处理函数
            socket.exceptionHandler(throwable->{
                System.out.println("open throwable");
            });
        });
        //开启监听方法,这个方法不必须在指定了connectHandler之后才能初始化
        netServer.listen(33333,"localhost",res -> {
            if (res.succeeded()) {
                System.out.println("Server is now listening!");
            } else {
                System.out.println("Failed to bind!");
            }
        });
        //关闭服务器
        netServer.close(res->{
            if (res.succeeded()) {
                System.out.println("Server is now closed");
            } else {
                System.out.println("close failed");
            }
        });
    }
}
```

从这个方法中可以看出来vert.x自身的一切皆异步的特性,其实看上面的注释应该就可以理解了

### 创建一个客户端

```java
public class SockerClient {
    public static void main(String[] args) {
        Vertx vertx = Vertx.vertx();
        NetClientOptions options = new NetClientOptions()
                    .setConnectTimeout(10000)//超时10000毫秒
                    .setReconnectInterval(10)//重试10次
                    .setReconnectAttempts(500)//间隔500毫秒
                    .setLogActivity(true);//开启netty网络日志
        NetClient client = vertx.createNetClient(options);
        client.connect(33333, "localhost", res -> {//创建一个链接其实res就已经携带了这个链接的所有关键信息
            if (res.succeeded()) {
                System.out.println("Connected!");
                NetSocket socket = res.result();
                Buffer buffer = Buffer.buffer().appendBytes("this is test".getBytes());
                socket.write(buffer);
                // Write a string in UTF-8 encoding
                socket.write("some data");
                // Write a string using thespecified encoding
                socket.write("some data", "UTF-8");
                socket.handler(b->{//socket添加事件监听,来处理返回的数据
                    System.out.println("I received some bytes: " + b.length());
                    System.out.println(b.toString());
                }); 
            } else {
                System.out.println("Failed to connect: " + res.cause().getMessage());
            }
        });
        //关闭链接
        client.close();
    }
}
```

## vert.x tcp 其他特性

### 1. socket 检索 本地地址和远程地址

vert.x 提供了两种方法获取本地(我的地址)和远程地址(去链接的地址)

```java
socket.localAddress()//本地地址
socket.remoteAddress()//远程地址
```
### 2. socket 文件处理

vert.x 针对文件的处理方法同样非常简单使用sendfile方法就可以进行文件数据的发送了

```java
socket.sendFile("main.properties");
``` 

注意: 这个文件的地址必须是这个项目的相对路径地址

### 3. vert.x 的tcp使用的eventLoop,是在一个核心上运行的,如果要使用更好的性能,自动的扩展到多核心上去,可以采用一下的方法

```java
for (int i = 0; i < 10; i++) {
  NetServer server = vertx.createNetServer();
  server.connectHandler(socket -> {
    socket.handler(buffer -> {
      // Just echo back the data
      socket.write(buffer);
    });
  });
  server.listen(1234, "localhost");
}
```

> 果使用Verticle，则可以使用-instances命令行上的选项简单地部署服务器Verticle的更多实例：

```
vertx run com.mycompany.MyVerticle -instances 10
```
或者以编程方式部署Verticle

```java
DeploymentOptions options = new DeploymentOptions().setInstances(10);
vertx.deployVerticle("com.mycompany.MyVerticle", options);
```

执行此操作后，您会发现echo服务器在功能上与以前完全相同，但您的服务器上的所有核心都可以使用，并且可以处理更多工作。

## vert.x tcp 的SSL/TLS支持

可以将TCP客户端和服务器配置为使用传输层安全性 - 早期版本的TLS称为SSL

> 在服务器上启用SSL/TLS,并指定服务器的密钥/证书

1. 使用JDK附带的keytool实用程序管理Java密钥库

使用密钥文件初始化

```java
NetServerOptions options = new NetServerOptions()
            .setSsl(true)
            .setKeyStoreOptions(
                new JksOptions().
                    setPath("/path/to/your/server-keystore.jks").
                    setPassword("password-of-your-keystore")
);
NetServer server = vertx.createNetServer(options);
```

读取密钥存储区作为缓冲区并直接提供

```java
Buffer myKeyStoreAsABuffer = vertx.fileSystem().readFileBlocking("/path/to/your/server-keystore.jks");
JksOptions jksOptions = new JksOptions().
            setValue(myKeyStoreAsABuffer).
            setPassword("password-of-your-keystore");
NetServerOptions options = new NetServerOptions().
            setSsl(true).
            setKeyStoreOptions(jksOptions);
NetServer server = vertx.createNetServer(options);
``` 

2. PKCS＃12格式的密钥/证书

使用密钥文件初始化

```java
NetServerOptions options = new NetServerOptions()
    .setSsl(true).setPfxKeyCertOptions(
        new PfxOptions().
            setPath("/path/to/your/server-keystore.pfx").
            setPassword("password-of-your-keystore")
);
NetServer server = vertx.createNetServer(options);
```

读取密钥存储区作为缓冲区并直接提供

```java
Buffer myKeyStoreAsABuffer = vertx.fileSystem().readFileBlocking("/path/to/your/server-keystore.pfx");
PfxOptions pfxOptions = new PfxOptions().
  setValue(myKeyStoreAsABuffer).
  setPassword("password-of-your-keystore");
NetServerOptions options = new NetServerOptions().
  setSsl(true).
  setPfxKeyCertOptions(pfxOptions);
NetServer server = vertx.createNetServer(options);
```

3. 使用.pem文件分别提供服务器私钥和证书

使用密钥文件初始化

```java
NetServerOptions options = new NetServerOptions().setSsl(true).setPemKeyCertOptions(
  new PemKeyCertOptions().
    setKeyPath("/path/to/your/server-key.pem").
    setCertPath("/path/to/your/server-cert.pem")
);
NetServer server = vertx.createNetServer(options);
```

还支持缓冲区配置

```java
Buffer myKeyAsABuffer = vertx.fileSystem().readFileBlocking("/path/to/your/server-key.pem");
Buffer myCertAsABuffer = vertx.fileSystem().readFileBlocking("/path/to/your/server-cert.pem");
PemKeyCertOptions pemOptions = new PemKeyCertOptions().
  setKeyValue(myKeyAsABuffer).
  setCertValue(myCertAsABuffer);
NetServerOptions options = new NetServerOptions().
  setSsl(true).
  setPemKeyCertOptions(pemOptions);
NetServer server = vertx.createNetServer(options);
```

ps:暂时就看这么多吧,改天开个专题专门研究一下这个TSL/SSL