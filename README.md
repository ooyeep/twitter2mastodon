# twitter2mastodon

**企图维护一个  Twitter username 到 Mastodon username 的公共列表。**  
**支持安装油猴脚本，在用户主页显示跳转按钮。**  
本程序由本废物完成1%，ChatGPT完成99%  

# 登记方法 

首先在 [公共登记页面](https://t2m.ooyeep.uk/) 完成授权登录，授权登录仅仅验证Twitter用户名，不会进行其他操作。 

然后再提交你的 Mastodon 信息 

# Tampermonkey 脚本

~~那个repo首页上有个`user.js`文件，你打开进去把东西复制一下，然后手动到油猴里面新建一个脚本，添加和安装和启用~~  

[直接到这里安装，勉强能用](https://greasyfork.org/zh-CN/scripts/470141-twitter-to-mastodon-redirector)

'Ctrl + S' 保存文件，保存前可以修改下`HOME_SERVER`到你最常用的mstdn实例。

# API

```
[GET] https://t2m.ooyeep.uk/api?username=TWITTER_USERNAME
```
返回示例
```
{"mastodon_domain":"nya.one","mastodon_username":"ooyeep","status":"success"}
```

# 安全性

目前能运行，其他的不清楚
