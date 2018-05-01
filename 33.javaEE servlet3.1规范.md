说道spring的web支持首先就可以想到了spring MVC 的技术(其他的技术还有spring的webflux 以后讨论),从这片博客开始要进行相关知识点的整理.

### spring MVC 整体的架构设计

![](/blogimg/springMVC/1.jpg)

spring 自己的webapplication支持嵌套作用域,通过这个方法可以实现spring applicationcongtext的继承特性(继承特性,子作用域可以访问夫作用域的中的属性,但是父作用域中的属性无法访问子作用域中的属性,具体的使用看HierarchicalBeanFactory)

#### web容器的初始化设置

springMVC 支持使用xml进行配置

```xml
<web-app>
    <listener>
        <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
    </listener>
    <context-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>/WEB-INF/app-context.xml</param-value>
    </context-param>
    <servlet>
        <servlet-name>app</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value></param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>app</servlet-name>
        <url-pattern>/app/*</url-pattern>
    </servlet-mapping>
</web-app>
```

从spring5.0 开始 spring官方文档提倡使用接口配置,容器在初始化的时候将会自动的加载这个接口的实现类从而进行配置
spring mvc 的自动化配置是通过 WebApplicationInitializer 接口实现的 但是系统提供了更加高级的接口 AbstractAnnotationConfigDispatcherServletInitializer 

```java
public class MyWebAppInitializer extends AbstractAnnotationConfigDispatcherServletInitializer {
    @Override
    protected Class<?>[] getRootConfigClasses() {
        return new Class<?[] { RootConfig.class };
    }
    @Override
    protected Class<?>[] getServletConfigClasses() {
        return new Class<?[] { App1Config.class };
    }
    @Override
    protected String[] getServletMappings() {
        return new String[] { "/app1/*" };
    }
}
```

```java
import org.springframework.web.WebApplicationInitializer;

public class MyWebApplicationInitializer implements WebApplicationInitializer {
    @Override
    public void onStartup(ServletContext container) {
        XmlWebApplicationContext appContext = new XmlWebApplicationContext();
        appContext.setConfigLocation("/WEB-INF/spring/dispatcher-config.xml");

        ServletRegistration.Dynamic registration = container.addServlet("dispatcher", new DispatcherServlet(appContext));
        registration.setLoadOnStartup(1);
        registration.addMapping("/");
    }
}
```

如果使用基于xml 的 spring配置则需要使用这个方法进行相关的调用

```java
public class MyWebAppInitializer extends AbstractDispatcherServletInitializer {
    @Override
    protected WebApplicationContext createRootApplicationContext() {
        return null;
    }
    @Override
    protected WebApplicationContext createServletApplicationContext() {
        XmlWebApplicationContext cxt = new XmlWebApplicationContext();
        cxt.setConfigLocation("/WEB-INF/spring/dispatcher-config.xml");
        return cxt;
    }
    @Override
    protected String[] getServletMappings() {
        return new String[] { "/" };
    }
}
```

如果要添加filter 配置 重构如下的方法

```java
public class MyWebAppInitializer extends AbstractDispatcherServletInitializer {
    // ...
    @Override
    protected Filter[] getServletFilters() {
        return new Filter[] {
            new HiddenHttpMethodFilter(), new CharacterEncodingFilter() };
    }
}
```
这个方法将会为每一个filter 添加一个默认的过滤器,并且自动的添加到对应的display中

这个方法还有一个isisAsyncSupported() 默认情况下返回true 表示spring mvc 框架中的filter 将会异步的处理请求

> 当使用idea 进行操作的时候注意要保证spring—web包要在class path目录下，不然tomcat等web 容器将不会使用spi技术将相关的各种需要的东西夹在到class中

引申： tomcat 此处实现spi技术的解析

spring的web包的META-INF的文件夹中有一个名为，javax.servlet.ServletContainerInitializer的文件，其中的内容org.springframework.web.SpringServletContainerInitializer，表示定义的ServletContainerInitializer和spring的实现接口SpringServletContainerInitializer，其中@HandlesTypes注解表示CustomServletContainerInitializer 可以处理的类，在onStartup 方法中，可以通过Set<Class<?>> c 获取得到。

见下面代码：

