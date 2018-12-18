### java nio支持的背后unix系统的五种IO模型

(1) 阻塞I/O模型

非常好理解最简单的IO模型

![](blogimg/java/javaNIO/1.png)

(2) 非阻塞I/O模型

其实本质上就是轮训来查找是否有可以进行读取的资源

![](blogimg/java/javaNIO/2.png)

(3) I/O复用模型

这个是select/poll,linux 的epoll是进化版,基于事件驱动模型性能更好

![](blogimg/java/javaNIO/3.png)

(4) 信号驱动I/O模型

![](blogimg/java/javaNIO/4.png)

(5) 异步I/O模型

这个就是AIO 全信号驱动模型

![](blogimg/java/javaNIO/5.png)

### java 集中io模型样例

#### BIO 模型

java 的同步阻塞模型是一对一的线程模型最大的缺点就是缺少弹性,单用户量增加的时候,系统的线程数出于一种线性的增加状态中

![](/blogimg/java/javaNIO/6.png)

> 服务端

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
public class ServerWorker implements Runnable{
    private Socket socket;
    public ServerWorker(Socket socket){
        this.socket = socket;
    }
    @Override
    public void run() {
        BufferedReader reader = null;
        PrintWriter writer = null;
        try {
            reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            writer = new PrintWriter(socket.getOutputStream());
            String question = reader.readLine();//没有内容会阻塞
            while(!question.equals("OVER")){
                String answer = getAnswer(question);
                writer.println(answer);
                question = reader.readLine();
            }
            writer.println("OVER");//OVER作为操作完成暗号
            writer.flush();
            if(writer != null){
                writer.close();
            }

            if(reader != null){
                reader.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    private static String getAnswer(String question){
        String answer = null;
        switch(question){
            case "who":
                answer = "我是小娜";
                break;
            case "what":
                answer = "我是来帮你解闷的";
                break;
            case "where":
                answer = "我来自外太空";
                break;
            default:
                answer = "请输入 who， 或者what， 或者where";
        }
        return answer;
    }
}
```

> 服务端使用线程池

```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class ServerHandlerExecutePool {
    private ExecutorService executorService;

    public ServerHandlerExecutePool(int maxPoolSize,int queueSize){
        executorService = new ThreadPoolExecutor(Runtime.getRuntime().availableProcessors(),maxPoolSize,
                120L, TimeUnit.SECONDS,new ArrayBlockingQueue<Runnable>(queueSize));
    }

    public void execute(Runnable task){
        executorService.execute(task);
    }
}

import com.magic.web.bio.ServerWorker;
import com.magic.web.bio.simple.BIOService;
import javax.net.ServerSocketFactory;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class BIOServiceWithExecute {
    public static void main(String[] args){
        BIOService bioService = new BIOService();
        ServerSocket serverSocket = null;
        Socket socket = null;
        try {
            //可以设置客户连接请求队列的长度，比如5，队列长度超过5后拒绝连接请求
            //serverSocket = ServerSocketFactory.getDefault().createServerSocket(8383, 5);
            serverSocket = ServerSocketFactory.getDefault().createServerSocket(8383);
            ServerHandlerExecutePool executePool = new ServerHandlerExecutePool(50,10000);
            while(true){
                try{
                    //监听直到接受连接后返回一个新Socket对象
                    socket = serverSocket.accept();//阻塞
                    //new一个线程处理连接请求
                    executePool.execute(new ServerWorker(socket));
                }
                catch (Throwable e) {    //防止发生异常搞死服务器
                    e.printStackTrace();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        finally{
            try {
                if(socket != null){
                    socket.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}

```

> 客户端
```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class BIOClient {
    public static void main(String[] args) {
        BIOClient c = new BIOClient();
        //种20个线程发起Socket客户端连接请求
        for (int i = 0; i < 20; i++) {
            new Thread(c.new Worker()).start();
        }
    }
    private class Worker implements Runnable {
        @Override
        public void run() {
            Socket socket = null;
            BufferedReader reader = null;
            PrintWriter writer = null;
            try {
                //创建一个Socket并连接到指定的目标服务器
                socket = new Socket("localhost", 8383);
                reader = new BufferedReader(new InputStreamReader(
                        socket.getInputStream()));
                writer = new PrintWriter(socket.getOutputStream());
                //TODO 这里必须是使用的println 因为读取的时候使用的就是 readline
                writer.println("who");
                writer.println("what");
                writer.println("where");
                writer.println("OVER");//OVER作为操作完成暗号
                writer.flush();
                String answer = reader.readLine();   //没有内容会阻塞
                while (!answer.equals("OVER")) {
                    System.out.println(Thread.currentThread().getId() + "---Message from server:" + answer);
                    answer = reader.readLine();
                }
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                try {
                    if (writer != null) {
                        writer.close();
                    }

                    if (reader != null) {
                        reader.close();
                    }

                    if (socket != null) {
                        socket.close();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
```

>　这种阻塞式网络io模型的缺点和优点

缺点: 

1. 