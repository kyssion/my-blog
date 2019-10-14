gradle可以自动的执行测试样例，前提是要求测试的包名和要测试的类是一一对应的

当项目中编写了Test目录中的内容的时候，然后指定的测试样例写法正确，当运行test task的时候，gradle将会自动的执行对应的测试，并且在build的build 文件夹中的reports 以html的形式，输出对应的结果

![](blogimg/gradle/1.png)

![](blogimg/gradle/2.png)