```java
@HandlesTypes(WebApplicationInitializer.class)
public class SpringServletContainerInitializer implements ServletContainerInitializer {
	@Override
	public void onStartup(@Nullable Set<Class<?>> webAppInitializerClasses, ServletContext servletContext)
			throws ServletException {
		List<WebApplicationInitializer> initializers = new LinkedList<>()
		if (webAppInitializerClasses != null) {
			for (Class<?> waiClass : webAppInitializerClasses) {
				if (!waiClass.isInterface() && !Modifier.isAbstract(waiClass.getModifiers()) &&
						WebApplicationInitializer.class.isAssignableFrom(waiClass)) {
					try {
						initializers.add((WebApplicationInitializer)
								ReflectionUtils.accessibleConstructor(waiClass).newInstance());
					}
					catch (Throwable ex) {
						throw new ServletException("Failed to instantiate WebApplicationInitializer class", ex);
					}
				}
			}
		}
		if (initializers.isEmpty()) {
			servletContext.log("No Spring WebApplicationInitializer types detected on classpath");
			return;
		}
		servletContext.log(initializers.size() + " Spring WebApplicationInitializers detected on classpath");
		AnnotationAwareOrderComparator.sort(initializers);
		for (WebApplicationInitializer initializer : initializers) {
			initializer.onStartup(servletContext);
		}
	}
}
```

### 最核心类 DispatcherServlet

如果要说这个类就需要看一下springmvc的流程图

![](/blogimg/1.png);

在这里之前 DispathcerServlet 将会webapplicationcontext的字符串引用放入java中 

```java
public static final String WEB_APPLICATION_CONTEXT_ATTRIBUTE = DispatcherServlet.class.getName() + ".CONTEXT";
```

一个一个看

1. HandlerMapping 

这个类解决了 url地址映射到对应的处理类中，主要有两个实现RequestMappingHandlerMapping-为@RequestMapping 注解提供支持 ，SimpleUrlHandlerMapping，实现简单的url地址映射

2. HandlerExceptionResolver 

这个是试图返回的异常处理包括相关的错误处理方法

3. HandlerIntercepter 

处理相关的接口进行拦截 

4. HandlerAdapter

使用适配器模式，将试图的映射由指定的接口处理

5. 各种resolver 提供视图解析展示的功能

LocaleResolver, LocaleContextResolver，ThemeResolver，MultipartResolver

6. FlashMapManager

处理flash的时候使用的 估计用不到了

### Interception 拦截器

在spring MVC 中声明springmvc 的方法有如下几种：
1. 实现HandlerInterceptor接口或者实现HandlerInterceptorAdapter 抽象类
2. 实现WebRequestInterceptor接口，或者实现了WebRequestInterceptor的类

#### HandlerInterceptor 接口方法

(1)boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handle)方法，这个将会在请求传入之前进行相关的处理，如果返回值是true，将会自动的进行链式调用其他按照顺序执行的定时器，否则将会终止调用controll和其他拦截器。

(2) postHandle (HttpServletRequest request, HttpServletResponse response, Object handle, ModelAndView modelAndView) 方法,这个方法将会在处理器执行完后进行处理，和preHandle的执行方法，注意这个方法将不会自动拦截@requsetBody注解ResponseEntity

注意这里：（1）和（2）的第三个参数 handle 官方的解释是@controller标记的本身或者使用HandleMethod这个类，其实这里是springmvc 自己增强的方法，



> ResponseEntity 详解： 这个类其实是对 http请求的一个封装，封装了http的报头，状态码，http code 等数据，本质上是一种通信协议

如果使用的不是string类型，那么将会是一种类似rpc协议

```java
//客户端
public void client(){
    RestTemplate restTemplate = new RestTemplate();
    ResponseEntity<String> entity = restTemplate.getForEntity("http://example.com", String.class);
    String body = entity.getBody();
    MediaType contentType = entity.getHeaders().getContentType();
    HttpStatus statusCode = entity.getStatusCode();
}

//服务端
@RequestMapping("/handle")
public ResponseEntity<String> handle() {
    URI location = ...;
    HttpHeaders responseHeaders = new HttpHeaders();
    responseHeaders.setLocation(location);
    responseHeaders.set("MyResponseHeader", "MyValue");
    return new ResponseEntity<String>("Hello World", responseHeaders,   HttpStatus.CREATED);
}
```

当使用string类型的时候就和@ResponceBody+@ResponseStatus 相同

```java
@RequestMapping("/handle")
public ResponseEntity<String> handle() {
    URI location = ...;
    return ResponseEntity.created(location).header("MyResponseHeader",  "MyValue").body("Hello World");
} 
```
(3)afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handle, Exception ex) 方法，该方法也是需要当前对应的Interceptor 的preHandle 方法的返回值为true 时才会执行。该方法将在整个请求结束之后，也就是在DispatcherServlet 渲染了对应的视图之后执行。这个方法的主要作用是用于进行资源清理工作的。

