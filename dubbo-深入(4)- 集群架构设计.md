## 深入dubbo（四）- 集群架构设计

这次跟踪源代码，看一看dubbo在进行远程调用的时候进行了那些方法

1. 首先调用我们声明的接口方法  

```java
String hello = demoService.sayHello("world"); // 执行远程方法
```

2. 很明显进入了动态代理类中 注意返回值

```java
public class InvokerInvocationHandler implements InvocationHandler {
    private final Invoker<?> invoker;
    public InvokerInvocationHandler(Invoker<?> handler) {
        this.invoker = handler;
    }
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        String methodName = method.getName();
        Class<?>[] parameterTypes = method.getParameterTypes();
        if (method.getDeclaringClass() == Object.class) {
            return method.invoke(invoker, args);
        }
        if ("toString".equals(methodName) && parameterTypes.length == 0) {
            return invoker.toString();
        }
        if ("hashCode".equals(methodName) && parameterTypes.length == 0) {
            return invoker.hashCode();
        }
        if ("equals".equals(methodName) && parameterTypes.length == 1) {
            return invoker.equals(args[0]);
        }
        return invoker.invoke(new RpcInvocation(method, args)).recreate();
    }
}
```

3. 上一步的return方法中我们需要进一步分析invoke（xxx）方法的过程

![](blogimg/dubbo/1.png)

4. 来到了第一个关键的类中 AbstractClusterInvoker 通过 下图中的两个方法我们找到了 下一个关键directory

![](blogimg/dubbo/2.png)

![](blogimg/dubbo/3.png)

5. 来到了directory类中 list方法是返回一个所需要的invoke结果集合 中间使用directory 返回所有集合和使用router对结果集进行筛选

![](blogimg/dubbo/4.png)

![](blogimg/dubbo/5.png)
