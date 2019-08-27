### 获取镜像 pull

关键命令

```shell
docker pull [选项] [Docker Registry 地址[:端口号]/]仓库名[:标签]
```

命名格式


- Docker 镜像仓库地址：地址的格式一般是 <域名/IP>[:端口号]。默认地址是 Docker Hub。
- 仓库名：如之前所说，这里的仓库名是两段式名称，即 <用户名>/<软件名>。对于 Docker Hub，如果不给出用户名，则默认为 library，也就是官方镜像。

### 运行镜像 run

镜像格式

```shell
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```



```shell
docker run -it --rm ubuntu:16.04 bash
```

启动容器有两种方式，一种是基于镜像新建一个容器并启动，另外一个是将在终止状态（stopped）的容器重新启动。

因为 Docker 的容器实在太轻量级了，很多时候用户都是随时删除和新创建容器。

OPTIONS说明：

- -a stdin: 指定标准输入输出内容类型，可选 STDIN/STDOUT/STDERR 三项；

- -d: 后台运行容器，并返回容器ID；

- -i: 以交互模式运行容器，通常与 -t 同时使用；

- -t: 为容器重新分配一个伪输入终端，通常与 -i 同时使用；

- --name="nginx-lb": 为容器指定一个名称；

- --dns 8.8.8.8: 指定容器使用的DNS服务器，默认和宿主一致；

- --dns-search example.com: 指定容器DNS搜索域名，默认和宿主一致；

- -h "mars": 指定容器的hostname；

- -e username="ritchie": 设置环境变量；

- --env-file=[]: 从指定文件读入环境变量；

- --cpuset="0-2" or --cpuset="0,1,2": 绑定容器到指定CPU运行；

- -m :设置容器使用内存最大值；

- --net="bridge": 指定容器的网络连接类型，支持 bridge/host/none/container: 四种类型；

- --link=[]: 添加链接到另一个容器；

- --expose=[]: 开放一个端口或一组端口；

当利用 docker run 来创建容器时，Docker 在后台运行的标准操作包括：

- 检查本地是否存在指定的镜像，不存在就从公有仓库下载
- 利用镜像创建并启动一个容器
- 分配一个文件系统，并在只读的镜像层外面挂载一层可读写层
- 从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去
- 从地址池配置一个 ip 地址给容器
- 执行用户指定的应用程序
- 执行完毕后容器被终止

### docker container start



### 列出镜像 image ls

```shell
docker image ls
```

打印输出所有的镜像

```shell
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
nginx               v3                  57bd2e54ef1b        24 hours ago        109MB
nginx               latest              5699ececb21c        6 days ago          109MB
ubuntu              16.04               5e8b97a2a082        3 weeks ago         114MB
hello-world         latest              e38bc07ac18e        2 months ago        1.85kB
```

#### 查看docker 磁盘的使用情况

```shell
docker system df
```

注意：这里引申一下docker image 命令显示出来的各种信息，docker image ls 列表中的镜像体积总和并非是所有镜像实际硬盘消耗。由于 Docker 镜像是多层存储结构，并且可以继承、复用，因此不同镜像可能会因为使用相同的基础镜像，从而拥有共同的层。由于 Docker 使用 Union FS，相同的层只需要保存一份即可，因此实际镜像硬盘占用空间很可能要比这个列表镜像大小的总和要小的多。

#### 特殊的玄虚镜像

由于新旧镜像同名，旧镜像名称被取消等，出现仓库名、标签均为 <none> 的镜二维码像。这类无标签镜像也被称为 虚悬镜像(dangling image)

> 使用这个命令将会直接的看到这些镜像

```
$ docker image ls -f dangling=true
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
<none>              <none>              00285df0df87        5 days ago          342 MB
```

> 一般来说，虚悬镜像已经失去了存在的价值，是可以随意删除的，可以用下面的命令删除。

```shell
$ docker image prune
```

#### 中间层镜像

默认的 docker image ls 列表中只会显示顶层镜像，如果希望显示包括中间层镜像在内的所有镜像的话，需要加 -a 参数。

```shell
$ docker image ls -a
```

