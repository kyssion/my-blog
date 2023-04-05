其实这个东西是linux的一个信号

# linux 结束任务有三种信号量 sigint sigterm sigkill

1. sigint : 和ctrl+c关联 , 用来终止当前终端中正在运行的任务
2. sigterm : 相当于kill进程 , 会终止当前终端的后台任务(在当前终端的守护线程中的任务)
3. sigkill : 相当于kill -9 , 不会和sigterm信号量会等待当前线程结束 , 而是直接的杀死它

# linux 程序运行时状态切换

## 一、&

加在一个命令的最后，可以把这个命令放到后台执行，如
watch -n 10 sh test.sh & #每10s在后台执行一次test.sh脚本

## 二、ctrl + z

可以将一个正在前台执行的命令放到后台，并且处于暂停状态。

## 三、jobs

查看当前有多少在后台运行的命令
jobs -l选项可显示所有任务的PID，jobs的状态可以是running, stopped, Terminated。但是如果任务被终止了（kill），shell 从当前的shell环境已知的列表中删除任务的进程标识。

## 四、fg

将后台中的命令调至前台继续运行。如果后台中有多个命令，可以用fg %jobnumber（是命令编号，不是进程号）将选中的命令调出。


## 五、bg

将一个在后台暂停的命令，变成在后台继续执行。如果后台中有多个命令，可以用bg %jobnumber将选中的命令调出。


## 六、kill

法子1：通过jobs命令查看job号（假设为num），然后执行kill %num
法子2：通过ps命令查看job的进程号（PID，假设为pid），然后执行kill pid
前台进程的终止：Ctrl+c


## 七、nohup

如果让程序始终在后台执行，即使关闭当前的终端也执行（之前的&做不到），这时候需要nohup。该命令可以在你退出帐户/关闭终端之后继续运行相应的进程。关闭中断后，在另一个终端jobs已经无法看到后台跑得程序了，此时利用ps（进程查看命令）

ps -aux | grep “test.sh” #a:显示所有程序 u:以用户为主的格式来显示 x:显示所有程序，不以终端机来区分

