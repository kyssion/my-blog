## java-jdbc驱动使用详解（三）单机分库分表下的性能测试

上一篇进行过测试，批处理和事务提交结合，可以显著的提升数据库增删改操作的性能，但是有一个问题——在多表和多数据库情况下使用多线程编程性能会提升多少。为了解决这个问题进行了如下的测试

### 测试代码

```java
package org;
 
 
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.Calendar;
import java.util.concurrent.atomic.AtomicInteger;
 
/*
    测试同库不同表和不同库不同表的性能之间的差别
 */
public class MainT {
    static AtomicInteger atomicInteger = new AtomicInteger(0);
 
    static class ExecuteThread extends Thread {
        PreparedStatement preparedStatement;
        Connection connection;
 
        public ExecuteThread(PreparedStatement statement, Connection connection) {
            this.preparedStatement = statement;
            this.connection = connection;
        }
 
        @Override
        public void run() {
            try {
                preparedStatement.executeBatch();
            } catch (SQLException e) {
                e.printStackTrace();
            }
            try {
                connection.commit();
            } catch (SQLException e) {
                e.printStackTrace();
            }
            atomicInteger.addAndGet(1);
        }
    }
 
    static {
        try {
            Class.forName("com.mysql.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
 
    public static int times = 1000000;
 
    public static void main(String[] args) throws SQLException {
        method1();
        method2();
        method3();
        //method4();
        //method5();
        //method6();
    }
 
    public static long time = 0;
 
    public static void start() {
        time = Calendar.getInstance().getTimeInMillis();
    }
 
    public static void end(String string) {
        System.out.println(string + " " + "time is:" + (Calendar.getInstance().getTimeInMillis() - time));
    }
 
    /*
        同数据库 多练接 事务批处理
     */
    public static void method1() throws SQLException {
        Connection con = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/TestOther?useServerPrepStmts=true&cachePrepStmts=true&rewriteBatchedStatements=true", "root", "14159265jkl");
        Connection con2 = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/TestOther?useServerPrepStmts=true&cachePrepStmts=true&rewriteBatchedStatements=true", "root", "14159265jkl");
        con.setAutoCommit(false);
        con2.setAutoCommit(false);
        PreparedStatement statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
        PreparedStatement statement2 = con2.prepareStatement("insert into tbtwo(id,name,password) values(?,'a','b')");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement.setInt(1, a);
                statement.addBatch();
            } else {
                statement2.setInt(1, a);
                statement2.addBatch();
            }
            if (a % 200000 == 0) {
                statement.executeBatch();
                statement2.executeBatch();
            }
        }
        new ExecuteThread(statement, con).start();
        new ExecuteThread(statement2, con2).start();
        while (true) {
            if (atomicInteger.getAndAdd(0) == 2) {
                break;
            }
        }
        atomicInteger.set(0);
        end("同数据库 多练接 事务批处理:增加");
        statement = con.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
        statement2 = con2.prepareStatement("update tbtwo SET name='aa',password='bb' where id=?");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement.setInt(1, a);
                statement.addBatch();
            } else {
                statement2.setInt(1, a);
                statement2.addBatch();
            }
            if (a % 200000 == 0) {
                statement.executeBatch();
                statement2.executeBatch();
            }
        }
        new ExecuteThread(statement, con).start();
        new ExecuteThread(statement2, con2).start();
        while (true) {
            if (atomicInteger.getAndAdd(0) == 2) {
                break;
            }
        }
        atomicInteger.set(0);
 
        end("同数据库 多练接 事务批处理:修改");
        statement = con.prepareStatement("delete FROM tbone where id=?");
        statement2 = con2.prepareStatement("delete FROM tbtwo where id=?");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement.setInt(1, a);
                statement.addBatch();
            } else {
                statement2.setInt(1, a);
                statement2.addBatch();
            }
            if (a % 200000 == 0) {
                statement.executeBatch();
                statement2.executeBatch();
            }
        }
        new ExecuteThread(statement, con).start();
        new ExecuteThread(statement2, con2).start();
        while (true) {
            if (atomicInteger.getAndAdd(0) == 2) {
                break;
            }
        }
        atomicInteger.set(0);
        end("同数据库 多练接 事务批处理:删除");
        statement.close();
        statement2.close();
        con.close();
    }
 
    /*
            不同数据库 多练接 事务批处理
         */
    public static void method2() throws SQLException {
        Connection con = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/TestOne?useServerPrepStmts=true&cachePrepStmts=true&rewriteBatchedStatements=true", "root", "14159265jkl");
        Connection con2 = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/TestTwo?useServerPrepStmts=true&cachePrepStmts=true&rewriteBatchedStatements=true", "root", "14159265jkl");
        con.setAutoCommit(false);
        con2.setAutoCommit(false);
        PreparedStatement statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
        PreparedStatement statement2 = con2.prepareStatement("insert into tbtwo(id,name,password) values(?,'a','b')");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement.setInt(1, a);
                statement.addBatch();
            } else {
                statement2.setInt(1, a);
                statement2.addBatch();
            }
            if (a % 200000 == 0) {
                statement.executeBatch();
                statement2.executeBatch();
            }
        }
        new ExecuteThread(statement, con).start();
        new ExecuteThread(statement2, con2).start();
        while (true) {
            if (atomicInteger.getAndAdd(0) == 2) {
                break;
            }
        }
        atomicInteger.set(0);
        end("不同数据库 多练接 事务批处理:增加");
        statement = con.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
        statement2 = con2.prepareStatement("update tbtwo SET name='aa',password='bb' where id=?");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement.setInt(1, a);
                statement.addBatch();
            } else {
                statement2.setInt(1, a);
                statement2.addBatch();
            }
            if (a % 200000 == 0) {
                statement.executeBatch();
                statement2.executeBatch();
            }
        }
        new ExecuteThread(statement, con).start();
        new ExecuteThread(statement2, con2).start();
        while (true) {
            if (atomicInteger.getAndAdd(0) == 2) {
                break;
            }
        }
        atomicInteger.set(0);
 
        end("不同数据库 多练接 事务批处理:修改");
        statement = con.prepareStatement("delete FROM tbone where id=?");
        statement2 = con2.prepareStatement("delete FROM tbtwo where id=?");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement.setInt(1, a);
                statement.addBatch();
            } else {
                statement2.setInt(1, a);
                statement2.addBatch();
            }
            if (a % 200000 == 0) {
                statement.executeBatch();
                statement2.executeBatch();
            }
        }
        new ExecuteThread(statement, con).start();
        new ExecuteThread(statement2, con2).start();
        while (true) {
            if (atomicInteger.getAndAdd(0) == 2) {
                break;
            }
        }
        atomicInteger.set(0);
        end("不同数据库 多练接 事务批处理:删除");
        statement.close();
        statement2.close();
        con.close();
    }
 
    /*
     * 同数据库 单练接 事务批处理
	 */
    public static void method3() throws SQLException {
        Connection con = DriverManager.getConnection(
                "jdbc:mysql://127.0.0.1:3306/TestOther?useServerPrepStmts=true&cachePrepStmts=true&rewriteBatchedStatements=true",
                "root", "14159265jkl");
        con.setAutoCommit(false);
        PreparedStatement statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
        PreparedStatement statement2 = con.prepareStatement("insert into tbtwo(id,name,password) values(?,'a','b')");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement.setInt(1, a);
                statement.addBatch();
            } else {
                statement2.setInt(1, a);
                statement2.addBatch();
            }
            if (a % 200000 == 0) {
                statement.executeBatch();
                statement2.executeBatch();
            }
        }
        new ExecuteThread(statement, con).start();
        new ExecuteThread(statement2, con).start();
        while (true) {
            if (atomicInteger.getAndAdd(0) == 2) {
                break;
            }
        }
        atomicInteger.set(0);
        end("同数据库 单练接 事务批处理:增加");
        statement = con.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
        statement2 = con.prepareStatement("update tbtwo SET name='aa',password='bb' where id=?");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement.setInt(1, a);
                statement.addBatch();
            } else {
                statement2.setInt(1, a);
                statement2.addBatch();
            }
            if (a % 200000 == 0) {
                statement.executeBatch();
                statement2.executeBatch();
            }
        }
        new ExecuteThread(statement, con).start();
        new ExecuteThread(statement2, con).start();
        while (true) {
            if (atomicInteger.getAndAdd(0) == 2) {
                break;
            }
        }
        atomicInteger.set(0);
 
        end("同数据库 单练接 事务批处理:修改");
        statement = con.prepareStatement("delete FROM tbone where id=?");
        statement2 = con.prepareStatement("delete FROM tbtwo where id=?");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement.setInt(1, a);
                statement.addBatch();
            } else {
                statement2.setInt(1, a);
                statement2.addBatch();
            }
            if (a % 200000 == 0) {
                statement.executeBatch();
                statement2.executeBatch();
            }
        }
        new ExecuteThread(statement, con).start();
        new ExecuteThread(statement2, con).start();
        while (true) {
            if (atomicInteger.getAndAdd(0) == 2) {
                break;
            }
        }
        atomicInteger.set(0);
        end("同数据库 单练接 事务批处理:修改");
        statement.close();
        statement2.close();
        con.close();
    }
 
    /*
        不同数据库 单链接 事务批处理
     */
    //不存在
 
 
    /*
        不同数据库，多链接，非批处理
    */
    static class ExecuteThread2 extends Thread {
        public PreparedStatement statement;
 
        public ExecuteThread2(PreparedStatement statement) {
            this.statement = statement;
        }
 
        @Override
        public void run() {
            try {
 
                this.statement.execute();
            } catch (SQLException e) {
                System.out.println(this.statement);
                e.printStackTrace();
            }
            atomicInteger.addAndGet(1);
        }
    }
 
    public static void method4() throws SQLException {
        Connection con = DriverManager.getConnection(
                "jdbc:mysql://127.0.0.1:3306/TestOne",
                "root", "14159265jkl");
        Connection con2 = DriverManager.getConnection(
                "jdbc:mysql://127.0.0.1:3306/TestTwo",
                "root", "14159265jkl");
        PreparedStatement statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
        PreparedStatement statement2 = con2.prepareStatement("insert into tbtwo(id,name,password) values(?,'a','b')");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
                statement.setInt(1, a);
                new ExecuteThread2(statement).start();
            } else {
                statement2 = con2.prepareStatement("insert into tbtwo(id,name,password) values(?,'a','b')");
                statement2.setInt(1, a);
                new ExecuteThread2(statement2).start();
            }
        }
        while (true) {
            if (atomicInteger.getAndAdd(0) == times) {
                break;
            }
        }
        atomicInteger.set(0);
        end(" 不同数据库，多链接，非批处理:增加");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement = con.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
                statement.setInt(1, a);
                new ExecuteThread2(statement).start();
            } else {
                statement2 = con2.prepareStatement("update tbtwo SET name='aa',password='bb' where id=?");
                statement2.setInt(1, a);
                new ExecuteThread2(statement2).start();
            }
        }
        while (true) {
            if (atomicInteger.getAndAdd(0) == times) {
                break;
            }
        }
        atomicInteger.set(0);
 
        end(" 不同数据库，多链接，非批处理:修改");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement = con.prepareStatement("delete FROM tbone where id=?");
                statement.setInt(1, a);
                new ExecuteThread2(statement).start();
            } else {
                statement2 = con2.prepareStatement("delete FROM tbtwo where id=?");
                statement2.setInt(1, a);
                new ExecuteThread2(statement2).start();
            }
        }
        while (true) {
            if (atomicInteger.getAndAdd(0) == times) {
                break;
            }
        }
        atomicInteger.set(0);
        end(" 不同数据库，多链接，非批处理:删除");
        statement.close();
        statement2.close();
        con.close();
    }
 
    /*
    *   同数据库 单链接 非批处理
    * */
    public static void method5() throws SQLException {
        Connection con = DriverManager.getConnection(
                "jdbc:mysql://127.0.0.1:3306/TestOne",
                "root", "14159265jkl");
        PreparedStatement statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
        PreparedStatement statement2 = con.prepareStatement("insert into tbtwo(id,name,password) values(?,'a','b')");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
                statement.setInt(1, a);
                new ExecuteThread2(statement).start();
            } else {
                statement2 = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
                statement2.setInt(1, a);
                new ExecuteThread2(statement2).start();
            }
        }
        while (true) {
            if (atomicInteger.getAndAdd(0) == times) {
                break;
            }
        }
        atomicInteger.set(0);
        end(" 同数据库 单链接 非批处理:增加");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement = con.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
                statement.setInt(1, a);
                new ExecuteThread2(statement).start();
            } else {
                statement2 = con.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
                statement2.setInt(1, a);
                new ExecuteThread2(statement2).start();
            }
        }
        while (true) {
            if (atomicInteger.getAndAdd(0) == times) {
                break;
            }
        }
        atomicInteger.set(0);
 
        end(" 同数据库 单链接 非批处理:修改");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement = con.prepareStatement("delete FROM tbone where id=?");
                statement.setInt(1, a);
                new ExecuteThread2(statement).start();
            } else {
                statement2 = con.prepareStatement("delete FROM tbone where id=?");
                statement2.setInt(1, a);
                new ExecuteThread2(statement2).start();
            }
        }
        while (true) {
            if (atomicInteger.getAndAdd(0) == times) {
                break;
            }
        }
        atomicInteger.set(0);
        end(" 同数据库 单链接 非批处理:删除");
        statement.close();
        statement2.close();
        con.close();
    }
 
    /*
    *   同数据库 多链接 非批处理
    * */
    public static void method6() throws SQLException {
        Connection con = DriverManager.getConnection(
                "jdbc:mysql://127.0.0.1:3306/TestOther",
                "root", "14159265jkl");
        Connection con2 = DriverManager.getConnection(
                "jdbc:mysql://127.0.0.1:3306/TestOther",
                "root", "14159265jkl");
        PreparedStatement statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
        PreparedStatement statement2 = con2.prepareStatement("insert into tbtwo(id,name,password) values(?,'a','b')");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement = con.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
                statement.setInt(1, a);
                new ExecuteThread2(statement).start();
            } else {
                statement2 = con2.prepareStatement("insert into tbone(id,name,password) values(?,'a','b')");
                statement2.setInt(1, a);
                new ExecuteThread2(statement2).start();
            }
        }
        while (true) {
            if (atomicInteger.getAndAdd(0) == times) {
                break;
            }
        }
        atomicInteger.set(0);
        end("  同数据库 多链接 非批处理:增加");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement = con.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
                statement.setInt(1, a);
                new ExecuteThread2(statement).start();
            } else {
                statement2 = con2.prepareStatement("update tbone SET name='aa',password='bb' where id=?");
                statement2.setInt(1, a);
                new ExecuteThread2(statement2).start();
            }
        }
        while (true) {
            if (atomicInteger.getAndAdd(0) == times) {
                break;
            }
        }
        atomicInteger.set(0);
 
        end("  同数据库 多链接 非批处理:修改");
        start();
        for (int a = 0; a < times; a++) {
            if (a % 2 == 0) {
                statement = con.prepareStatement("delete FROM tbone where id=?");
                statement.setInt(1, a);
                new ExecuteThread2(statement).start();
            } else {
                statement2 = con2.prepareStatement("delete FROM tbone where id=?");
                statement2.setInt(1, a);
                new ExecuteThread2(statement2).start();
            }
        }
        while (true) {
            if (atomicInteger.getAndAdd(0) == times) {
                break;
            }
        }
        atomicInteger.set(0);
        end("  同数据库 多链接 非批处理:删除");
        statement.close();
        statement2.close();
        con.close();
    }
}
```

### 测试样例和结果

组号|是否是同一个数据库|是否使用多个链接|是否使用批处理方法|1w（毫秒）|100w（毫秒）
---|---|---|---|---|---
第一组|Y|N|N|添加 :42306，修改 :43521，删除 :44073|大于一小时
第二组|N|Y|N|添加 : 34137，修改 : 34215，删除 : 33698|大于一小时
第三组|Y|Y|N|添加 : 34511，修改 : 34060，删除 : 33970|大于一小时
第四组|Y|N|Y|添加 : 81，修改 : 724，删除 : 454|添加 : 9504，修改 : 78451，删除 : 46229
第五组|N|Y|Y|添加 : 70，修改 : 424，删除 : 276|添加 : 8953，修改 : 69865，删除 : 40738
第六组|Y|Y|Y|添加 :200，修改 : 595，删除 : 289|添加 : 6119，修改 : 78899，删除 : 47316

### 总结（结合专题二和专题三）

单库多链接在大数据量（100w）下性能优势明显，但是多库分表在新能区间上更优，分表相比教不分表性能更好