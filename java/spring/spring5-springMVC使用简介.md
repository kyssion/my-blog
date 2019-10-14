## spring5-springMVC使用

使用一个基本demo进行相关的整理

### java  controller

```java
//当不是用配置文件的时候我们将不需要使用接口直接使用一个注释
@Controller//这个注释讲这个bean配制成一个控制器-注解没有标记只是起到了一个标记的作用
//注意要让这个注解起到作用需要早xml文件中进行配置
@EnableWebMvc
//@RequestMapping(value="/sdf")//这样下面的所有方法的起始地址就是/sdf
public class Noconfig {
    @RequestMapping(value="/mappingOne",method={RequestMethod.GET,RequestMethod.PUT})
    //注解中属性-value：表示需要匹配的url的格式。 //method：表示所需处理请求的http 协议(如get,post,put,delete等)，可选值为RequestMethod这个enum的值。
    //params:格式为”paramname=paramvalue” 或 “paramname!=paramvalue”。不带参数则表示paramvalue可以为任意值。
    //  如params =  {"param1=1","param2!=2","param3"},
    //  表示对应的url必须包括param1,param2,param3三个参数，其中param1的值必须为1，param2的值不能为2，param3的值可以为任意值。
    //headers:用来限定对应的reqeust请求的headers中必须包括的内容，例如
    //  headers={"Connection=keep-alive"}, 表示请求头中的connection的值必须为keep-alive。
    //  定义的方法中可以讲需要的属性直接写进去,从而直接能得到,spring底层使用反射技术能动态的知道你需要什么属性
    //spring支持的属性
    //     java- HttpServletRequest HttpServletServletResponse HttpSession Locale 
    //           inputstream reader outputStream writer Map 
    //spring的属性WebRequest NativeWebRequest ModeMap model- 
    //         表单对象(气势model 或者 map 或者 ModeMap就是封装了request.setAttrbute方法)
    //注意这些参数都是在一个请求中有效也就是说只要获取了对台进行操作在一次请求转发过程中都能获得和进行操作
    public ModelAndView mappingOne(HttpServletRequest request,HttpServletResponse response ,ModelMap modelMap){
        System.out.println(request.getParameter("one"));
        modelMap.addAttribute("xixi", "123145");
        return new ModelAndView("myModeAndView");
        //处理方法可以返回的类型
        //Modelandview Medel map View 代表逻辑属兔名称的String void 
    }
    @RequestMapping(value="mappingTwo/{id}/{xixi}",method={RequestMethod.GET,RequestMethod.POST})
    public void mappingTwo(@PathVariable() int id,@PathVariable String xixi){
        //一种解析url的方法 -讲url地址地址中的方法进行解析处理  名称要相互匹配要相同
        //name(value) - 指定绑定的参数

        System.out.println(id+"  "+xixi);
    }
    @RequestMapping(value="mappingThree",method={RequestMethod.GET,RequestMethod.POST})
    public void mappingThree(@RequestParam(value="sadf") int id,@RequestParam String hehe){
        //讲url 地址中的响应字子自动和函数中的参数相匹配 注意名称要相互匹配要相同
        //name-指定参数中那个元素和者个进行绑定 value 是他的别名
        //defaulfvalue -  指定默认的参数
        System.out.println(id+"  "+hehe);
    }
    //spring 重定向
    public String mappingFour(RedirectAttributes redirectAttributes){
        redirectAttributes.addFlashAttribute("xx", "asdfasdf");//使用这个方法可以实现内部的重定向属性传递方法
        //在spring中返回字符串使用rediret开头的时候表使用了重定向技术
        return "redirect:/xxxx/";
    }
    //设置请求头为utf8 解决中文乱码
    @RequestMapping(value="name",produces = "application/json;charset=utf-8")
    @ResponseBody
    public String hehe() {
        return "sdfsdf";
    }
    //model and view 
    public void springModelandView(){
        //modelandview 其实是将model和view 封装在一个如果想使用需要使用get方法生成
        ModelAndView modelAndView = new ModelAndView();
        //modelAndView= new ModelAndView(viewName, model)
        modelAndView.addAllObjects(new HashMap<String,String>());
        modelAndView.addObject("xxx", "xxx");
        View view=modelAndView.getView();
        ModelMap map =modelAndView.getModelMap();
        modelAndView.setView(view);
        modelAndView.setViewName("xxx");
        //modelMap--其实是map的实现类而已
        ModelMap map2= new ModelMap();
        map.addAllAttributes(new HashMap<String,String>());
        map.addAttribute("xx", "heh");
        //view---没什么用就当是字符串就好了
        View view2 = new View() {
            public void render(Map<String, ?> arg0, HttpServletRequest arg1, HttpServletResponse arg2) throws Exception {}
            public String getContentType() {return null;}
        };
    }
}
```

其他一些注解

```java
@EnableWebMvc//开起一些viewResolver或者MessageConverter等
@RestController// 相当于Controller和ResponseBody的结合，使用在类上面，导致所有的返回值都是body类型
```

