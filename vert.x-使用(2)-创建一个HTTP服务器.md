## vert.x 简单请求处理

```java
import io.vertx.core.MultiMap;
import io.vertx.core.Vertx;
import io.vertx.core.buffer.Buffer;
import io.vertx.core.http.HttpServer;
import io.vertx.core.http.HttpServerOptions;
import java.util.Iterator;
import java.util.Map;
public class WebHttpServer {
    public static void main(String[] args) {
        Vertx vertx = Vertx.vertx();
        HttpServerOptions options = new HttpServerOptions()
                .setMaxWebsocketFrameSize(1000000)
                .setLogActivity(true);
        HttpServer server = vertx.createHttpServer(options);
        server.requestHandler(res->{
            //这将返回一个实例MultiMap- 它类似于普通的Map或Hash，但允许同一个键的多个值 - 这是因为HTTP允许多个头值具有相同的键。
            MultiMap headers = res.headers();
            showMap("header",headers.iterator());
            System.out.println("absoluteURI:"+res.absoluteURI());
            System.out.println("uri:"+res.uri());
            System.out.println("host:"+res.host());
            System.out.println("path:"+res.path());
            System.out.println("query:"+res.query());
            System.out.println("remoteAddress:"+res.remoteAddress());
            MultiMap params = res.params();
            showMap("params",params.iterator());
            System.out.println(res.getParam("param1"));//这个方法只能获取一个值
            System.out.println(params.getAll("param1"));//通过这种方法可以获取多个相同的key的值
            res.response().end("Hello world");
            //使用handle 处理正文(post大字段非url请求)
            Buffer totalBuffer = Buffer.buffer();
            //因为body可能并不是一次性获取成功,需要多次聚合
            res.handler(buffer -> {
                System.out.println("I have received a chunk of the body of length " + buffer.length());
                totalBuffer.appendBuffer(buffer);
            });
            //当整个处理都结束(数据全部读取完)的时候,将会回调这个方法
            res.endHandler((end)->{
                System.out.println("handle end");
                //最终状态的时候一定可以获取到信息,所以直接处理之前缓存的
                System.out.println("Full body received, length = " + totalBuffer.length());
                System.out.println(totalBuffer.toString());
            });
            //vert.x 针对这种情况,将上面的方法统一的实现一个事件 bodyhandle
            res.bodyHandler(buf -> {
                System.out.println("Full body received, length = " + buf.length());
            });

        });
        server.listen(8888,"localhost", res -> {
            if (res.succeeded()) {
                System.out.println("Server is now listening!");
            } else {
                System.out.println("Failed to bind!");
            }
        });
    }
    public static void showMap(String title, Iterator<Map.Entry<String,String>> iterator){
        System.out.println("-------------<"+title+">-------------");
        while (iterator.hasNext()){
            Map.Entry<String,String> item = iterator.next();
            System.out.println(item.getKey()+"  "+item.getValue());
        }
        System.out.println("----------------------------------");
    }
}
```

总结一下,这里说的简单请求处理,其实就是不包括表单提交和文件上传的处理,总结一下

1. vert.x 提供了几种回调的用法

- handle : 最基本的请求处理方法,不保证数据完整
- endHandlle : 最终状态的处理器,这个时候数据完整
- bodyHandle : 专门处理简单类型大body的请求,相当于handle和endhandle配合使用的情况

2. vert.x 提供了非常方便的参数处理方法,提供了一个特殊的Map--MultiMap,通过这个方法可以很方便的获取header,params,表单(下面会说明名)中的数据,和普通map的不同点是,MultiMap支持相同的key的情况

## vert.x 的文件处理方法

## vert.x 的表单处理方法


