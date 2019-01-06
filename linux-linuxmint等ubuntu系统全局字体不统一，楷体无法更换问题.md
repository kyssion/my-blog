## linux mint等ubuntu系统全局字体不统一，楷体无法更换问题

此页面是关于此楷体无法更换问题的，应该是类乌班图系统都会遇到的问题: https://bugs.launchpad.net/ubuntukylin/+bug/1227034 

新安装的Linux mint 字体更新了以后，设置的全局字体不统一，部分字体偏小，部分字体甚至是比较小的楷体，模糊不清，十分影响观感和使用体验。

终端使用命令fc-match ‘sans-serif’和fc-match ‘serif’和fc-match ‘monospace’均输出类似于ukai.ttc: “AR PL UKai CN” “Book”如果删除了ukai即楷体则输出uming.ttc: “AR PL UMing CN” “Light”。
种种迹象表面是/etc/font/conf.d中的某文件改写错误造成.
新安装的linuxMint应该均会出现这样的楷体错误。 一个简单的解决办法是终端输入命令： 

```shell 
sudo apt-get install language-selector-*
```

安装完成后字体会改变为

```
~ $fc-match 'sans-serif'
NotoSansCJK-Regular.ttc: "Noto Sans CJK SC" "Regular"
~ $fc-match 'serif'
uming.ttc: "AR PL UMing CN" "Light"
~ $fc-match 'monospace'
DejaVuSansMono.ttf: "DejaVu Sans Mono" "Book"
```

另外建议新安装的Mint18全中文系统，使用文本编辑器比如kate执行

```
sudo kate /var/lib/locales/supported.d/local
```

或者

```
sudo kate /var/lib/locales/supported.d/zh-hans
```

编辑其中的一个文件即可。添加如下内容，以配置更完全详细的中文本地支持. 

```
en_US.UTF-8 UTF-8
zh_CN.UTF-8 UTF-8
zh_CN.GBK GBK
zh_CN GB2312
zh_CN.GB18030 GB18030
zh_CN.GBK GBK
zh_HK BIG5-HKSCS
zh_HK.UTF-8 UTF-8
zh_SG GB2312
zh_SG.GBK GBK
zh_SG.UTF-8 UTF-8
zh_TW BIG5
zh_TW.EUC-TW EUC-TW
zh_TW.UTF-8 UTF-8
```

然后执行 sudo locale-gen

``` 
Generating locales (this might take a while)...
en_AG.UTF-8... done
en_AU.UTF-8... done
en_BW.UTF-8... done
en_CA.UTF-8... done
en_DK.UTF-8... done
en_GB.UTF-8... done
en_HK.UTF-8... done
en_IE.UTF-8... done
en_IN.UTF-8... done
en_NG.UTF-8... done
en_NZ.UTF-8... done
en_PH.UTF-8... done
en_SG.UTF-8... done
en_US.UTF-8... done
en_ZA.UTF-8... done
en_ZM.UTF-8... done
en_ZW.UTF-8... done
zh_CN.GB2312... done
zh_CN.GB18030... done
zh_CN.GBK... done
zh_CN.UTF-8... done
zh_HK.BIG5-HKSCS... done
zh_HK.UTF-8... done
zh_SG.GB2312... done
zh_SG.GBK... done
zh_SG.UTF-8... done
zh_TW.BIG5... done
zh_TW.EUC-TW... done
zh_TW.UTF-8... done
```