这样会看到很多无标签的镜像，与之前的虚悬镜像不同，这些无标签的镜像很多都是中间层镜像，是其它镜像所依赖的镜像。这些无标签镜像不应该删除，否则会导致上层镜像因为依赖丢失而出错。实际上，这些镜像也没必要删除，因为之前说过，相同的层只会存一遍，而这些镜像是别的镜像的依赖，因此并不会因为它们被列出来而多存了一份，无论如何你也会需要它们。只要删除那些依赖它们的镜像后，这些依赖的中间层镜像也会被连带删除。

#### 列出部分镜像

不加任何参数的情况下，docker image ls 会列出所有顶级镜像，但是有时候我们只希望列出部分镜像。docker image ls 有好几个参数可以帮助做到这个事情。

> 根据仓库名列出镜像
```shell
$ docker image ls ubuntu
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              16.04               f753707788c5        4 weeks ago         127 MB
ubuntu              latest              f753707788c5        4 weeks ago         127 MB
ubuntu              14.04               1e0c3dd64ccd        4 weeks ago         188 MB
```

> 显示镜像详细信息

```shell
$ docker image ls --digests
```

这个方法将会显示出这个镜像的长id等信息


> 列出特定的某个镜像，也就是说指定仓库名和标签

```shell
$ docker image ls ubuntu:16.04
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              16.04               f753707788c5        4 weeks ago         127 MB
```

> docker image ls 还支持强大的过滤器参数 --filter，或者简写 -f

比如，我们希望看到在 mongo:3.2 之后建立的镜像，可以用下面的命令：

```shell
$ docker image ls -f since=mongo:3.2
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
redis               latest              5f515359c7f8        5 days ago          183 MB
nginx               latest              05a60462f8ba        5 days ago          181 MB
```

> 想查看某个位置之前的镜像也可以，只需要把 since 换成 before 即可。

#### 利用 docker image ls 把所有的虚悬镜像的 ID 列出来

```shell
$ docker image ls -q
5f515359c7f8
05a60462f8ba
fe9198c04d62
00285df0df87
f753707788c5
f753707788c5
1e0c3dd64ccd
```

#### 配合使用go 模板语法

下面的命令会直接列出镜像结果，并且只包含镜像ID和仓库名：

```shell
$ docker image ls --format "{{.ID}}: {{.Repository}}"
5f515359c7f8: redis
05a60462f8ba: nginx
fe9198c04d62: mongo
00285df0df87: <none>
f753707788c5: ubuntu
f753707788c5: ubuntu
1e0c3dd64ccd: ubuntu
```

或者打算以表格等距显示，并且有标题行，和默认一样，不过自己定义列：
```shell
$ docker image ls --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}"
IMAGE ID            REPOSITORY          TAG
5f515359c7f8        redis               latest
05a60462f8ba        nginx               latest
fe9198c04d62        mongo               3.2
00285df0df87        <none>              <none>
f753707788c5        ubuntu              16.04
f753707788c5        ubuntu              latest
1e0c3dd64ccd        ubuntu              14.04
```

### 删除本地镜像

#### 用 ID、镜像名、摘要删除镜像

如果要删除本地的镜像，可以使用 docker image rm 命令，其格式为：

```shell
$ docker image rm [选项] <镜像1> [<镜像2> ...]
```

<镜像> 可以是 镜像短 ID、镜像长 ID、镜像名(<仓库名>:<标签>) 或者 镜像摘要

> 引申： 短id 其实就是docker image ls 展示的相关的id

#### Untagged 和 Deleted

首先观察一个删除的命令和结果

```shell
$ docker image rm centos
Untagged: centos:latest
Untagged: centos@sha256:b2f9d1c0ff5f87a4743104d099a3d561002ac500db1b9bfa02a783a46e0d366c
Deleted: sha256:0584b3d2cf6d235ee310cf14b54667d889887b838d3f3d3033acd70fc3c48b8a
Deleted: sha256:97ca462ad9eeae25941546209454496e1d66749d53dfa2ee32bf1faabd239d38
```

删除行为分为两类，一类是 Untagged，另一类是 Deleted。我们之前介绍过，镜像的唯一标识是其 ID 和摘要，而一个镜像可以有多个标签。

