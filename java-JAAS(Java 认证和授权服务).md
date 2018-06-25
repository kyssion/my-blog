> 之前写过一篇有关java内部安全机制和沙箱的一片文章,那一篇中jvm是基于代码的维度进行权限管理的,但是java在java1.4内置一个JAAS基于用户的权限管理(虽然个人觉得这个东西非常鸡肋,适合单体应用并不适合现在的微服务和分布式框架,因为有个非常坑爹的配置文件-我权限管理都是使用数据库实现的:disappointed_relieved:)

### JAAS的大体组成

1. 客户端通过一个LoginContext对象与JAAS相互作用，这个LoginContext对象提供了一种开发应用程序的方式，它不依赖于底层的认证技术。
2. LoginContext：是javax.security.auth.login包里的一个类，它描述了用于验证对象(subjects)的方法。
3. Subject：就是在某个你想去认证和分配访问权限的系统里的一个标识。一个主体(subject)可能是一个用户、一个进程或者是一台机器，它用javax.security.auth.Subject类表示。
4. java.security.Principal： 由于一个Subject可能涉及多个授权（一个网上银行密码和另一个电子邮件系统），java.security.Principal就被用作在那些关联里的标识。也就是说，该Principal接口是一个能够被用作代表某个实体、公司或者登陆ID的抽象概念。一个Subject可能包含多个Principles. 稍后将有一个示例类实现了这个Principal接口。
5. LoginContext对象调用负责实现和执行认证的LoginModules。LoginModule接口(在javax.security.auth.spi 包里)必须让认证技术的提供者去实现，并且能够被应用程序指定提供一个特定认证类型。
 - LoginContext： 用来读取Configuaration和实例化特定的LoginModules.
 - Configuaration： 被某个特定的应用程序用作指定认证技术或者LoginModule。因此，不同的LoginModules能够被应用到某个应用程序而不用对这个应用程序做任何的代码修改。
6. CallbackHandler 安全机制的回调器处理器,用来处理和显示回调的信息
### 一个例子

> 主类:关键的一句第八行-在配置文件example.conf里，实体名"WeatherLogin"就是被MyClient.java用作关联这个实体的名字。这里同时还将一个回调处理程序传给了底层的LoginModule，因此他们能够通过提示用户名/密码同用户进行交流和作用，例如：通过文本或者图形用户接口。一旦LoginContext已经被实例化了，login方法就被调用去登陆.

```java
// LoginContext：是javax.security.auth.login包里的一个类，它描述了用于验证对象(subjects)的方法。  
// LoginContext对象调用负责实现和执行认证的LoginModules。  
public class MyClient {
	public static void main(String[] args) {
		LoginContext context = null;
		try {
			// 在配置文件example.conf里，实体名"WeatherLogin"就是被MyClient.java用作关联这个实体的名字。
			context = new LoginContext("WeatherLogin", new MyCallbackHandler());
		} catch (LoginException le) {
			System.err.println("LoginContext cannot be created. " + le.getMessage());
			System.exit(-1);
		} catch (SecurityException se) {
			System.err.println("LoginContext cannot be created. " + se.getMessage());
		}
		try {
			context.login();//使用反射调用出自己定义的实现LoginModules的类
		} catch (LoginException le) {
			System.out.println("Authentication failed. " + le.getMessage());
			System.exit(-1);
		}
		System.out.println("authentication succeeded.");
		System.exit(-1);
	}
}
```

> 回调类:底层安全服务可能要求通过传递单个的callbacks到回调处理程序。基于传递的callbacks，回调处理程序决定怎样去获取和显示信息。

```java
// 一个基于JAAS的应用程序实现了CallbackHandler接口，  
// 因此它能够提示用户去输入特定的认证信息，比如用户名或者密码，或者显示错误或者警告信息。  
// 基于传递的callbacks，回调处理程序决定怎样去获取和显示信息。  
public class MyCallbackHandler implements CallbackHandler {
	@Override
	public void handle(Callback[] callbacks) throws IOException, UnsupportedCallbackException {
		for (int i = 0; i < callbacks.length; i++) {
			if (callbacks[i] instanceof NameCallback) {
				NameCallback nc = (NameCallback) callbacks[0];
				System.err.println(nc.getPrompt());
				System.err.flush();
				String name = (new BufferedReader(new InputStreamReader(System.in))).readLine();
				nc.setName(name);
			} else {
				throw new UnsupportedCallbackException(callbacks[i], "callback handler not support");
			}
		}
	}
}
```

>Module类:真实的控制操作类

