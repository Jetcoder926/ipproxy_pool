# ipproxy_pool
#### 隔离在家太无聊催生了这个项目...
#### 很多网站都会有基本的反爬行机制.那么反ban措施之一就是搞个ip代理池了.网上有很多收费的代理ip服务(luminati、oxylabs等等).本项目目前的功能是爬取几个免费代理网站的代理Ip(包括西刺代理、快代理、66代理)、验证连接失败删掉无效ip、验证有效存入mongodb库供自定义爬虫调用.后期会更新更多功能.



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
* config目录下的config.py是项目的运行配置文件.
* db目录下的MongodbManager是初始化mongodb连接的类，model目录的proxymodel.py负责项目初始化时创建mongodb的database、代理ip的筛选、奖惩制度等等
* middlewares 目录是放自定义中间件 proxyMiddleware.py有2个职责责 1.设置请求的代理 2.处理连接超时或失败的ip；RandomUserAgentMiddleware.py负责设置请求头随机user-agent
* requester目录的requestEnginer.py负责1.把下载回来的数据过滤,2.验证ip的有效性3.一些请求任务
* spiders目录的proxySpiders目录存放爬代理ip的蜘蛛；yourSpider目录存放你自定义的爬虫项目


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
2.在你需要代理的自定义爬虫项目里的Request方法加上meta={'proxy':''}参数<br/>
3.修改EngineStar.py里的 your_spiders_list<br/>
4.运行EngineStar.py即可. 项目会生成2个进程.一个是爬代理ip的进程,另一个是自定义蜘蛛的进程.第一个进程跑完再会去运行第二个进程<br/>

## 参考资料
https://www.osgeo.cn/scrapy/index.html<br/>
https://docs.python.org/zh-cn/3/library/index.html


## 最后

#### 中国必胜,武汉必胜 -- 2020