因此当我们使用上面命令删除镜像的时候，实际上是在要求删除某个标签的镜像。所以首先需要做的是将满足我们要求的所有镜像标签都取消，这就是我们看到的 Untagged 的信息。因为一个镜像可以对应多个标签，因此当我们删除了所指定的标签后，可能还有别的标签指向了这个镜像，如果是这种情况，那么 Delete 行为就不会发生。所以并非所有的 docker image rm 都会产生删除镜像的行为，有可能仅仅是取消了某个标签而已。

当该镜像所有的标签都被取消了，该镜像很可能会失去了存在的意义，因此会触发删除行为。镜像是多层存储结构，因此在删除的时候也是从上层向基础层方向依次进行判断删除。镜像的多层结构让镜像复用变动非常容易，因此很有可能某个其它镜像正依赖于当前镜像的某一层。这种情况，依旧不会触发删除该层的行为。直到没有任何层依赖当前层时，才会真实的删除当前层。这就是为什么，有时候会奇怪，为什么明明没有别的标签指向这个镜像，但是它还是存在的原因，也是为什么有时候会发现所删除的层数和自己 docker pull 看到的层数不一样的源。

除了镜像依赖以外，还需要注意的是容器对镜像的依赖。如果有用这个镜像启动的容器存在（即使容器没有运行），那么同样不可以删除这个镜像。之前讲过，容器是以镜像为基础，再加一层容器存储层，组成这样的多层存储结构去运行的。因此该镜像如果被这个容器所依赖的，那么删除必然会导致故障。如果这些容器是不需要的，应该先将它们删除，然后再来删除镜像。

#### 用 docker image ls 命令来配合

像其它可以承接多个实体的命令一样，可以使用 docker image ls -q 来配合使用 docker image rm，这样可以成批的删除希望删除的镜像。我们在“镜像列表”章节介绍过很多过滤镜像列表的方式都可以拿过来使用。

> 比如，我们需要删除所有仓库名为 redis 的镜像：

```shell
$ docker image rm $(docker image ls -q redis)
```

> 或者删除所有在 mongo:3.2 之前的镜像：

```shell
$ docker image rm $(docker image ls -q -f before=mongo:3.2)
```

> 充分利用你的想象力和 Linux 命令行的强大，你可以完成很多非常赞的功能。

### docker commit 命令和相关的问题

docker commit 的语法格式为：

```shell
docker commit [选项] <容器ID或容器名> [<仓库名>[:<标签>]]
```

可以使用如下的方法将指定的容器打包成镜像

```shell
$ docker commit \
    --author "Tao Wang <twang2218@gmail.com>" \
    --message "修改了默认网页" \
    webserver \
    nginx:v2
sha256:07e33465974800ce65751acc279adc6ed2dc5ed4e0838f8b86f0c87aa1795214
```

> 引申：其中 --author 是指定修改的作者，而 --message 则是记录本次修改的内容。这点和 git 版本控制相似，不过这里这些信息可以省略留空。

使用 docker commit 命令虽然可以比较直观的帮助理解镜像分层存储的概念，但是实际环境中并不会这样使用。

首先，如果仔细观察之前的 docker diff webserver 的结果，你会发现除了真正想要修改的 /usr/share/nginx/html/index.html 文件外，由于命令的执行，还有很多文件被改动或添加了。这还仅仅是最简单的操作，如果是安装软件包、编译构建，那会有大量的无关内容被添加进来，如果不小心清理，将会导致镜像极为臃肿。

此外，使用 docker commit 意味着所有对镜像的操作都是黑箱操作，生成的镜像也被称为黑箱镜像，换句话说，就是除了制作镜像的人知道执行过什么命令、怎么生成的镜像，别人根本无从得知。而且，即使是这个制作镜像的人，过一段时间后也无法记清具体在操作的。虽然 docker diff 或许可以告诉得到一些线索，但是远远不到可以确保生成一致镜像的地步。这种黑箱镜像的维护工作是非常痛苦的。

> 注意： 应该使用dockerfile 进行相关的镜像生成和维护工作




