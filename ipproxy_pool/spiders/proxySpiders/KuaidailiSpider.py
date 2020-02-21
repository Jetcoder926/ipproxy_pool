import re
import scrapy
from scrapy import Request
from ipproxy_pool.items import IpproxyPoolItem

types = {'高匿名': 0, '匿名': 1, '透明': 2}



class kuaidailiSpider(scrapy.Spider):
    name = 'kuaidailiSpider'
    agent = '快代理'
    custom_settings = {

        'ITEM_PIPELINES': {
            'ipproxy_pool.pipelines.KuaidailiProxyPipeline': 1
        },

    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'text/html;charset=UTF-8',
        'Host': 'www.kuaidaili.com',
        'Upgrade-Insecure-Requests': '1',
        'Connection':'keep-alive',
        'Cache-Control': 'max-age=0'
    }

    def start_requests(self):
        url = 'https://www.kuaidaili.com/free/inha/1'

        yield Request(url, headers=self.headers, meta={'dont_retry': True})

    def parse(self, response):

        item = IpproxyPoolItem()
        infos = response.xpath('//div[@id="list"]/table/tbody/tr')

        for info in infos:
            item['agent'] = self.agent
            item['ip_addr'] = info.xpath('./td[1]/text()').get()
            item['port'] = info.xpath('./td[2]/text()').get()

            item['types'] = types[info.xpath('./td[3]/text()').get()]
            item['protocol'] = info.xpath('./td[4]/text()').get()
            item['country'] = 'Cn'
            item['area'] = info.xpath('./td[5]/text()').get()

            item['speed'] = info.xpath('./td[6]/text()').re_first(r'[1-9]\d*')
            item['time'] = ''
            item['survival_time'] = ''
            item['verify_time'] = info.xpath('./td[7]/text()').get()
            item['failures_times'] = 0
            item['score'] = 10
            yield item
        #
        next_page_num = int(response.url[-1]) + 1
        if next_page_num <= 5:
            next_url = 'https://www.kuaidaili.com/free/inha/' + str(next_page_num)
            yield Request(next_url, headers=self.headers, meta={'dont_retry': True})
