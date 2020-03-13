# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
from kafka.errors import KafkaError
from ipproxy_pool.service.kafka_python import Product
from .config.config import THREADPOOL_NUM, KAFKA_PROXY_CONSUMER_TOPIC


class ProxyPipeline(object):

    def __init__(self, client_id=None, handle_num=THREADPOOL_NUM, logger=None, msg_key=None):
        self.handle_num = handle_num
        self.logger = logger
        self.msg_key = msg_key
        self.client_id = client_id

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            client_id=crawler.settings.get('CLIENT_ID'),
            handle_num=crawler.settings.get('HANDLE_NUM'),
            logger=logging.getLogger(),
            msg_key=bytes(crawler.settings.get('MSG_KEY', 'key1'), 'ascii'),
        )

    def open_spider(self, spider):
        self.product = Product(value_serializer=lambda m: json.dumps(m).encode('ascii')).set_clientId(self.client_id)

    def close_spider(self, spider):
        self.product.engine.close()

    def process_item(self, item, spider):

        pid = spider.crawler.settings.get('PARTITION_ID')   # 将消息发送至指定分区.一般情况kafka自动分配即可
        self.product.product_send(KAFKA_PROXY_CONSUMER_TOPIC, key=self.msg_key, value=dict(item),
                                  errorCall=lambda : self.logger.error(
                                      'producter run failed in topic:%s , key:%s , value: %s' % (
                                          KAFKA_PROXY_CONSUMER_TOPIC, self.msg_key, dict(item))), partition=pid)

        return item
