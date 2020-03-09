# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
from ipproxy_pool.service.kafka_python import Product
from .config.config import THREADPOOL_NUM



class ProxyPipeline(object):

    def __init__(self, handle_num=THREADPOOL_NUM, logger=None, msg_key=None):
        self.handle_num = handle_num
        self.logger = logger
        self.msg_key = msg_key

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            handle_num=crawler.settings.get('HANDLE_NUM'),
            logger=logging.getLogger(),
            msg_key=bytes(crawler.settings.get('MSG_KEY', 'key1'), 'ascii'),
        )

    def open_spider(self, spider):

        self.kafka_topic = 'proxy_topic'
        self.product = Product(value_serializer=lambda m: json.dumps(m).encode('ascii'))

    def close_spider(self, spider):
        self.product.close()

    def process_item(self, item, spider):
        self.product.product_send(self.kafka_topic, key=self.msg_key, value=dict(item))

        return item
