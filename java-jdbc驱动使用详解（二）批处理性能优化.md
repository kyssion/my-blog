##  java-jdbc驱动使用详解（二）批处理性能优化

> 在使用mysql的时候或多或少会遇见大量的批操作的情况这里整理一下经验

这里我们对三种情况进行测试

> 性能优化的方法，在url请求中加上这些参数，useServerPrepStmts=true&cachePrepStmts=true&rewriteBatchedStatements=true

组号|是否开起服务端预处理和预处理缓存|是否使用事务提交方法|是否使用批处理方法|1w（毫秒）|100w（毫秒）
---|---|---|---|---|---
第一组|N|N|N|添加 : 39619，修改 : 41440，删除 : 39734|大于一小时
第二组|Y|N|N|添加 : 38741，修改 : 41146，删除 : 39538|大于一小时
第三组|N|Y|N|添加 : 1145，修改 : 1321，删除 : 926|添加 : 80560，修改 : 122566，删除 : 92001
第四组|Y|Y|N|添加 : 674，修改 : 1114，删除 : 859|添加 : 76134，修改 : 116780，删除 : 88954
第五组|N|N|Y|添加 : 72，修改 : 38930，删除 : 37931|大于一小时
第六组|Y|N|Y|添加 : 112，修改 : 38409，删除 : 37677|大于一小时
第七组|N|Y|Y|添加 : 54，修改 : 770，删除 : 510|添加 : 8925，修改 : 79631，删除 : 46655
第八组|Y|Y|Y|添加 : 88，修改 : 729，删除 : 444|添加 : 9401，修改 : 78899，删除 : 47316

### 测试代码

