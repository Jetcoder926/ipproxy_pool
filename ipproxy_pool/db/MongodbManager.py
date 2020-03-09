import pymongo, logging
from ..config import config
from pymongo import errors

logger = logging.getLogger()


class mongodbManager(object):

    def __init__(self, database=None, collection=None):
        self.collection = self.mongo_client()[database][collection]

    @staticmethod
    def mongo_client():
        try:
            # PyMongo不是fork-safe,connect= False 解决父子进程间的复制
            return pymongo.MongoClient(config.MONGODB_URI, connect=False)
        except pymongo.errors.ConnectionFailure as e:
            logger.error('无法连接 MongoDB: %s' % e)
        except pymongo.errors.ServerSelectionTimeoutError as e:
            logger.error('MongoDB 选择服务器超时: %s' % e)
        except Exception as e:
            logger.error('连接 MongoDB发生错误: %s' % e)

    def mongo_collection(self):
        return self.collection
