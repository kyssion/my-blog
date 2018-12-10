一般情况下，我们有的时候可能需要对web框架的返回值进行一定的处理，但是这种情况下有一定的局限性比如下面这种使用拦截器的情况

```java
public class ControllerReturnInterceptor implements HandlerInterceptor {
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        System.out.println(handler);
    }
}
```

我们继承了HandlerUbterceotor 接口并且实现了postHandle 方法，这个方法将会在controller处理完之后将返回值放入handler中，通过这种方法我们可以对handler中的属性进行修改。

但是这样是有局限性的，首先我们无法封装handler 比如将返回的值换成另一个类，其次这个对象是object 我们需要强制转化才能使用，这样就有了一定的局限性。

正因为这样在spring4 添加了两个新的接口 RequestBodyAdvice和ResponseBodyAdvice

```java
public interface RequestBodyAdvice {

	boolean supports(MethodParameter methodParameter, Type targetType,
			Class<? extends HttpMessageConverter<?>> converterType);

	HttpInputMessage beforeBodyRead(HttpInputMessage inputMessage, MethodParameter parameter,
			Type targetType, Class<? extends HttpMessageConverter<?>> converterType) throws IOException;

	Object afterBodyRead(Object body, HttpInputMessage inputMessage, MethodParameter parameter,
			Type targetType, Class<? extends HttpMessageConverter<?>> converterType);

	Object handleEmptyBody(@Nullable Object body, HttpInputMessage inputMessage, MethodParameter parameter,
			Type targetType, Class<? extends HttpMessageConverter<?>> converterType);

}
public interface ResponseBodyAdvice<T> {

	boolean supports(MethodParameter returnType, Class<? extends HttpMessageConverter<?>> converterType);

	@Nullable
	T beforeBodyWrite(@Nullable T body, MethodParameter returnType, MediaType selectedContentType,
			Class<? extends HttpMessageConverter<?>> selectedConverterType,
			ServerHttpRequest request, ServerHttpResponse response);

}

```

其中supports方法是为了判断是否可以执行处理逻辑，剩下的方法就封装恶劣在参数生成之前之后等操作步骤和拦截器相同，就不在多说了
