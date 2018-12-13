## pring5-springMVC异步请求支持

提供AsyncRestTemplate用于客户端非阻塞异步支持

### 服务端

```java
@RestController
public class UserController {
    private UserService userService;
    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }
    @RequestMapping("/api")
    public Callable<User> api() {
        System.out.println("=====hello");
        return new Callable<User>() {
            @Override
            public User call() throws Exception {
                Thread.sleep(10L * 1000); //暂停两秒
                User user = new User();
                user.setId(1L);
                user.setName("haha");
                return user;
            }
        };
    }
}
```

### 客户端

```java
public class UserController {
    public static void main(String[] args) {
        AsyncRestTemplate template = new AsyncRestTemplate();
        //调用完后立即返回（没有阻塞）
        ListenableFuture<ResponseEntity<User>> future = template.getForEntity("http://localhost:9080/spring4/api", User.class);
        //设置异步回调
        future.addCallback(new ListenableFutureCallback<ResponseEntity<User>>() {
            @Override
            public void onSuccess(ResponseEntity<User> result) {
                System.out.println("======client get result : " + result.getBody());
            }

            @Override
            public void onFailure(Throwable t) {
                System.out.println("======client failure : " + t);
            }
        });
        System.out.println("==no wait");
    }
}
```

**注意**:这个方法在spring5中是过期的，使用 WebClient