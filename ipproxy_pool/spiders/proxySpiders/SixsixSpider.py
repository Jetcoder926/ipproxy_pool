import scrapy,time
from scrapy import Request
from ipproxy_pool.items import IpproxyPoolItem

from scrapy.selector import Selector

num = 200
port = 80


class SixsixSpider(scrapy.Spider):
    name = 'sixsixSpider'
    agent = '66代理'
    custom_settings = {
        'HANDLE_NUM': num,
        'ITEM_PIPELINES': {
            'ipproxy_pool.pipelines.SixsixProxyPipeline': 1
        },
        'DOWNLOADER_MIDDLEWARES': {}
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'text/html;charset=UTF-8',
        'Host': 'www.66ip.cn',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0'
    }

    def start_requests(self):
        url = "http://www.66ip.cn/mo.php?sxb=&tqsl={0}&port={1}&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1".format(num,
                                                                                                                 port)

        yield Request(url, headers=self.headers, meta={'dont_retry': True})

    def parse(self, response):
        item = IpproxyPoolItem()
        infos = Selector(text=response.text).re(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}')

        for i, info in enumerate(infos):
            item['agent'] = self.agent
            item['ip_addr'] = infos[i]
            item['port'] = str(port)
            item['types'] = 0
            item['protocol'] = 'HTTP'
            item['country'] = 'Cn'
            item['area'] = ''
            item['speed'] = 0
            item['time'] = ''
            item['survival_time'] = ''
            item['verify_time'] = ''
            item['failures_times'] = 0
            item['score'] = 10
            item['created_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            yield item
