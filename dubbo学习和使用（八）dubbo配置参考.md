
### dubbo:service(<dubbo:service>)

这个配置是针对服务端的，用来暴露服务端可以对外提供的服务信息

>对应的配置类com.alibaba.dubbo.config.ServiceConfig

属性|对应URL|类型|是否必填|缺省值|作用|描述|兼容性|
---|---|---|---|---|---|---|---|
interface|-|class|必填|-|服务发现|服务接口名|1.0.0以上版本|
ref|-|object|必填|-|服务发现|服务对象实现引用|1.0.0以上版本|
version|version|string|可选|0.0.0|服务发现|服务版本，建议使用两位数字版本，如：1.0，通常在接口不兼容是版本号才需要升级|1.0.0以上版本|
group|group|string|可选|-|服务发现|服务分组，当一个借口有多个实现，可以用分组区分|1.0.7以上版本|
path||string|可选|缺省为接口|服务发现|服务路径|1.0.12以上版本|
delay|delay|int|可选|0|性能调优|延迟注册服务时间(毫秒)，设为-1时，表示延迟到Spring容器初始化完成时暴露服务|1.0.14以上版本|
timeout|timeout|int|可选|1000|性能调优|远程服务调用超时时间(毫秒)|2.0.0以上版本|
retries|retries|int|可选|2|性能调优|远程服务调用重试次数，不包括第一次调用，0为不需要重试|2.0.0以上版本|
connections|connections|boolean|可选|100|性能调优|对每个提供者的最大连接数，rmi、http、hesslan等多连接协议表示限制连接数，dubbo等长链接协议表示建立的长连接个数|2.0.0以上版本|
loadbalance|loadbalance|string|可选|random|性能调优|负载均衡策略，可选值：random，roundrobin，leastactice，分别表示：随机，轮询，最少活跃调用|2.0.0以上版本|
async|async|boolean|可选|FALSE|性能调优|是否缺省异步执行，不可靠异步，只是忽略返回值，不阻塞执行线程|2.0.0以上版本|
stub|stub|class/boolean|可选|FALSE|服务治理|设为ture，表示使用缺省代理类名，即：接口名+Local后缀，服务接口客户端本地代理类名，用于在客户端执行本地逻辑，如本地缓存等。该本地代理类的构造函数必须允许传入远程代理对象，构造函数如：publicxxxServiceLocal(XxxServicexxxService)|2.0.0以上版本|
mock|mock|class/boolean|可选|FALSE|服务治理|设为true，表示使用缺省Mock类名，即：接口名+Mock后缀，服务接口调用失败Mock实现类，该Mock类必须有一个无参构造函数，与Local的区别在于，Local总是被执行，而Mock只在出现非业务异常(比如超时，网络异常等)时执行，Local在远程调用之前执行，Mock在远程调用后执行|2.0.0以上版本|
token|token|string/bollean|可选|FALSE|服务治理|令牌验证，为空表示不开启。如果为true，表示随机生成动态令牌，否则使用静态令牌。令牌的作用是防止消费者绕过注册中心直接访问，保证注册中心的授权功能有效。如果使用点对点调用，需要关闭令牌功能|2.0.0以上版本|
registry|-|string|可选|缺省向所有registry注册|配置关联|向指定注册中心注册<dubbo:registry>的属性为id的value；在向多个注册中心注册时，多个id使用逗号分隔；如果不想讲该服务注册到任何registry，可将值设置N/A|2.0.0以上版本|
provider|-|string|可选|缺省使用第一个provider配置|配置关联|指定provider，值为<dubbo:provider>的id属性|2.0.0以上版本|
deprecated|deprecated|boolean|可选|FALSE|服务治理|服务是否过时，如果设置为true，消费方引用时将打印服务过时警告error日志|2.0.5以上版本|
dynamic|dynamic|boolean|可选|TRUE|服务治理|服务是否动态注册，如果设为false，注册后将显示disable状态，需要人工启用；并且服务提供者停止时，也不会自动取消注册，需要人工禁用|2.0.5以上版本|
accesslog|accesslog|string/boolean|可选|FALSE|服务治理|设为true，将向logger中输入访问日志，也可以填写访问日志文件路径，直接把访问日志输出到指定文件|2.0.5以上版本|
owner|owner|string|可选|-|服务治理|服务责任人，用于服务治理，请填写公司负责人邮箱前缀|2.0.5以上版本|
document|document|string|可选|-|服务治理|服务文档URL|1.0.5以上版本|
weight|weight|int|可选|-|服务调优|服务权重|2.0.5以上版本|
executes|executes|int|可选|0|性能调优|服务提供者每个服务方法最大可并行请求数||
actives|actives|int|可选|0|性能调优|服务消费者每个服务方法最大并发调用数||
proxy|proxy|string|可选|javassist|性能调优|省城动态代理方法，可选：jdk/javassist|2.0.5以上版本|
cluster|cluster|stirng|可选|failover|性能调优|集群方式，可选:failover/failfast/failsafe/failback/forking|2.0.5以上版本|
filter|service.filter|string|可选|default|性能调优|服务提供方远程调用过程拦截器名称，多个名称用逗号分隔|2.0.5以上版本|
listener|exporter.listener|string|可选|default|性能调优|服务提供方导出服务监听器名称，多个名称用逗号分隔|2.0.5以上版本|
protocol|-|string|可选|-|配置关联|使用指定的协议暴露服务，在使用多协议时，<dubbo:protocol>的id属性的value,使用逗号分隔|2.0.5以上版本|
layer|layer|string|可选|-|服务治理|服务提供者所在的分层。如：biz,dao,intl:web,china:acton|2.0.7以上版本|
register|register|boolean|可选|TRUE|服务治理|该协议的服务是否注册到注册中心|2.0.8以上版本|

