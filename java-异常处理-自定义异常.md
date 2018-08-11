
> 学习java感觉，java的异常处理机制异常的强大，为程序的编写和调试提供的方便快捷的错误提示功能，可以节省大量的时间。系统内置的异常就不记录了，这里记录一下怎样自定义异常

## 一.创建异常类

> 继承Exception类 
> 并且是想相关的有参构造函数

```java
//首先自定以异常类  必须带一个带有String参数类型的构造参数
class ChushulingException extends Exception {
/**
* 
*/
private static final long serialVersionUID = 1L;
//自定义异常函数必须要有一个带string类型的构造函数
public ChushulingException(String msg) {
		super(msg);
	}
}
```
## 二.使用自定义的异常类

```java
class Numbertest {//在定义的方法中显示的抛出异常类
	public int shang(int x, int y) throws ChushulingException, ChushufuException {
		if (y < 0) {
			throw new ChushufuException("您输入的是" + y + ",规定除数不能为负数!");// 抛出异常
		}
		if (y == 0) {
			throw new ChushulingException("您输入的是" + y + ",除数不能为0!");
		}
		int m = x / y;
		return m;
	}
}
```
使用throw 抛出自定义的异常

## 三.在其他类中进行监听抛出的异常

```java
class Rt001 {
	public void oo() {
		Numbertest n = new Numbertest();
		// 使用try - catch 语句    finally
		try {
			System.out.println("商=" + n.shang(1, -3));
		} catch (ChushulingException yc) {
			System.out.println(yc.getMessage());
			yc.printStackTrace();
		} catch (ChushufuException yx) {//出现错误的时候执行的语句
			System.out.println(yx.getMessage());
			yx.printStackTrace();
		} catch (Exception y) {
			System.out.println(y.getMessage());
			y.printStackTrace();
		}
		finally {
			System.out.println("finally!");
		} //// finally不管发没发生异常都会被执行
	}
}
```
异常类中的.printStackTrace();将会打印出异常堆栈 .getMessage();将会打印出异常描述也就是自己定义的类中传入的字符串
## 四.总结
#### 1.自定义异常
```java
class 异常类名 extends Exception { 
	public 异常类名(String msg){ 
	super(msg);
	} 
}
```
#### 2.标识可能抛出的异常（用在方法上面）
```java
throws 异常类名1,异常类名2;
```
#### 3.捕获异常
```java
try{
	.....
} catch(异常类名 y){
	......
}finally{
	
}
```
#### 4.异常的解释
> 调用异常类的相关方法
```java
getMessage()
//输出异常的信息 printStackTrace()
//输出导致异常更为详细的信息 
```

## 五.引申
> java7 之后try-catch 语句将会自动的关闭相关的资源,**前提是相关类必须实现AutoCloseable或者Closeable接口和实现其中的close()方法**
本质上是一种观察者模式

```java
class Auto implements AutoCloseable{
	@Override
	public void close() throws Exception {
		// TODO Auto-generated method stub
			
	}
		
}
	
//之后 当使用try-catch-finally 将会自动的添加 关闭资源的方法
public void hehe() {
	try {
		Auto ceshi = new Auto();
		
	}catch (Exception e) {
		// TODO: handle exception
	}
}
//之后将会自动的调用ceshi的close方法
```

