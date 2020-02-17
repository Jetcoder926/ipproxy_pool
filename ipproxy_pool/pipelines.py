# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import errors
import logging
from ipproxy_pool.requester import requestEnginer
from .config.config import MONGODB_PROXY_DATABASE, THREADPOOL_NUM, MONGODB_PROXY_COLLECTION


class BaseProxyPipeline(object):

    def __init__(self, handle_num=THREADPOOL_NUM):
        self.handle_num = handle_num

    def open_spider(self, spider):
        from .db.MongodbManager import mongodbManager
        self.client = mongodbManager.mongo_client()
        self.collection = mongodbManager(MONGODB_PROXY_DATABASE, MONGODB_PROXY_COLLECTION).mongo_collection()
        self.collection.create_index('ip_addr', unique=True)
        self.proxy_list = []

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.proxy_list.append(dict(item))
        if len(self.proxy_list) >= self.handle_num:
            filtered_models = requestEnginer.filter_unavailable_proxy(self.proxy_list)
            self._insert_mongo(filtered_models)
            self.proxy_list.clear()
        return item

    def _insert_mongo(self, proxy_list: list):
        if proxy_list:
            try:
                self.collection.insert_many(proxy_list)
            except errors.BulkWriteError as e:
                logging.error('出现重复的数据: %s' % e)
            except Exception as e:
                logging.error('插入mongo发生错误: %s' % e)
        else:
            pass


class XiciProxyPipeline(BaseProxyPipeline):
    def __init__(self):
        super().__init__()


class KuaidailiProxyPipeline(BaseProxyPipeline):
    def __init__(self):
        super().__init__(15)

class SixsixProxyPipeline(BaseProxyPipeline):
    def __init__(self):
        super().__init__()
