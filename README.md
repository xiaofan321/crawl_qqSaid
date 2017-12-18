## qq空间说说爬虫 ##
----------
 
## 0x0 功能 ##
1.获取QQ空间说说
2.获取说说的评论


## 0x1 安装依赖 ##
selenium
bs4
lxml

## 0x2 简单说明 ##
用selenium 操作firefox，模拟正常人的访问来获取QQ空间说说内容以及评论

## 0x3 程序说明 ##
1.需要参数 qq用户名密码
2.login函数是登陆操作
  getAllpage函数用来获取说说总共多少页
  crawqq 为主要函数，通过下拉滚动条实现说说的异步加载

## 0x3 结果实例 ##
![](https://i.imgur.com/2vPxgZN.jpg)
