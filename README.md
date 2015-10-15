# 搜狐移动首页爬虫

## 需要安装的模块
1. ``` pip install docopt ```
2. ``` pip install requests ```

## 爬取需求

1. 保存全部图片
2. 保存css和js文件
3. 尽可能还原网页

## 爬取思路

### 反爬虫

由于站点有反爬虫机制，所以要模拟浏览器访问，要修改请求头部。否则后面的js文件不会再源码中出现，css文件也不相同。

### 保存图片
网页中图片可以分成四类：

#### 有加载动画的图片:

```<img src="http://s1.rr.itc.cn/p/images/imgloading.jpg" original="http://s8.rr.itc.cn/org/wapChange/201510_15_7/b5o70d8524002308451.jpg" width="146" height="124" />```

这类图片标签中**src**是加载动画，需要的真正图片在**original**中，所以需要爬去的**original**中的url，然后用get请求下载图片。

#### 正常的图片标签： 

```<img src="http://s1.rr.itc.cn/w/u/0/home_logo.png" alt="搜狐网SOHU.com" name="搜狐网SOHU.com">```

这类图片只需要爬去**src**中的url，然后用get下载即可。

#### 固定的图片，即不是动态加载而来的：

网页中一共有三个固定的图片是：加载图片、左箭头、右箭头

```<img src="http://s1.rr.itc.cn/p/images/imgloading.jpg" original="http://s8.rr.itc.cn/org/wapChange/201510_15_7/b5o70d8524002308451.jpg" width="146" height="124" />```

```<img src="http://s8.rr.itc.cn/org/wapChange/20156_2_15/b84mvp4105546836266.png" width="11"></a> <a class="page-next">```

```<img src="http://s9.rr.itc.cn/org/wapChange/20156_2_15/a81j1i5977584219487.png" width="11">```

只需要去固定的url中下载即可。

### 保存css和js文件

绕开站点的反爬虫后就可得到正确的css和js文件的url。

```<link rel="stylesheet" type="text/css" href="http://s2.rr.itc.cn/h5/css/msohu/v3/tags/3.2.14/c/home.css" media="all">```

```<script type="text/javascript" src="http://s1.rr.itc.cn/h5/js/tags/v3/msohu/3.2.14/home.js"></script>```

提取url下载即可

### ajax加载部分

由于ajax动态加载，在保存源码的时候无法把这部分也保存下载，导致一个section无法显示。
我的解决办法是先获取```http://m.sohu.com/api/house/```该url的json返回值，然后使用返回值手动构建缺失的section部分，去替换原来空的section。

## 使用方法

```main.py -d <sec> -u <url> -o <output>```