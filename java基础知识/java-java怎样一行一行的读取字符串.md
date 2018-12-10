> 最近开发中遇到了一个问题,需要一行一行的读取字符串,自己想了想总结了两种方法\

#### 方法一  使用Scanner类

```java
import java.util.Scanner;
public class Main{
    public static void main(String[] args) {
        String info ="sdfsdfsdf\n"+"aaaaaa\n"+"bbbbbbbb\n";
        Scanner scanner = new Scanner(info);
        while(scanner.hasNext()){
            System.out.println(scanner.nextLine());
        }
    }
}
```

> 这种方法就是使用了Scanner特性,思路是将带换行符的字符串想象成聪明行进行输入的

#### 方法二 

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.StringReader;
public class Main{
    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(new StringReader("123\n456\n222222\n444"));
        try {
            String line;
            while((line=reader.readLine())!=null){
                System.out.println(line);
            }
        } catch (IOException e) {
        }finally {
            reader.close();
        }
    }
}
```
> 使用Reader进行处理