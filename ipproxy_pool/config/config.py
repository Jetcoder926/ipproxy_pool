import logging, datetime


from ..service.log import get_logger
def get_log_config():
    # Log 文件名
    LOG_STORE_NAME = 'proxy_{}.txt'.format(
        datetime.datetime.now().strftime("%Y%m%d"))

    get_logger(filename=LOG_STORE_NAME).logger()
    # 将 requests的日志级别设成 WARNING
    LOG_LEVEL = logging.WARNING
    logging.getLogger("requests").setLevel(LOG_LEVEL)


MONGODB_URI = 'mongodb://root:aa123456@127.0.0.1:17017/'
MONGODB_PROXY_DATABASE = 'proxy'
MONGODB_PROXY_COLLECTION = 'proxy_list'

MONGODB_KAFKA_DATABASE = 'kafka'
MONGODB_KAFKA_COLLECTION = '_offset'
# 冷启动的判断标准--库中代理ip的数量
# COLD_START_MIN_REQUIREMENT = 1000



# 验证代理地址的网站
Validated_url = 'http://httpbin.org/get'



# 验证代理地址的线程池的总数
THREADPOOL_NUM = 50