```java
public class MyHandlerInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception { return false; }
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception { }
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception { }
}
```


除了实现HandlerInterceptor可以实现拦截器之外，使用WebRequestInterceptor 同样可以实现拦截器

```java
class MyWebHandlerInterceptor implements WebRequestInterceptor {
    @Override
    public void preHandle(WebRequest request) throws Exception {}
    @Override
    public void postHandle(WebRequest request, ModelMap model) throws Exception {}
    @Override
    public void afterCompletion(WebRequest request, Exception ex) throws Exception {}
}
```
(1)preHandle(WebRequest request) 方法。注意这个方法没有返回直，一般主要用它来进行资源的准备工作，其中的webrequest参数是HttpServletRequest的加强版，可以使用setAttribute(name, value, scope)添加参数到指定的作用域中，scope参数有如下的几个值：
    1. SCOPE_REQUEST ：它的值是0 ，代表只有在request 中可以访问。
    2. SCOPE_SESSION ：它的值是1 ，如果环境允许的话它代表的是一个局部的隔离的session，否则就代表普通的session，并且在该session范围内可以访问。
    3. SCOPE_GLOBAL_SESSION ：它的值是2 ，如果环境允许的话，它代表的是一个全局共享的session，否则就代表普通的session，并且在该session 范围内可以访问。
(2)postHandle(WebRequest request, ModelMap model) 方法。该方法将在请求处理之后，也就是在Controller 方法调用之后被调用，但是会在视图返回被渲染之前被调用，request 就是传递的请求参数，model就是返回的视图
(3)afterCompletion(WebRequest request, Exception ex) 方法。该方法会在整个请求处理完成，也就是在视图返回并被渲染之后执行。所以在该方法中可以进行资源的释放操作。而WebRequest 参数就可以把我们在preHandle 中准备的资源传递到这里进行释放。Exception 参数表示的是当前请求的异常对象，如果在Controller 中抛出的异常已经被Spring 的异常处理器给处理了的话，那么这个异常对象就是是null 。

####HandlerExceptionResolver springmvc 异常处理

异常处理用于处理@controll 这种接口抛出的各种异常，主要有如下的几种  

1. SimpleMappingExceptionResolver 异常类名称和错误视图名称之间的映射。用于在浏览器应用程序中呈现错误页面。

2. DefaultHandlerExceptionResolver 解决Spring MVC引发的异常并将它们映射到HTTP状态代码。另请参阅备用ResponseEntityExceptionHandler和REST API例外。

3. ResponseStatusExceptionResolver 根据@ResponseStatus注释中的值解决注释中的异常并将其映射到HTTP状态代码。

4. ExceptionHandlerExceptionResolver 通过调用@ExceptionHandler一个@Controller或一个 @ControllerAdvice类中的方法来解决异常。请参阅@ExceptionHandler方法。

对于异常处理来说通常的解决结果有如下的几种方法

1. 使用ModelAndView 指向错误视图。

2. 返回空的modelandview 如果异常被处理

3. 如果异常没有被解决，将会使用异常调用连进行处理，如果调用到最后将会抛出到servlet中

在spring mvc 中集中进行异常处理的有三种方法

1. 使用@ResponseStatus 注释一个异常类，当spring中抛出这个异常的时候将会自动的交由这个类处理,并且可以制定http code值，比如下面的方法将会跑出403错误

```java
package com.zj.exception;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;
@ResponseStatus(value=HttpStatus.FORBIDDEN,reason="用户不匹配")
public class UserNotMatchException extends RuntimeException{}


@RequestMapping("/testResponseStatus")
public String testResponseStatus(int i){
    if(i==0)
        throw new UserNotMatchException();
    return "hello";
}

```

注意如果这个注解使用在 一个方法上的时候 ， 不论结果如何都将会放回制定的httpcode 异常

```java
@ResponseStatus(value=HttpStatus.FORBIDDEN,reason="用户名不匹配")
@RequestMapping("/testResponseStatus")
public String testResponseStatus(int i){
    if(i==0)
        throw new UserNotMatchException();
    return "hello";
}
```

2.@ControllerAdvice 和 @ExceptionHandler

这两个注解同样用于异常处理

（1）@ExceptionHandler 当一个Controller中有方法加了@ExceptionHandler之后，这个Controller其他方法中没有捕获的异常就会以参数的形式传入加了@ExceptionHandler注解的那个方法中。**注意这个方法要有一个参数，这个参数就是指定要处理的异常**

