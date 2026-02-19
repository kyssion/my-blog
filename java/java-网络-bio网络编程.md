java的网络编程是一个硬茬

这里记录一下java 阻塞式网络编程的正确姿势

## 编写一个服务端程序

```java
public class setver {
    public static void main(String[] args) throws Exception {
        ServerSocket serverSocket = new ServerSocket(22222);
        BufferedReader bufferedReader = null;
        PrintWriter printWriter = null;
        Socket socket = serverSocket.accept();
        while(true){
            bufferedReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String msg = bufferedReader.readLine();
            printWriter = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())),true);
            System.out.println(msg);
            printWriter.println("server get msg : "+ msg);
            printWriter.flush();
            if(msg.equals("END")){
                break;
            }
        }
        printWriter.close();
        bufferedReader.close();
        serverSocket.close();
    }
}
```

## client端程序

```java
public class client {
    public static void main(String[] args) throws Exception {
        Socket socket = new Socket("127.0.0.1",22222);
        BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        PrintWriter printWriter = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())));
        BufferedReader lineRead = new BufferedReader(new InputStreamReader(System.in));
        String str = "";
        do{
            str = lineRead.readLine();
            printWriter.println(str);
            printWriter.flush();
            String msg = reader.readLine();
            System.out.println(msg);

        }while(!str.equals("end"));
    }
}
```

注意这种底层网络编程的坑点

1. java 的 tcp sockt 实现中一个socket和一个socket 一一对应
2. 要注意tcp读取的字节数量的问题,比如使用buffer的时候readLine 就是读取一个换行回车的数据,如果没有找到对应的标识符将不会返回的