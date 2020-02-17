from ..MongodbManager import mongodbManager
from ipproxy_pool.config.config import MONGODB_PROXY_DATABASE
from ipproxy_pool.config.config import MONGODB_PROXY_COLLECTION
from ipproxy_pool.config.config import THREADPOOL_NUM
import logging

class ProxyModel(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.mongodbManager = mongodbManager(MONGODB_PROXY_DATABASE, MONGODB_PROXY_COLLECTION)
        self.mongodbCollection  = self.mongodbManager.mongo_collection()

    def create_database(self): pass

    def statistics_proxy(self):
        return self.mongodbCollection.count()

    def plus_proxy_failure_time(self, proxy_ip):
        ip = proxy_ip.split(':')[0]
        port = proxy_ip.split(':')[1]
        try:
            self.mongodbCollection.find_and_modify({'ip_addr': ip, 'port': port}, update={"$inc": {'failures_times': 1}},
                                                   new=True)
        except Exception as e:
            logging.error('代理ip: %s 添加失败次数失败, 原因: %s' % (ip, e))

    def choice_proxy_ip(self):
        data = self.select_random_proxy(1)
        if data:
            return "%s://%s:%s" % (data['protocol'].lower(),data['ip_addr'],data['port'])
        else:
            return ''

    def select_random_proxy(self, num):
        data = list(self.mongodbCollection.aggregate([{"$match": {"failures_times": {"$lt": 2},"score":{"$gt":6}}}, {"$sample": {'size': 1}}], allowDiskUse=True))
        if data:
            return data if num > 1 else data[0]
        else:
            return None

    def reduce_proxy_score(self, proxy_ip, score= -1):
        ip = proxy_ip.split(':')[0]
        port = proxy_ip.split(':')[1]
        try:
            self.mongodbCollection.find_and_modify({'ip_addr':ip,'port':port},update={ "$inc": { "score": score} }, new=True)
        except Exception as e:
            logging.error('代理ip: %s 减分失败, 原因: %s' % (ip,e))

    def delete_proxy(self,proxy_ip):
        ip = proxy_ip.split(':')[0]
        port = proxy_ip.split(':')[1]

        try:
            self.mongodbCollection.delete_one({'ip_addr':ip,'port':port})
        except Exception as e:
            logging.error('代理ip: %s 删除失败, 原因: %s' % (ip, e))

    def find_limit(self, limit = THREADPOOL_NUM):
        return list(self.mongodbCollection.find().limit(limit))


proxy_object = ProxyModel()


def proxy_operating():
    return proxy_object