### springMVC webapplication 配置文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/mvc http://www.springframework.org/schema/mvc/spring-mvc-4.3.xsd
		http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.2.xsd
		http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.3.xsd">
    <context:annotation-config></context:annotation-config>
    <!-- 激活spring关于annotation的DI -->
    <!--  	注册 DefaultAnnotationHandlerMapping 和AnnotationMethodHandlerAdapter两个bean，
    及一系列缺省的messageconverter(需要classpath中有相应的lib包的支持)
            并且启用了controler中的url请求参数绑定参数绑定
     -->
    <mvc:annotation-driven></mvc:annotation-driven>
    <!-- 注册HandlerInterceptors 或 WebRequestInterceptors 拦截器来拦截request请求 -->
    <mvc:interceptors>
        <mvc:interceptor>
            <mvc:mapping path="/*" />
            <bean class="p_spring事务.hasconfig.CustomerTransforHasConfig" />
        </mvc:interceptor>
    </mvc:interceptors>

    <!--将spring mvc的DispatcherServlet替换当前web server的缺省的Servlet。
        这样做的好处是定义spring mvc处理请求时，不再需要定义*.do,*.action,/action/*之类的url-pattern，
        而是可以直接定义为<url-pattern>/</url-pattern> 
        （注意不是<url-pattern>/*</url-pattern>，/*将匹配所有请求而导致所有jsp和静态内容都无法正常显示，而/只匹配缺省的servlet）。 
        常见web 容器的default servlet name spring mvc中都能自动识别，
        但对于不常见的web 容器或default servlet name 被改写过的，则需增加参数 default-servlet-name来指定对应的servlet name. 
        需与<mvc:annotation-driven/>一起使用 
    -->
    <mvc:default-servlet-handler/>
    <!-- 将指定路径的请求直接转到对应的view上，而不需要特定的controller来处理请求 -->
    <mvc:view-controller path="/hello/*" view-name="helloWorld"/>
    <!-- 将指定URL 的匹配模式来访问静态文件 -->
    <mvc:resources mapping="/js/**" location="/WEB-INF/js/" cache-period="3600"/>
</beans>
```

### web.xml配置文件


```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         id="WebApp_ID" version="3.1">
    <display-name>Spring和SpringMVC和SpringBoot和Mybatis</display-name>
    <welcome-file-list>
        <welcome-file>index.html</welcome-file>
        <welcome-file>index.htm</welcome-file>
        <welcome-file>index.jsp</welcome-file>
        <welcome-file>default.html</welcome-file>
        <welcome-file>default.htm</welcome-file>
        <welcome-file>default.jsp</welcome-file>
    </welcome-file-list>
    <!-- 在spring体系中 root appliction使用 ContextLoaderListener进行加载 webapplication使用 Dispatchar加载  webappliction会继承 rootapplication 的继承 -->
    <!-- 和ContextLoaderListener 相互对应实现对除了mvc层的控制 自动装配ApplicationContext的配置信息。因为它实现了ServletContextListener这个接口-->
    <context-param>
        <param-name>contextConfigLocation</param-name>
        <!-- 如果不写默认的配置路径是 /WEB-INF/applicationContext.xml 下面的配置使用通配符表示使用所有的配置文件-->
        <param-value>/WEB-INF/application.xml</param-value>
    </context-param>
    <listener>
        <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
    </listener>
    <!-- 添加文字控制servlet层 -->
    <filter>
        <filter-name>CharacterEncodingFilter</filter-name>
        <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
        <init-param>
            <param-name>encoding</param-name>
            <param-value>utf-8</param-value>
        </init-param>
    </filter>
    <filter-mapping>
        <filter-name>CharacterEncodingFilter</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
    <servlet>
        <servlet-name>springMVC</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <!-- 设置webappliction 的默认加载位置 -->
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>/WEB-INF/springMVC-servlet.xml</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>
    <servlet-mapping>
        <servlet-name>springMVC</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
</web-app>
```

### springMVC过滤器


```java
package q_springMVC.过滤器;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;
//实现自定义spring拦截器必须继承的接口HandlerINterceptor  但是如果要使用这个拦截器需要将这个拦截器注册到相应的springmvc的配置文件(不是web.xml)中去
public class MyspringFilter implements HandlerInterceptor{
    @Override
    public void afterCompletion(HttpServletRequest arg0, HttpServletResponse arg1, Object arg2, Exception arg3)
            throws Exception {
        // TODO Auto-generated method stub
        //请求结束的时候调用的方法 object类的效果和上面的的相同 Exception表示抛出的异常
        //试图完成后执行的各种参数

    }

    @Override//在业务处理器处理请求执行完成后,生成视图之前执行
    public void postHandle(HttpServletRequest arg0, HttpServletResponse arg1, Object arg2, ModelAndView arg3)
            throws Exception {
        // TODO Auto-generated method stub

    }

    @Override//这个方法表示是否见当前的请求拦截下来 true表示不false 拦截  参数中有一个object 的类i表示将要进行拦截对象的实例
    public boolean preHandle(HttpServletRequest arg0, HttpServletResponse arg1, Object arg2) throws Exception {
        // TODO Auto-generated method stub
        return true;
    }

}
```

### 相关流程简介

![](blogimg/springMVC/1.png)

![](blogimg/springMVC/2.png)

![](blogimg/springMVC/3.png)