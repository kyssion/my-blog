> 基于dubbo2.7 + 

上一篇分析了dubbo有关自动化扩展的相关信息，这一片正式进入主题，研究一下dubbo服务初始化的过程

# 初始化代码的展示

```java
public class ApplicationProvider {
    public static void main(String[] args) throws Exception {
        ServiceConfig<DemoServiceImpl> service = new ServiceConfig<>();
        service.setInterface(DemoService.class);
        service.setRef(new DemoServiceImpl());
        DubboBootstrap bootstrap = DubboBootstrap.getInstance();
        bootstrap
                .application(new ApplicationConfig("dubbo-demo-api-provider"))
                .registry(new RegistryConfig("zookeeper://127.0.0.1:2181"))
                .service(service)
                .start()
                .await();
    }
}
```

> 注意这里的两块 ， 一个是setInterface初始化的是实现的接口，并且初始化ServiceConfig内部的ID值为这个接口的名称，另一个石Ref方法，对应这个接口的实现类

然后重点就是这个DubboBootstrap类了