```java
// 以下代码展示了一个LoginModule简单的实现. 这个例子是非常简单的，  
// 因为他仅仅有一个认证字符串和一个Principal（特征） "SunnyDay", 两个都是硬编码。  
// 如果去login，系统将显示"What is the weather like today?", 如果答案是"Sunny", 用户就能通过。  
public class WeatherLoginModule implements LoginModule {
	private Subject subject;
	private ExamplePrincipal entity;
	private CallbackHandler callbackhandler;
	private static final int NOT = 0;
	private static final int OK = 1;
	private static final int COMMIT = 2;
	private int status;
	// initialize: 这个方法的目的就是用有关的信息去实例化这个LoginModule。
	// 如果login成功，在这个方法里的Subject就被用在存储Principals和Credentials.
	// 注意这个方法有一个能被用作输入认证信息的CallbackHandler。在这个例子里，我没有用CallbackHandler.
	// CallbackHandler是有用的，因为它从被用作特定输入设备里分离了服务提供者。
	public void initialize(Subject subject, CallbackHandler callbackhandler, Map state, Map options) {
		status = NOT;
		entity = null;
		this.subject = subject;
		this.callbackhandler = callbackhandler;
	}
	// login: 请求LoginModule去认证Subject. 注意此时Principal还没有被指定。
	public boolean login() throws LoginException {
		if (callbackhandler == null) {
			throw new LoginException("No callback handler is available");
		}
		Callback callbacks[] = new Callback[1];
		callbacks[0] = new NameCallback("What is the weather like today?");
		String name = null;
		try {
			// 调用 MyCallbackHandler.java 中的 handle 方法进行处理
			// 以读入用户输入的认证信息（如 username）
			callbackhandler.handle(callbacks);
			name = ((NameCallback) callbacks[0]).getName();
		} catch (java.io.IOException ioe) {
			throw new LoginException(ioe.toString());
		} catch (UnsupportedCallbackException ce) {
			throw new LoginException("Error: " + ce.getCallback().toString());
		}
		if (name.equals("Sunny")) {
			entity = new ExamplePrincipal("SunnyDay");
			status = OK;
			return true;
		} else {
			return false;
		}
	}
	// commit: 如果LoginContext的认证全部成功就调用这个方法。
	public boolean commit() throws LoginException {
		if (status == NOT) {
			return false;
		}
		if (subject == null) {
			return false;
		}
		Set entities = subject.getPrincipals();
		if (!entities.contains(entity)) {
			entities.add(entity);
		}
		status = COMMIT;
		return true;
	}
	// abort: 通知其他LoginModule供应者或LoginModule模型认证已经失败了。整个login将失败。
	public boolean abort() throws LoginException {
		if ((subject != null) && (entity != null)) {
			Set entities = subject.getPrincipals();
			if (entities.contains(entity)) {
				entities.remove(entity);
			}
		}
		subject = null;
		entity = null;
		status = NOT;
		return true;
	}
	// logout: 通过从Subject里移除Principals和Credentials注销Subject。
	public boolean logout() throws LoginException {
		subject.getPrincipals().remove(entity);
		status = NOT;
		subject = null;
		return true;
	}
}
```

> Principal : Principal接口的一个实现。

```java
// ExamplePrincipal 展示了Principal（主体特征）接口的一个实现。   
public class ExamplePrincipal implements Principal {
	private final String name;
	public ExamplePrincipal(String name) {
		if (name == null) {
			throw new IllegalArgumentException("Null name");
		}
		this.name = name;
	}
	public String getName() {
		return name;
	}
	public String toString() {
		return "ExamplePrinciapl: " + name;
	}
	public boolean equals(Object obj) {
		if (obj == null)
			return false;
		if (obj == this)
			return true;
		if (!(obj instanceof ExamplePrincipal))
			return false;
		ExamplePrincipal another = (ExamplePrincipal) obj;
		return name.equals(another.getName());
	}
	public int hasCode() {
		return name.hashCode();
	}
}
```

### 配置文件设置

> LoginContext通过读取Configuration去决定那个LoginModule将被使用。

```java
WeatherLogin
{
    com.kys.WeatherLoginModule required;
};
```

使用下面的命令（指定了login配置文件）运行客户端.

```java
prompt> java -Djava.security.auth.login.config=example.conf MyClient
```

> 引申:如果开启了安全模式java -Djava.security.manager,需要指定安全策略的

```java
grant codebase "file:./*"
{
  permission javax.security.auth.AuthPermission "createLoginContext";
  permission javax.security.auth.AuthPermission "modifyPrincipals";
};
```
运行如下的命令运行
```shell
java -Djava.security.manager -Djava.security.policy==policy.txt -Djava.security.auth.login.config==example.conf MyClient
```

>结束语: 看看就好了,知道是个啥就行了,基本上用不上

