今天刚刚进行工作一个星期，感觉自己以前在大学里自己做项目的时候许多欠缺的地方，比如说版本控制上的欠缺，这里写几篇博客补充一下自己在版本控制上面的坑

### 将一个纳入git的控制之中

```java
git init
```

这个命令将一个文件夹新建成一个git仓库

### 将文件放入暂存区

```java
git add *
```

这个方法可以一个或者多个方法放入文件的暂存区

### 克隆远程版本库

```java
git clone <版本库的网址>
```

可以将指定的远程仓库克隆到本地

#### 更新本的仓库中的文件

```java
git pull origin next:master
```

上面例子中代码的作用就是将哦origin指定的远程仓库中的next分支合并到本地分支中

> 在默认模式下，git pull是git fetch后跟git merge FETCH_HEAD的缩写

### git branch

git branch 对命令进行分支进行操作

```java
git breach -a  #l列出所有的分支 包括远程分支和本地分支
git branch -r  #  单独的列出远程的分支
git branch #列出本地分支
git branch xxx
```

### 其他的一些说明

```java
git log 查看commit的历史
git show <commit-hash-id>查看某次commit的修改内容
git log -p <filename>查看某个文件的修改历史
git log -p -2查看最近2次的更新内容
```