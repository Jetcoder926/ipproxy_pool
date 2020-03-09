import re
from xml import etree

import scrapy, json
from scrapy import Request

types = {'高匿': 0, '匿名': 1, '透明': 2}


class TestSpider(scrapy.Spider):
    name = 'testSpider'

    custom_settings = {

        'ITEM_PIPELINES': {
            'ipproxy_pool.pipelines.TestPipeline': 1
        },
        'DOWNLOADER_MIDDLEWARES':{}
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Referer': 'http://www.xicidaili.com/wt/1',
        'Content-Type': 'text/html;charset=UTF-8',
        'Upgrade-Insecure-Requests': '1',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'http://47.107.153.69:804/toutiao.html'
        yield Request(url, headers=self.headers, dont_filter=True, meta={'proxy':''})

    def parse(self, response):
        # selector = etree.HTML(response.text)
        yield response.text
        # item = XiciProxyItem()
        # infos = response.xpath('//table[@id="ip_list"]/tr')
        #
        # for i, info in enumerate(infos):
        #     if i == 0:
        #         pass
        #     else:
        #         item['country'] = info.xpath('./td[1]/img/@alt').get()
        #         item['ip_addr'] = info.xpath('./td[2]/text()').get()
        #         item['port'] = info.xpath('./td[3]/text()').get()
        #         item['area'] = info.xpath('./td[4]/a/text()').get()
        #         item['types'] = types[info.xpath('./td[5]/text()').get()]
        #         item['protocol'] = info.xpath('./td[6]/text()').get()
        #         item['speed'] = info.xpath('./td[7]/div/@title').re_first(r'[1-9]\d*.\d*|0\.\d*[1-9]\d*')
        #         item['time'] = info.xpath('./td[8]/div/@title').re_first(r'[1-9]\d*.\d*|0\.\d*[1-9]\d*')
        #         item['survival_time'] = info.xpath('./td[9]/text()').get()
        #         item['verify_time'] = info.xpath('./td[10]/text()').get()
        #         item['failures_times'] = 0
        #         item['score'] = 10
        #         yield item
