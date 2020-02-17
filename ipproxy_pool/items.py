# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IpproxyPoolItem(scrapy.Item):
    agent = scrapy.Field()
    country = scrapy.Field()
    ip_addr = scrapy.Field()
    port = scrapy.Field()
    area = scrapy.Field()
    types = scrapy.Field()
    protocol = scrapy.Field()
    speed = scrapy.Field()
    time = scrapy.Field()
    survival_time = scrapy.Field()
    verify_time = scrapy.Field()
    failures_times = scrapy.Field()
    score = scrapy.Field()



