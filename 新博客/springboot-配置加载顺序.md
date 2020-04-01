优先级由高到低,高优先级覆盖低优先级

1.在命令行中传入的参数;
2.SPRING_APPLICATION_JSON 中的属性。SPRING_APPLICATION_JSON 是以JSON 格式配置在系统环境变量中的内容；
3.java:comp/env 中的 JNDI 属性;
4.java 的系统属性，可以通过System.getProperties()获得的内容;
5.操作系统的环境变量。
6.通过random.*配置的随机属性；
7.位于当前应用jar包之外，针对不同{profile}环境的配置文件内容，例如 applicaiton-{profile}.properties 或是 yaml 定义的配置文件；
8.位于当前应用jar包之内，针对不同{profile}环境的配置文件内容，例如 applicaiton-{profile}.properites 或是 yaml 定义的配置文件；
9.位于当前应用jar包之外的 application.properties 和yaml配置内容；
10.位于当前应用jar包之内的 application.properties 和yaml配置内容；
11.在@Configration注解修改的类中，通过@PropertySource注解定义的属性；
12.应用默认属性，使用SpringApplication.setDefaultProperties定义的内容；