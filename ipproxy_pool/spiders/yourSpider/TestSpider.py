import scrapy
from scrapy import Request




class TestSpider(scrapy.Spider):
    name = 'testSpider'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'text/html;charset=UTF-8',
        'Upgrade-Insecure-Requests': '1',
    }

    def start_requests(self):
        url = 'https://www.douban.com'
        yield Request(url, headers=self.headers, dont_filter=True, meta={'proxy':''})

    def parse(self, response):

        self.logger.debug(response.text)
