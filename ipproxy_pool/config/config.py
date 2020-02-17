import logging, datetime
def get_log_config():
    # 将 requests的日志级别设成 WARNING
    LOG_LEVEL = logging.WARNING
    logging.getLogger("requests").setLevel(LOG_LEVEL)

    # Log 文件名
    LOG_STORE_NAME = 'proxy_{}.txt'.format(
        datetime.datetime.now().strftime("%Y%m%d"))

    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s %(filename)s[line:%(lineno)d]/%(levelname)s/  %(message)s',
        datefmt='%Y-%b-%d',
        filename='./log/' + LOG_STORE_NAME,
        filemode='w')

MONGODB_URI = 'mongodb://root:aa123456@127.0.0.1:17017/'
MONGODB_PROXY_DATABASE = 'proxy'
MONGODB_PROXY_COLLECTION = 'proxy_list'

# 冷启动的判断标准--库中代理ip的数量
# COLD_START_MIN_REQUIREMENT = 1000

# 验证代理地址的线程池的总数
THREADPOOL_NUM = 50

# 验证代理地址的网站
Validated_url = 'http://httpbin.org/get'


