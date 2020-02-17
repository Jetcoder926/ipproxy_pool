# ipproxy_pool
#### 隔离在家太无聊催生了这个项目...
#### 很多网站都会有基本的反爬行机制.例如检测请求头中的user-agent、限制短时间内ip的访问频率、ip大量重复会被Ban之类.那么反ban机制之一就是ip代理池了.此项目目前仅仅爬取几个免费代理网站的代理Ip、验证连接失败删掉无效ip、存入mongodb库供自定义爬虫调用.



## 项目说明
#### 目录结构
* ipproxy_pool
	+ config
	+ db
    	- model
	+ middlewares
	+ requester
	+ spiders
		- proxySpiders
		- yourSpider


* EngineStar.py是项目主入口文件.负责启动爬虫
* config目录下的config.py文件是项目的运行配置文件.
* db目录下的MongodbManager是初始化mongodb连接的类，model目录的proxymodel.py负责项目初始化时创建mongodb的database、代理ip的筛选、奖惩制度等等
* middlewares 目录是放自定义中间件 proxyMiddleware.py有2个职责责 1.设置请求的代理 2.处理连接超时或失败的ip；RandomUserAgentMiddleware.py负责设置请求头随机user-agent
* requester目录的requestEnginer.py负责1.把下载回来的数据过滤,2.验证ip的有效性3.一些请求任务
* spiders目录的proxySpiders目录存放爬代理ip的蜘蛛；yourSpider目录存放爬业务的蜘蛛


## 使用说明

### 1 项目环境
* python 3.6或以上
<br/>
你需要通过 pip 安装以下依赖：

* requests version:lastest
* scrapy version:lastest
* pymongo version:lastest

### 2 修改配置
1.修改config目录下config.py文件中的mongodb连接配置 <br/>
2.修改EngineStar.py里的 proxy_spiders_list 和 your_spiders_list<br/>
3.运行EngineStar.py即可. 项目会生成2个进程.一个是爬代理ip的进程,另一个是自定义蜘蛛的进程.第一个进程跑完再会去运行第二个进程<br/>

### 最后

#### 中国必胜,武汉必胜 -- 2020
