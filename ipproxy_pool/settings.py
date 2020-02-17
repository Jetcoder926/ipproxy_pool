# -*- coding: utf-8 -*-

# Scrapy settings for ipproxy_pool project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ipproxy_pool'

SPIDER_MODULES = ['ipproxy_pool.spiders']
NEWSPIDER_MODULE = 'ipproxy_pool.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ipproxy_pool (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Scrapy下载程序将执行的最大并发（即同时）请求数
CONCURRENT_REQUESTS = 32

# 下载者从同一网站下载连续页面之前应等待的时间（以秒计）。这可以用来限制爬行速度，以避免对服务器造成太大的冲击。支持十进制数。例子
DOWNLOAD_DELAY = 0.25
# 将对任何单个域执行的最大并发（即同时）请求数
CONCURRENT_REQUESTS_PER_DOMAIN = 10
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'text/html;charset=UTF-8',
    'Cache-Control': 'no-cache',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ipproxy_pool.middlewares.IpproxyPoolSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html



DOWNLOADER_MIDDLEWARES = {

    # 设置 User-Agent
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'ipproxy_pool.middlewares.RandomUserAgentMiddleware.RandomUserAgentMiddleware': 125,

    # 设置代理
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'ipproxy_pool.middlewares.proxyMiddleware.SetProxyMiddleware': 200,

    # 设置自定义重连中间件
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'ipproxy_pool.middlewares.proxyMiddleware.MyRetryMiddleware': 543,
}
# HTTPERROR_ALLOWED_CODES = [403, 404, 503]
DOWNLOAD_TIMEOUT = 3
RETRY_ENABLED = True
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 404, 403]
RETRY_TIMES = 2
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'ipproxy_pool.pipelines.IpproxyPoolPipeline': 300,
#}

# AutoThrottle 算法根据以下规则调整下载延迟：
#
# 蜘蛛总是以下载延迟开始 AUTOTHROTTLE_START_DELAY ；
# 当收到响应时，目标下载延迟计算为 latency / N 在哪里？ latency 是响应的延迟，并且 N 是 AUTOTHROTTLE_TARGET_CONCURRENCY .
# 下一个请求的下载延迟设置为上一个下载延迟和目标下载延迟的平均值；
# 不允许非200响应的延迟减少延迟；
# 下载延迟不能小于 DOWNLOAD_DELAY 或大于 AUTOTHROTTLE_MAX_DELAY

#启用AutoThrottle 扩展。
AUTOTHROTTLE_ENABLED = True
# 初始下载延迟（秒）
AUTOTHROTTLE_START_DELAY = 1
# 在高延迟情况下设置的最大下载延迟（秒）
AUTOTHROTTLE_MAX_DELAY = 3
# Scrapy的平均请求数应与远程网站并行发送。
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# 启用 AutoThrottle 调试模式，该模式将显示收到的每个响应的统计信息，以便您可以看到如何实时调整节流参数
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
