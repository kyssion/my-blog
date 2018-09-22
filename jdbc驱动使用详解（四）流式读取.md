## java-jdbc驱动使用详解（四）流式读取

mysql驱动默认的行为是需要把整个结果全部读取到内存中才开始允许应用读取结果，执行ResultSet的next方法是阻塞的，期望的方式是有数据就让人他返回，所以这里开发mysql的流式读取

```java

PreparedStatement ps = connection.prepareStatement("select .. from ..", 
            ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY); 
 
//forward only read only也是mysql 驱动的默认值，所以不指定也是可以的 比如： PreparedStatement ps = connection.prepareStatement("select .. from .."); 
 
ps.setFetchSize(Integer.MIN_VALUE); //也可以修改jdbc url通过defaultFetchSize参数来设置，这样默认所以的返回结果都是通过流方式读取.
ResultSet rs = ps.executeQuery(); 
 
while (rs.next()) { 
　　System.out.println(rs.getString("fieldName")); 
}
```
mysql判断是否开启流式读取结果的方法，有三个条件forward-only，read-only，fatch size是Integer.MIN_VALUE