```java
package org;
 
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.Calendar;
 
/*
进行单机的myql压力测试
 */
public class Main {
    static {
        try {
            Class.forName("com.mysql.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
 
    public static int times = 10000;
 
    public static void main(String[] args) throws SQLException {
        for (int a=0;a<3;a++) {
            System.out.println("第"+a+"次"+"次数："+times);
            System.out.println("N,N,N");
            method1();
            System.out.println("N,Y,N");
            method2();
            System.out.println("Y,N,N");
            method3();
            System.out.println("Y,Y,N");
            method4();
            System.out.println("N,N,Y");
            method8();
            System.out.println("N,Y,Y");
            method6();
            System.out.println("Y,N,Y");
            method7();
            System.out.println("Y,Y,Y");
            method5();
            System.out.println("---------------------------------------------------------------");
            times=times*10;
        }
    }
 
    public static Connection tool(String data, String... args) throws SQLException {
        String url = "jdbc:mysql://127.0.0.1" + "/" + data;
        String user = "root";
        String password = "14159265jkl";
        for (String item : args) {
            url += "?" + item;
        }
        return DriverManager.getConnection(url, user, password);
    }
 
    public static long start = 0;
 
    public static void start() {
        start = Calendar.getInstance().getTimeInMillis();
    }
 
    public static void end(String info) {
        System.out.println(info + " : " + (Calendar.getInstance().getTimeInMillis() - start));
    }
 
    /*
        不使用服务器预编译，不使用事物提交使用自动提交,不使用批处理
     */
    public static void method1() throws SQLException {
        Connection con = tool("TestOther");
        PreparedStatement statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.execute();
        }
        end("不使用服务器预编译，不使用事物提交使用自动提交,不使用批处理-增加");
        statement = con.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.execute();
        }
        end("不使用服务器预编译，不使用事物提交使用自动提交,不使用批处理-修改");
        statement = con.prepareStatement("delete FROM tbone where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.execute();
        }
        end("不使用服务器预编译，不使用事物提交使用自动提交,不使用批处理-删除");
        statement.close();
        con.close();
    }
 
    /*
        不使用服务器预编译，使用事务提交,不使用批处理
     */
    public static void method2() throws SQLException {
        Connection con = tool("TestOther");
        con.setAutoCommit(false);
        PreparedStatement statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.execute();
        }
        con.commit();
        end("不使用服务器预编译，使用事务提交,不使用批处理-添加");
        statement = con.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.execute();
        }
        con.commit();
        end("不使用服务器预编译，使用事务提交,不使用批处理-修改");
        statement = con.prepareStatement("delete FROM tbone where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.execute();
        }
        con.commit();
        end("不使用服务器预编译，使用事务提交,不使用批处理-删除");
        statement.close();
        con.close();
    }
 
    /*
        使用服务器预编译，不使用事务提交方法,不使用批处理
     */
    public static void method3() throws SQLException {
        //开起服务端预编译，开起预编译缓存，
        Connection con = tool("TestOther", new String[]{"useServerPrepStmts=true&cachePrepStmts=true"});
        PreparedStatement statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.execute();
        }
        end("使用服务器预编译，不使用事务提交方法,不使用批处理-增加");
        statement = con.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.execute();
        }
        end("使用服务器预编译，不使用事务提交方法,不使用批处理-修改");
        statement = con.prepareStatement("delete FROM tbone where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.execute();
        }
        end("使用服务器预编译，不使用事务提交方法,不使用批处理-删除");
        statement.close();
        con.close();
    }
 
    /*
       使用服务器预编译，使用事务提交方法,不使用批处理
    */
    public static void method4() throws SQLException {
        //开起服务端预编译，开起预编译缓存，
        Connection con = tool("TestOther", new String[]{"useServerPrepStmts=true&cachePrepStmts=true"});
        con.setAutoCommit(false);
        PreparedStatement statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.execute();
        }
        con.commit();
        end("使用服务器预编译，使用事务提交,不使用批处理-添加");
        statement = con.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.execute();
        }
        con.commit();
        end("使用服务器预编译，使用事务提交,不使用批处理-修改");
        statement = con.prepareStatement("delete FROM tbone where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.execute();
        }
        con.commit();
        end("使用服务器预编译，使用事务提交,不使用批处理-删除");
        statement.close();
        con.close();
    }
 
    /*
        使用服务器预编译，使用事务，使用批处理
     */
    public static void method5() throws SQLException {
        //开起服务端预编译，开起预编译缓存，
        Connection con = tool("TestOther", new String[]{"useServerPrepStmts=true&cachePrepStmts=true&rewriteBatchedStatements=true"});
        con.setAutoCommit(false);
        PreparedStatement statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.addBatch();
            if (a % 10000 == 0) {
                statement.executeBatch();
            }
        }
        statement.executeBatch();
        con.commit();
        end("使用服务器预编译，使用事务提交,使用批处理-添加");
        statement = con.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.addBatch();
            if (a % 10000 == 0) {
                statement.executeBatch();
            }
        }
        statement.executeBatch();
        con.commit();
        end("使用服务器预编译，使用事务提交,使用批处理-修改");
        statement = con.prepareStatement("delete FROM tbone where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.addBatch();
            if (a % 10000 == 0) {
                statement.executeBatch();
            }
        }
        statement.executeBatch();
        con.commit();
        end("使用服务器预编译，使用事务提交,使用批处理-删除");
        statement.close();
        con.close();
    }
 
    /*
        不使用服务器预编译，使用事务，使用批处理
     */
    public static void method6() throws SQLException {
        //开起服务端预编译，开起预编译缓存，
        Connection con = tool("TestOther", new String[]{"useServerPrepStmts=false&cachePrepStmts=true&rewriteBatchedStatements=true"});
        con.setAutoCommit(false);
        PreparedStatement statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.addBatch();
            if (a % 10000 == 0) {
                statement.executeBatch();
            }
        }
        statement.executeBatch();
        con.commit();
        end("不使用服务器预编译，使用事务提交,使用批处理-添加");
        statement = con.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.addBatch();
            if (a % 10000 == 0) {
                statement.executeBatch();
            }
        }
        statement.executeBatch();
        con.commit();
        end("不使用服务器预编译，使用事务提交,使用批处理-修改");
        statement = con.prepareStatement("delete FROM tbone where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.addBatch();
            if (a % 10000 == 0) {
                statement.executeBatch();
            }
        }
        statement.executeBatch();
        con.commit();
        end("不使用服务器预编译，使用事务提交,使用批处理-删除");
        statement.close();
        con.close();
    }
 
    /*
        使用服务器预编译，不使用事务，使用批处理
     */
    public static void method7() throws SQLException {
        //开起服务端预编译，开起预编译缓存，
        Connection con = tool("TestOther", new String[]{"useServerPrepStmts=true&cachePrepStmts=true&rewriteBatchedStatements=true"});
        PreparedStatement statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.addBatch();
            if (a % 10000 == 0) {
                statement.executeBatch();
            }
        }
        statement.executeBatch();
        end("使用服务器预编译，不使用事务，使用批处理-添加");
        statement = con.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.addBatch();
            if (a % 10000 == 0) {
                statement.executeBatch();
            }
        }
        statement.executeBatch();
        end("使用服务器预编译，不使用事务，使用批处理-修改");
        statement = con.prepareStatement("delete FROM tbone where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.addBatch();
            if (a % 10000 == 0) {
                statement.executeBatch();
            }
        }
        statement.executeBatch();
        end("使用服务器预编译，不使用事务，使用批处理-删除");
        statement.close();
        con.close();
    }
 
    /*
        不使用服务器预编译，不使用事务，使用批处理
     */
    public static void method8() throws SQLException {
        //开起服务端预编译，开起预编译缓存，
        Connection con = tool("TestOther", new String[]{"useServerPrepStmts=false&cachePrepStmts=true&rewriteBatchedStatements=true"});
        PreparedStatement statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.addBatch();
            if (a % 10000 == 0) {
                statement.executeBatch();
            }
        }
        statement.executeBatch();
        end("不使用服务器预编译，不使用事务，使用批处理-添加");
        statement = con.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.addBatch();
            if (a % 10000 == 0) {
                statement.executeBatch();
            }
        }
        statement.executeBatch();
        end("不使用服务器预编译，不使用事务，使用批处理-修改");
        statement = con.prepareStatement("delete FROM tbone where id=?");
        start();
        for (int a = 0; a < times; a++) {
            statement.setInt(1, a);
            statement.addBatch();
            if (a % 10000 == 0) {
                statement.executeBatch();
            }
        }
        statement.executeBatch();
        end("不使用服务器预编译，不使用事务，使用批处理-删除");
        statement.close();
        con.close();
    }
}
```