import re
import scrapy
from scrapy import Request
from ipproxy_pool.items import IpproxyPoolItem

types = {'高匿': 0, '匿名': 1, '透明': 2}


class xiciSpider(scrapy.Spider):
    agent = '西刺'
    name = 'xiciSpider'
    custom_settings = {

        'ITEM_PIPELINES': {
            'ipproxy_pool.pipelines.XiciProxyPipeline': 1
        },

    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'http://www.xicidaili.com/wn',
        'Content-Type': 'text/html;charset=UTF-8',
        'Host': 'www.xicidaili.com',
        'Upgrade-Insecure-Requests': '1',
    }

    def start_requests(self):
        url = 'https://www.xicidaili.com/nn/1'

        yield Request(url, headers=self.headers, meta={'dont_retry': True})

    def parse(self, response):

        item = IpproxyPoolItem()
        infos = response.xpath('//table[@id="ip_list"]/tr')

        for i, info in enumerate(infos):
            if i == 0:
                pass
            else:
                item['agent'] = self.agent
                item['country'] = info.xpath('./td[1]/img/@alt').get()
                item['ip_addr'] = info.xpath('./td[2]/text()').get()
                item['port'] = info.xpath('./td[3]/text()').get()
                item['area'] = info.xpath('./td[4]/a/text()').get()
                item['types'] = types[info.xpath('./td[5]/text()').get()]
                item['protocol'] = info.xpath('./td[6]/text()').get()
                item['speed'] = info.xpath('./td[7]/div/@title').re_first(r'[1-9]\d*.\d*|0\.\d*[1-9]\d*')
                item['time'] = info.xpath('./td[8]/div/@title').re_first(r'[1-9]\d*.\d*|0\.\d*[1-9]\d*')
                item['survival_time'] = info.xpath('./td[9]/text()').get()
                item['verify_time'] = info.xpath('./td[10]/text()').get()
                item['failures_times'] = 0
                item['score'] = 10
                yield item

        next_page_num = int(response.url[-1]) + 1
        if next_page_num <= 5:

            next_url = 'https://www.xicidaili.com/nn/' + str(next_page_num)
            yield Request(next_url, headers=self.headers, meta={'dont_retry': True})
