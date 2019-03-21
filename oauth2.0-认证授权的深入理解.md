oAuth2.0 是一个广泛应用的认证授权方法,我最开始接触的时候是在微信登入授权上

在整个oAuth2.0的认证有以下的参与者

```
（1） Third-party application：第三方应用程序，本文中又称"客户端"（client），即上一节例子中的"云冲印"。

（2）HTTP service：HTTP服务提供商，本文中简称"服务提供商"，即上一节例子中的Google。

（3）Resource Owner：资源所有者，本文中又称"用户"（user）。

（4）User Agent：用户代理，本文中就是指浏览器。

（5）Authorization server：认证服务器，即服务提供商专门用来处理认证的服务器。

（6）Resource server：资源服务器，即服务提供商存放用户生成的资源的服务器。它与认证服务器，可以是同一台服务器，也可以是不同的服务器。
```