```java
/**
 * Created by liuruijie.
 * 处理异常的类，需要处理异常的Controller直接继承这个类
 */
public class BaseController {
    /**
     * 处理Controller抛出的异常
     * @param e 异常实例
     * @return Controller层的返回值
     */
    @ExceptionHandler
    @ResponseBody
    public Object expHandler(Exception e){
        if(e instanceof SystemException){
            SystemException ex= (SystemException) e;
            return WebResult.buildResult().status(ex.getCode())
                            .msg(ex.getMessage());
        }else{
            e.printStackTrace();
            return WebResult.buildResult().status(Config.FAIL)
                            .msg("系统错误");
        }
    }
}
```

（2）@ControllerAdvice  实现这个注解的类可以让这个类中 @ExceptionHandler标记的方法实现全觉异常监听

```java
@ControllerAdvice
public class GlobalExceptionHandler {
   //处理自定义的异常
   @ExceptionHandler(SystemException.class) 
   @ResponseBody
   public Object customHandler(SystemException e){
      e.printStackTrace();
      return WebResult.buildResult().status(e.getCode()).msg(e.getMessage());
   }
   //其他未处理的异常
   @ExceptionHandler(Exception.class)
   @ResponseBody
   public Object exceptionHandler(Exception e){
      e.printStackTrace();
      return WebResult.buildResult().status(Config.FAIL).msg("系统错误");
   }
}
```
最后对于springmvc 如果异常没有被处理，spring提供了默认的页面展示异常，使用如下方法配置
xml ： 制定默认错误页面
```xml
<error-page>
    <location>/error</location>
</error-page>
```
 java ： 处理url
 ```java
@RestController
public class ErrorController {
    @RequestMapping(path = "/error")
    public Map<String, Object> handle(HttpServletRequest request) {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("status", request.getAttribute("javax.servlet.error.status_code"));
        map.put("reason", request.getAttribute("javax.servlet.error.message"));
        return map;
    }
}
 ```
#### ViewResolver 提供了view 名称到view实例之间的绑定，并且完成真正视图展示之前将相关数据进行整理的功能

spring mvc 中将相关的视图变成一个网页经历的过程
1. 将SpringMVC控制器中的返回结果封装成一个ModelAndView对象。
2. 通过SpringMVC中的视图解析器，使用ViewResolver对控制器返回的ModelAndView对象进行解析，将逻辑视图转换成物理视图。
3. 调用View中的render()方法对物理视图进行渲染。

几个主要的视图的介绍

1. AbstractCachingViewResolver: 最抽象的类提供了视图缓存的功能
2. UrlBasedViewResolver: 提供了更加细粒度的url控制，支持前缀后缀等功能，但是使用这个方法必须制定相关的view解析工具，默认使用的是jsp解析工具InternalResourceView（和可以使用其他的是解析工具比如FreeMarkerView等）， 并且提供了重定向和转发的功能

```xml
<bean  
   class="org.springframework.web.servlet.view.UrlBasedViewResolver">  
   <property name="prefix" value="/WEB-INF/" />  
   <property name="suffix" value=".jsp" />  
   <property name="viewClass" value="org.springframework.web.servlet.view.InternalResourceView"/>  
</bean>  
```
3. InternalResourceViewResolver：这个方法是 UrlBasedViewResolver 的子类，支持父类的所有功能，InternalResourceViewResolver会把返回的视图名称都解析为InternalResourceView对象，内部使用重定向的方法，将controller返回的view 包装成InternalResourceView， 并且鞋带上前缀和后缀，同时再转发出去

视图解析链：
在SpringMVC中可以同时定义多个ViewResolver视图解析器，然后它们会组成一个ViewResolver链。当Controller处理器方法返回一个逻辑视图名称后，ViewResolver链将根据其中ViewResolver的优先级来进行处理。所有的ViewResolver都实现了Ordered接口，在Spring中实现了这个接口的类都是可以排序的。在ViewResolver中是通过order属性来指定顺序的，默认都是最大值。所以我们可以通过指定ViewResolver的order属性来实现ViewResolver的优先级，order属性是Integer类型，order越小，对应的ViewResolver将有越高的解析视图的权利，所以第一个进行解析的将是ViewResolver链中order值最小的那个。当一个ViewResolver在进行视图解析后返回的View对象是null的话就表示该ViewResolver不能解析该视图，这个时候如果还存在其他order值比它大的ViewResolver就会调用剩余的ViewResolver中的order值最小的那个来解析该视图，依此类推。当ViewResolver在进行视图解析后返回的是一个非空的View对象的时候，就表示该ViewResolver能够解析该视图，那么视图解析这一步就完成了，后续的ViewResolver将不会再用来解析该视图。当定义的所有ViewResolver都不能解析该视图的时候，Spring就会抛出一个异常。

