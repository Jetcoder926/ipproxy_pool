# ipproxy_pool
#### 隔离在家太无聊催生了这个项目...
#### 很多网站都会有基本的反爬行机制.那么反ban措施之一就是搞个ip代理池了.网上有很多收费的代理ip服务(luminati、oxylabs等等).
#### 项目提供爬取几个免费代理网站的代理Ip(包括西刺代理、快代理、66代理)


>## 项目说明

项目采用mongodb作为database,&emsp;kafka作为MQ系统

### 特点
* 多线程消费MQ,采用database管理MQ位移值
* 异步爬取N个代理网站,多线程检查代理ip可用性(积分淘汰机制)及存储代理ip,均为后台任务式执行
* 同一时间运行多个自定义爬虫
* 单线程爬取1000条数据时间大概在2秒内(理论值,5M带宽的机子)

> ## 使用说明

### 1 项目环境
* java 1.8.0
* python 3.6或以上
* mongdb 4.2.3
* zookeeper 3.5.6
* kafka 2.12-2.4.0
<br/>

你需要通过 pip 安装以下依赖：
* kafka-python
* requests 
* scrapy 
* pymongo 
* apscheduler 

### 2 配置
1.修改config目录下`config.py`,`kafka_config.py`文件中的mongodb连接配置 <br/>
2.在你需要代理的自定义爬虫项目里的Request方法加上`meta={'proxy':''}`参数<br/>

### 3启动代理ip爬虫
1 进入项目根目录<br/>
2 chmod +x task.sh<br/>
3 `./tash.sh start` 启动任务脚本. 停止脚本的命令: `./task.sh stop`<br>

### 4启动自定义爬虫
修改`EngineStar.py`里的 your_spiders_list 并运行`EngineStar.py`即可<br>
<br>
>## 参考资料
https://www.osgeo.cn/scrapy/index.html<br/>
https://docs.python.org/zh-cn/3/library/index.html<br/>
https://juejin.im/post/5d3718c35188251b2569f9e8
http://kafka.apachecn.org/quickstart.html
<br>

> ## 最后

欢迎fork&star我的项目.刚写python不久.如果你有更好的建议欢迎issues或联系我
