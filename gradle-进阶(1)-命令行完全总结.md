这里记录一下gradle的详细使用信息

# gradle 命令的组成

> gradle的命令总体上只有两个点 taskname 和 option

```
gradle [task-Name...] [--option-name...]
```

如果不带-- 就是task 带的话就是option

> option可能带有参数,这里使用=号来为他赋值

```
--console=plain
```

> 可以使用 --no- 来命名反转,表示不进行什么操作

```
--build-cache 
--no-build-cache
```

> option具有等价形式比如

```
--help
等价
-h
```

# gradle 执行task

> 在子项目环境下可以使用[:子项目名称]...[:子项目名称][:taskName] 来运行指定的task(只是在root项目中可以运行)

```
gradle :mySubproject:taskName
```

> 如果没有指定子项目名称将会从当前目录的项目中向下寻找task

```
gradle taskName
```

> 多task运行

应用上面的规则,使用空格可开就可以指定多个子task顺序执行了

```
gradle test deploy
```

> 移除一个task

使用 --exclude-task 移除gradle运行过程中的一个task

```
gradle dist --exclude-task test
```

