1. 校验文件是否存在

```bash
if ! [ -f "文件名称" ] ; then
    xxxxx
if
```

2. 制定bash的文件目录


```bash
cd xxxxx || exit
```

> 这里是一个规范 ， cd 操作很可能存在问题 ，所以一般会联动 exit 终止脚本