### spring mvc 常用注解

spring 提供了一整套注解来简化spring相关的配置

#### @Controll 和 @RestController

Spring MVC提供了一种基于注释的编程模型，其中@Controller和@RestController组件使用注释来表示请求映射，请求输入，异常处理等。

其中的@RestController 是@ResponseBody和@Controller注解的一种集合。
```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Controller
@ResponseBody
public @interface RestController {
	@AliasFor(annotation = Controller.class)
	String value() default "";

}
```

注意：如果使用aop方法对controller 进行增强的话请使用class-based proxying代理，但是如果使用了非spring context回调接口的方法的时候，需要明确的制定相关的配置信息：<tx:annotation-driven/>, 改变为 <tx:annotation-driven proxy-target-class="true"/>.

#### @RequestMapping

```java
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Mapping
public @interface RequestMapping {
	String name() default "";
	@AliasFor("path")
	String[] value() default {};
	@AliasFor("value")//这个注解和path 标志制定的url地址，可以使用resulf请求的格式
    //spring-web/{symbolicName:[a-z-]+}-{version:\d\.\d\.\d}.{extension:\.[a-z]}
	String[] path() default {};
	RequestMethod[] method() default {};//制定请求的方法，RequestMethod.DELETE
	String[] params() default {};//表示制定的请求参数中存在的参数组合，如myParam = myValue，表示给定的参数为指定的值才会返回
    //可以使用name ！= value 表示不等于的关系
	String[] headers() default {};// 制定头部包含的相关信息和上面的params类似，Referer=http://www.ifeng.com
	String[] produces() default {};//指定返回的内容类型，仅当request请求头中的(Accept)类型中包含该指定类型才返回，表示浏览器接受的相关资源
    String[] consumes() default {};//指定处理请求的提交内容类型（Content-Type），例如application/json, text/html
}
```

requestMapping:有简化版的各种注解@GetMapping，@PostMapping，@PutMapping，@DeleteMapping，@PatchMapping，指定了相关的method方法对应的各种请求

request 请求可以接受的请求可以通过通配符或者glob参数的方法进行匹配

spring mvc 的地址匹配方法满足一定的相关原则，可以使用通配符进行匹配

|Wildcard|Description|
|-|-|
|？|匹配任何单字符| 
|*|匹配0或者任意数量的字符| 
|**|匹配0或者更多的目录|