注意：头四个是最重要的属性dubbo通过这些属性来唯一的标示一个service

### dubbo:reference

这个配置是针对消费者端的，消费中通过这个类发起请求向服务端进行调用

>对应的配置类com.alibaba.dubbo.config.ReferenceConfig

属性|对应URL|类型|是否必填|缺省值|作用|描述|兼容性|
---|---|---|---|---|---|---|---|
id|-|string|必填|-|配置关联|服务应用beanid|1.0.0以上版本|
interface|-|class|必填|-|服务发现|服务接口名|1.0.0以上版本|
version|version|string|可选|-|服务发现|服务版本，与服务提供者的版本保持一致|1.0.0以上版本|
group|group|string|可选|-|服务发现|服务分组，当一个借口有多个实现，可以用分组区分，必须和服务提供方一致|1.0.7版本|
timeout|timeout|long|可选|缺省使用<dubbo:consumer>的timeout|性能调优|服务方法调用超时时间(毫秒)|1.0.5以上版本|
retries|retries|int|可选|缺省使用<dubbo:consumer>的retries|性能调优|远程服务调用重试次数，不包括第一次调用，不需要重试请设置为0|2.0.0以上版本|
connections|connections|int|可选|缺省使用的connections|性能调优|对每个提供者的最大连接数，rmi、http、hessian等短连接协议表示限制连接数，dubbo等长连接协表示建立的长连接个数|2.0.0以上版本|
loadbalance|loadbalance|string|可选|缺省使用的loadbalance|性能调优|负载均衡策略，可选值：random,roundrobin,leastactive，分别表示：随机，轮循，最少活跃调用|2.0.0以上版本|
sync|sync|boolean|可选|缺省使用的async|性能调优|是否异步执行，不可靠异步，只是忽略返回值，不阻塞执行线程|2.0.0以上版本|
generic|generic|boolean|可选|缺省使用的generic|服务治理|是否缺省泛化接口，如果为泛化接口，将返回GenericService|2.0.0以上版本|
check|check|boolean|可选|缺省使用的check|服务治理|启动时检查提供者是否存在，true报错，false忽略|2.0.0以上版本|
url|<url>|string|可选|-|服务治理|点对点直连服务提供者地址，将绕过注册中心|1.0.6以上版本|
stub|stub|class/boolean|可选|-|服务治理|服务接口客户端本地代理类名，用于在客户端执行本地逻辑，如本地缓存等，该本地代理类的构造函数必须允许传入远程代理对象，构造函数如：publicXxxServiceLocal(XxxServicexxxService)|2.0.0以上版本|
mock|mock|class/boolean|可选|-|服务治理|服务接口调用失败Mock实现类名，该Mock类必须有一个无参构造函数，与Local的区别在于，Local总是被执行，而Mock只在出现非业务异常(比如超时，网络异常等)时执行，Local在远程调用之前执行，Mock在远程调用后执行|1.0.13以上版本|
cache|cache|string/boolean|可选|-|服务治理|以调用参数为key，缓存返回结果。可选：lru,threadlocal,jcache等|2.1.0以上版本|
validation|validation|boolean|可选|-|服务治理|是否启用JSR303标准注解验证，如果启用，将对方法参数上的注解进行校验|2.1.0以上版本|
proxy|proxy|boolean|可选|javassist|性能调优|选择动态代理实现策略，可选：javassist,jdk|2.0.2以上版本|
client|client|string|可选|-|性能调优|客户端传输类型设置，如Dubbo协议的netty或mina|2.0.0以上版本|
registry|-|string|可选|缺省将从所有注册中心获服务列表后合并结果|配置关联|从指定注册中心注册获取服务列表，在多个注册中心时使用，值为的id属性，多个注册中心ID用逗号分隔|2.0.0以上版本|
owner|owner|string|可选|-|服务治理|调用服务负责人，用于服务治理，请填写负责人公司邮箱前缀|2.0.5以上版本|
actives|actives|int|可选|0|性能调优|服务消费者每个服务方法最大并发调用数|2.0.5以上版本|
cluster|cluster|string|可选|failover|性能优化|集群方式，可选：failover/failfast/failsafe/failback/forking|2.0.5以上版本|
filter|reference.filter|string|可选|default|性能调优|服务消费方远程调用过程拦截器名称，多个名称用逗号分隔|2.0.5以上版本|
listener|invoker.listener|string|可选|default|性能调优|服务消费方引用服务监听器名称，多个名称用逗号分隔|2.0.5以上版本|
layer|layer|string|可选|-|服务治理|服务调用者所在的分层。如：biz、dao、intl:web、china:acton|2.0.7以上版本|
init|init|boolean|可选|FALSE|性能调优|是否在afterPropertiesSet()时饥饿初始化引用，否则等到有人注入或引用该实例时再初始化|2.0.10以上版本|
protocol|protocol|string|可选|-|服务治理|只调用指定协议的服务提供方，其他协议忽略||
|<dubbo:service>|listener|exporter.listener|string|可选|default|性能调优|服务提供方导出服务监听器名称，多个名称用逗号分隔|2.0.5以上版本|
|<dubbo:service>|protocol|-|string|可选|-|配置关联|使用指定的协议暴露服务，在使用多协议时，<dubbo:protocol>的id属性的value,使用逗号分隔|2.0.5以上版本|
|<dubbo:service>|layer|layer|string|可选|-|服务治理|服务提供者所在的分层。如：biz,dao,intl:web,china:acton|2.0.7以上版本|
|<dubbo:service>|register|register|boolean|可选|TRUE|服务治理|该协议的服务是否注册到注册中心|2.0.8以上版本|

注意：头四个是最重要的属性dubbo通过这些属性来唯一的标示一个service