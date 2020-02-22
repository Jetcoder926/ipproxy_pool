# ipproxy_pool
#### 隔离在家太无聊催生了这个项目...
#### 很多网站都会有基本的反爬行机制.那么反ban措施之一就是搞个ip代理池了.网上有很多收费的代理ip服务(luminati、oxylabs等等).本项目目前的功能是爬取几个免费代理网站的代理Ip(包括西刺代理、快代理、66代理)、验证连接失败删掉无效ip、验证有效存入mongodb库供自定义爬虫调用.后期会更新更多功能.



## 项目说明
#### 目录结构
<pre>
|-- ipproxy_pool
    |-- items.py
    |-- middlewares.py
    |-- pipelines.py
    |-- settings.py
    |-- utils.py
    |-- __init__.py
    |-- config
    |   |-- config.py
    |   |-- __init__.py
    |-- db
    |   |-- MongodbManager.py
    |   |-- __init__.py
    |   |-- model
    |       |-- proxymodel.py
    |       |-- __init__.py
    |-- middlewares
    |   |-- proxyMiddleware.py
    |   |-- RandomUserAgentMiddleware.py
    |   |-- __init__.py
    |-- requester
    |   |-- requestEnginer.py
    |   |-- __init__.py
    |-- service
    |-- spiders
        |-- __init__.py
        |-- proxySpiders
        |-- yourSpider
</pre>

* config目录下的`config.py`是项目的运行配置文件.
* db目录下的MongodbManager是初始化mongodb连接的类，model目录的`proxymodel.py`负责项目初始化时创建mongodb的database、代理ip的筛选、奖惩制度等等
* middlewares 目录是放自定义中间件 `proxyMiddleware.py`有2个职责责 1.设置请求的代理 2.处理连接超时或失败的ip；`RandomUserAgentMiddleware.py`负责设置请求头随机user-agent
* requester目录的`requestEnginer.py`负责验证爬取的代理ip有效性.
* service目录下是一些公共功能类.
* spiders目录的`proxySpiders`目录存放代理ip的爬虫项目；`yourSpider`目录是存放自定义的爬虫项目

## 使用说明

> ### 1 项目环境
* python 3.6或以上
<br/>
你需要通过 pip 安装以下依赖：

* requests 
* scrapy 
* pymongo 
* apscheduler 

> ### 2 修改配置
1.修改config目录下`config.py`文件中的mongodb连接配置 <br/>
2.在你需要代理的自定义爬虫项目里的Request方法加上`meta={'proxy':''}`参数<br/>
3.修改`EngineStar.py`里的 your_spiders_list AND 运行`EngineStar.py`即可<br/>
4.启动代理爬虫的方式: <br/>
&emsp;4.1 进入项目根目录<br/>
&emsp;4.2 chmod +x task.sh<br/>
&emsp;4.3 ./tash.sh start 启动任务脚本. 停止脚本的命令: ./task.sh stop

> ## 参考资料
https://www.osgeo.cn/scrapy/index.html<br/>
https://docs.python.org/zh-cn/3/library/index.html<br/>
https://juejin.im/post/5d3718c35188251b2569f9e8


> ## 最后

欢迎fork&star我的项目.刚写python不久.如果你有更好的建议欢迎issues或联系我