注意：spring将会按照匹配的字符最长的那个进行匹配，比如/**/*.jsp 和/app/dir/*.jsp，在这个过程中，将会匹配后者。

注意：spring mvc 的匹配原则是按照后缀匹配的原则，比如一个url地址 /name这个地址，表示的就是/name.*，一定程度上实现了文件扩展名引用

如果使用了文件扩展名称这种东西如果想要配置请查看如下两个接口：

```java
useSuffixPatternMatching(false), see PathMatchConfigurer
favorPathExtension(false), see ContentNeogiationConfigurer
```


##### 在requestMethod中可以接收的数据

接受的函数体中可以使用的注解和参数

1. WebRequest, NativeWebRequest

WebRequest是Spring Web MVC提供的统一请求访问接口，不仅仅可以访问请求相关数据（如参数区数据、请求头数据，但访问不到Cookie区数据），还可以访问会话和上下文中的数据；NativeWebRequest继承了WebRequest，并提供访问本地Servlet API的方法。

```java
public String webRequest(WebRequest webRequest, NativeWebRequest nativeWebRequest) {
    System.out.println(webRequest.getParameter("test"));//①得到请求参数test的值  
    webRequest.setAttribute("name", "value", WebRequest.SCOPE_REQUEST);//②  
    System.out.println(webRequest.getAttribute("name", WebRequest.SCOPE_REQUEST));
    HttpServletRequest request =
            nativeWebRequest.getNativeRequest(HttpServletRequest.class);//③  
    HttpServletResponse response =
            nativeWebRequest.getNativeResponse(HttpServletResponse.class);
    return "success";
}
```

2. javax.servlet.ServletRequest, javax.servlet.ServletResponse，javax.servlet.http.HttpSession

javax 提供的具体接口注意其中的httpsession ，会话访问不是线程安全的。如果允许多个请求同时访问会话，请考虑将RequestMappingHandlerAdapter的“synchronizeOnSession”标志设置为“true”。

3. HttpMethod 

这个值中有传入的方式，比如get还是post

4. java.io.InputStream, java.io.Reader，java.io.OutputStream, java.io.Writer

请求的原始请求数据流，和原始返回数据

5. @PathVariable和@MatrixVariable

使用{}表示的url请求对应的相关参数,

@PathVariable 没什么好说的关键是@MatrixVariable ， 这个注解将会自动的匹配url 地址中 ;uuu=123;iii=333 这种参数，并且一定的程度下并不需要{jj}中指定的名称来匹配，当发生参数冲突的时候可以使用pathVar参数指定名称，目前有bug不记录了

5. @PathVariable,@MatrixVariable,@RequestParam，@RequestBody，@RequestHeader，@CookieValue，@RequestPart,@ModelAttribute,@SessionAttribute,@RequestAttribute

- @PathVariable ,spring mvc提供了一套支持reastfulapi的方法，这套方法可以使用{}+通配符的方式，将url中的数据传递到method 对应的参数中

```java
@GetMapping("/owners/{ownerId}/pets/{petId}")
public Pet findPet(@PathVariable Long ownerId, @PathVariable Long petId) {
    // ...
}
// 可以使用这个方法实现全局的请求效果
@Controller
@RequestMapping("/owners/{ownerId}")
public class OwnerController {
    @GetMapping("/pets/{petId}")
    public Pet findPet(@PathVariable Long ownerId, @PathVariable(petId) Long petId) {
        // ...
    }
}
```
注意：{}里面的值值也可以使用正则表达式进行相关的配置，格式：{varName:regex}

```java
@GetMapping("/{name:[a-z-]+}-{version:\\d\\.\\d\\.\\d}{ext:\\.[a-z]+}")
public void handle(@PathVariable String version, @PathVariable String ext) {}
```

- @MatrixVariable，这个注解将会自动的匹配url地址中;uuu=123;iii=333这种参数，并且一定的程度下并不需要{jj}中指定的名称来匹配，当发生参数冲突的时候可以使用pathVar参数指定名称，目前有bug不记录了

- @RequestParam接口将会自动的将传入到指定的地址中 如果使用这个注解标识Map<String, String> or MultiValueMap<String, String>，将会将所有的属性注入进来
A） 常用来处理简单类型的绑定，通过Request.getParameter() 获取的String可直接转换为简单类型的情况（ String--> 简单类型的转换操作由ConversionService配置的转换器来完成）；因为使用request.getParameter()方式获取参数，所以可以处理get 方式中queryString的值，也可以处理post方式中 body data的值；
B）用来处理Content-Type: 为 application/x-www-form-urlencoded编码的内容，提交方式GET、POST；
C) 该注解有两个属性： value、required； value用来指定要传入值的id名称，required用来指示参数是否必须绑定；

- @RequestBody 该注解常用来处理Content-Type: 不是application/x-www-form-urlencoded编码的内容，例如application/json, application/xml等；它是通过使用HandlerAdapter 配置的HttpMessageConverters来解析post data body，然后绑定到相应的bean上的。

使用：HttpMessageConverter接口，需要开启<mvc:annotation-driven  />。 AnnotationMethodHandlerAdapter将会初始化7个转换器，可以通过调用AnnotationMethodHandlerAdapter的getMessageConverts()方法来获取转换器的一个集合 List<HttpMessageConverter>，这7个转化器如下：

```java
ByteArrayHttpMessageConverter 
StringHttpMessageConverter 
ResourceHttpMessageConverter 
SourceHttpMessageConverter 
XmlAwareFormHttpMessageConverter 
Jaxb2RootElementHttpMessageConverter 
MappingJacksonHttpMessageConverter
```
PS:Spring默认的json协议解析由Jackson完成。 这种方式的时候默认使用的就是json解析。

问题 如何扩展

```java
@Controller  
public class PersonController {    
    @RequestMapping(value = "/person/login", method = RequestMethod.POST)  
    public @ResponseBody  
    Person login(@RequestBody Person person) {  
        return person;  
    }  
}
//注意序列化接口
public class Person implements Serializable {  
    private int id;  
    private String name;  
    private boolean status;  
    public Person() {  
        // do nothing  
    }
}
```
ps：如果使用xml 方式，需要使用注解

```java
@XmlRootElement(name = "Person")
public class Person {
    private String name;
    private int age;
    public String getName() { return name;    }
    @XmlElement
    public void setName(String name) { this.name = name;    }
    public int getAge() { return age;    }
    @XmlElement
    public void setAge(int age) { this.age = age;    }
}
```
 
注意 这里如果要使用注意spring mvc 环境的配置

使用xml 进行配置

```xml    
<context:annotation-config></context:annotation-config>
<context:component-scan base-package="com"></context:component-scan>
<mvc:annotation-driven></mvc:annotation-driven>
<mvc:default-servlet-handler/>
```

使用java 进行配置

```java
//注意要将sevlet放入 WebApplicationContext中
public class MyWebApplication implements WebApplicationInitializer {
    public void onStartup(ServletContext servletContext) throws ServletException {
        AnnotationConfigWebApplicationContext annotationConfigWebApplicationContext=
                new AnnotationConfigWebApplicationContext();
        annotationConfigWebApplicationContext.register(AppConfig.class);
        annotationConfigWebApplicationContext.setServletContext(servletContext);
        annotationConfigWebApplicationContext.refresh();
        ServletRegistration.Dynamic dynamic=servletContext.addServlet("dispatcher",new DispatcherServlet(annotationConfigWebApplicationContext));
        dynamic.setLoadOnStartup(1);
        dynamic.addMapping("/");
    }
}

//自动化配置
@Configuration
@ComponentScan
@EnableWebMvc//使用EnableWebMVC注解自动的注入的相关的属性
public class AppConfig  { }
```


- @RequestPart  和文件上传相关，难度有点大，和http协议相关的暂时不考虑


- @RequestHeader 将http协议中相关的头注入到指定的数据中
```java
@GetMapping("/demo")
public void handle(
        @RequestHeader("Accept-Encoding") String encoding,
        @RequestHeader("Keep-Alive") long keepAlive) {
    //...
}
```

- @ModelAttribute

在使用model view 场景下，有如下的一应用

- 1. 全局model配置，在获得请求/helloWorld 后，populateModel方法在helloWorld方法之前先被调用，它把请求参数（/helloWorld?abc=text）加入到一个名为attributeName的model属性中，在它执行后 helloWorld被调用，返回视图名helloWorld和model已由@ModelAttribute方法生产好了。
```java
@Controller 
public class HelloWorldController { 
    @ModelAttribute 
    public void populateModel(@RequestParam String abc, Model model) { 
         model.addAttribute("attributeName", abc); 
    } 
    @ModelAttribute("attributeName") 
    public String addAccount(@RequestParam String abc) { 
        return abc; 
    } 
    @RequestMapping(value = "/helloWorld") 
    public String helloWorld() { 
       return "helloWorld"; 
    }
 }
```
- 2. 指派model配置  返回 helloworld.do视图，有一个model 参数是attributeName和值 hi

```java
@Controller 
public class HelloWorldController { 
    @RequestMapping(value = "/helloWorld.do") 
    @ModelAttribute("attributeName") 
    public String helloWorld() { 
        return "hi"; 
    } 
}
```
- 3. 绑定application/x-www-form-urlencoded 提交的请求中 的值到对象中 支持user.xxx,user2.ddd 嵌套对应法

```java
@Controller 
public class HelloWorldController { 
    @RequestMapping(value = "/helloWorld") 
    public String helloWorld(@ModelAttribute User user) { 
        return "helloWorld"; 
     } 
}
```

@CookieValue  和之前的相同，就是将cookie中相关的数据拿出来

```java
@GetMapping("/demo")
public void handle(@CookieValue("JSESSIONID") String cookie) {}
```

- HttpEntity<B> HttpEntity或多或少与使用@RequestBody相同，但基于公开请求标头和主体的容器对象。

注意这个方法多是用于post请求用来针对ajax序列化的json对象解析，其中有一个getbody方法

 ```java
@PostMapping("/accounts")
public void handle(HttpEntity<Account> entity) {
    Account account=entity.getBody();
}
 ```

- @InitBinder  spring自带的数据处理模块

由@InitBinder表示的方法，可以对WebDataBinder对象进行初始化。WebDataBinder是DataBinder的子类，用于完成由表单到JavaBean属性的绑定。
@InitBinder方法不能有返回值，它必须盛名为void。
@InitBinder方法的参数通常是WebDataBinder，@InitBinder可以对WebDataBinder进行初始化。


注意这个注解只是针对这个controller中的方法起作用，无法针对所有的controller

```java
@Controller
public class BinderAction {
    @RequestMapping("/sb2.do")
    public void doTest(@RequestParam(value="name")String name,@RequestParam(value="age")double age,@RequestParam(value="nowTime")Date nowTime){
        System.err.println("name:" + name);
        System.err.println("age:" + age);
        System.err.println("nowTime:" + nowTime);
    }    
    @InitBinder
    public void initBinder(WebDataBinder binder){
        binder.registerCustomEditor(Date.class, new CustomDateEditor(new SimpleDateFormat("yyyy-MM-dd"), true));
    }
    @InitBinder
    protected void initBinder(WebDataBinder binder) {
        binder.addCustomFormatter(new DateFormatter("yyyy-MM-dd"));
    }
}
```

注意WebDataBinder这个对象，这个对象拥有一个方法registerCustomEditor,这个方法将会自动的配置属性映射器，将相关的属性映射到指定的位置，属性映射器可以使用如下的方法进行自定义
实现PropertyEditor或者重写PropertyEditorSupport对象中的方法，注意这种方法只能实现string到对象的转换 setValue中就是转化后的对象，setAsText传入的就是传入的url字符串

```java
//实现PropertyEditor或者重写PropertyEditorSupport对象中的方法
import org.springframework.beans.propertyeditors.PropertiesEditor;
public class DoubleEditor extends PropertyEditorSupport {
    @Override
    public void setAsText(String text) throws IllegalArgumentException {
        if (text == null || text.equals("")) {
            text = "0";
        }
        setValue(Double.parseDouble(text));
    }
    @Override
    public String getAsText() {
        return getValue().toString();
    }
}
```
同时WebDataBinder这个对象，这个对象拥有一个addCustomFormatter 可以直接使用formatter进行参数转化本质上是相同的

```java
@InitBinder
protected void initBinder(WebDataBinder binder) {
    binder.addCustomFormatter(new DateFormatter("yyyy-MM-dd"));
}
```

addCustomFormatter本质上还是和registerCustomEditor是一样的见源代码

```java
public void addCustomFormatter(Formatter<?> formatter) {
	FormatterPropertyEditorAdapter adapter = new FormatterPropertyEditorAdapter(formatter);
	getPropertyEditorRegistry().registerCustomEditor(adapter.getFieldType(), adapter);
}
```

#### @RequestMapping 方法返回值中的参数

1. @ResponseBody


2. HttpEntity<B>, ResponseEntity<B>

- HttpEntity<B> HttpEntity或多或少与使用@RequestBody相同，但基于公开请求标头和主体的容器对象。

 ```java
@PostMapping("/accounts")
public void handle(HttpEntity<Account> entity) {
    // ...
}
 ```

- ResponseEntity<B> 这个类其实是对 http请求的一个封装，封装了http的报头，状态码，http code 等数据，本质上是一种通信协议

如果使用的不是string类型，那么将会是一种类似rpc协议

```java
//客户端
public void client(){
    RestTemplate restTemplate = new RestTemplate();
    ResponseEntity<String> entity = restTemplate.getForEntity("http://example.com", String.class);
    String body = entity.getBody();
    MediaType contentType = entity.getHeaders().getContentType();
    HttpStatus statusCode = entity.getStatusCode();
}

//服务端
@RequestMapping("/handle")
public ResponseEntity<String> handle() {
    URI location = ...;
    HttpHeaders responseHeaders = new HttpHeaders();
    responseHeaders.setLocation(location);
    responseHeaders.set("MyResponseHeader", "MyValue");
    return new ResponseEntity<String>("Hello World", responseHeaders,   HttpStatus.CREATED);
}
```

当使用string类型的时候就和@ResponceBody+@ResponseStatus 相同

```java
@RequestMapping("/handle")
public ResponseEntity<String> handle() {
    URI location = ...;
    return ResponseEntity.created(location).header("MyResponseHeader",  "MyValue").body("Hello World");
} 
```

3. HttpHeaders

返回一个封装的httpheaders的头，这个类有一个set方法，制定方法的头和内容，如果想深入的使用，需要精通http协议

```java
public HttpHeaders getHeader(){
    HttpHeaders httpHeaders = new HttpHeaders();
    return httpHeaders;   
}
```

4. string

最简单的一个方法，spring将会使用这个字符串找到对应的view

5. java.util.Map, org.springframework.ui.Model，@ModelAttribute

spring mvc modelandview体系的东西

6.  ResponseBodyEmitter, SseEmitter， StreamingResponseBody

7. Reactive types — Reactor, RxJava, or others via ReactiveAdapterRegistry

8. @ResponseStatus(HttpStatus.CREATED)

制定返回值的头部信息, 比如制定401 402 这种http code