oAuth2.0 是一个广泛应用的认证授权方法,我最开始接触的时候是在微信登入授权上

在整个oAuth2.0的认证有以下的参与者

- (1)Third-party application：第三方应用程序,称"客户端"(client)
- (2)HTTP service：HTTP服务提供商,简称"服务提供商"
- (3)Resource Owner：资源所有者,称"用户"(user).
- (4)User Agent：用户代理,本文中就是指浏览器.
- (5)Authorization server：认证服务器,即服务提供商专门用来处理认证的服务器.
- (6)Resource server：资源服务器,即服务提供商存放用户生成的资源的服务器.它与认证服务器,可以是同一台服务器,也可以是不同的服务器.

oAuth2.0的官方流程是这样的

![](blogimg/oauth2/oauth1.png)

- (A)用户打开客户端以后,客户端要求用户给予授权.
- (B)用户同意给予客户端授权.
- (C)客户端使用上一步获得的授权openToken,向认证服务器申请令牌accesssToken.
- (D)认证服务器对客户端进行认证以后,确认无误,同意发放令牌accesssToken.
- (E)客户端使用令牌,向资源服务器申请获取资源.
- (F)资源服务器确认令牌无误,同意向客户端开放资源.

其实这个登入流程的核心就是如何获取这个accessToken,这里对比微信登入,做一个整理


