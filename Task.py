import datetime, logging
import concurrent.futures
import multiprocessing
import json
from threading import Thread
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from ipproxy_pool.config.config import THREADPOOL_NUM, MONGODB_KAFKA_PROXY_DATABASE, MONGODB_KAFKA_PROXY_COLLECTION, \
    KAFKA_PROXY_CONSUMER_TOPIC, CHECK_CONSUMER_PROXY_NOW
from ipproxy_pool.db.MongodbManager import mongodbManager
from ipproxy_pool.db.model.proxymodel import proxy_operating
from ipproxy_pool.requester.requestEnginer import filter_proxy, filter_unavailable_proxy
from ipproxy_pool.service.log import get_logger
from ipproxy_pool.service.kafka_python import Consumer
from pymongo import errors

database = 'apscheduler_task'
collection = 'task'
explore_task_id = 'explore_proxy'
check_ip_task_id = 'check_ip'
consumer_topic_task_id = 'consumer_topic'

jobstores = {
    'default': MongoDBJobStore(database=database, collection=collection, client=mongodbManager.mongo_client())
}
executors = {
    'default': ThreadPoolExecutor(THREADPOOL_NUM),
    'processpool': ProcessPoolExecutor(multiprocessing.cpu_count() * 2 + 1)

}

scheduler = BlockingScheduler(jobstores=jobstores)


def my_listener(event):
    if event.exception:
        logging.error('任务出错 % s' % event.exception)
    else:
        logging.info('任务照常运行...')


from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings


def __explore_proxy_task():
    from ipproxy_pool.spiders.proxySpiders.xiciSpider import xiciSpider
    from ipproxy_pool.spiders.proxySpiders.SixsixSpider import SixsixSpider
    from ipproxy_pool.spiders.proxySpiders.KuaidailiSpider import kuaidailiSpider
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    for spider in [SixsixSpider, xiciSpider, kuaidailiSpider]:
        runner.crawl(spider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


@scheduler.scheduled_job('interval', days=1, id=explore_task_id, next_run_time=datetime.datetime.now())
def run_proxy_task():
    p = multiprocessing.Process(target=__explore_proxy_task)
    p.start()


@scheduler.scheduled_job('cron', args=[proxy_operating().find_limit_and_delete(limit=THREADPOOL_NUM), ],
                         day_of_week='mon-fri', hour=5, minute=30, end_date='2029-12-30',
                         id=check_ip_task_id)
def __check_ip_availability(proxy_list):
    logger.info('开始检查代理可用性任务')
    if proxy_list:
        with concurrent.futures.ThreadPoolExecutor(max_workers=THREADPOOL_NUM) as executor:
            future_data = {executor.submit(filter_proxy, proxy_data): proxy_data for proxy_data in proxy_list}
            for i in concurrent.futures.as_completed(future_data):
                f = future_data[i]
                proxy_ip = '%s:%s' % (f['ip_addr'], f['port'])
                try:
                    data = i.result()
                except Exception as e:
                    logger.error('代理ip %r 线程任务产生了错误: %s' % (f, e))
                else:
                    if data is None:
                        proxy_operating().reduce_proxy_score(proxy_ip)
                        proxy_operating().plus_proxy_failure_time(proxy_ip)
                        logger.warning('代理ip %s 在检查连接可以性超时或返回错误' % proxy_ip)
    else:
        logger.error('检查任务失败,ip代理池为空')


@scheduler.scheduled_job('interval', days=1, id=consumer_topic_task_id,
                         next_run_time=datetime.datetime.now() + datetime.timedelta(minutes=1))
def consumer_topic():
    CP().run_consumer()


thread_proxy_list = []


class CP(object):
    threads = []

    def __init__(self):
        self.client = mongodbManager.mongo_client()
        self.collection = mongodbManager(MONGODB_KAFKA_PROXY_DATABASE,
                                         MONGODB_KAFKA_PROXY_COLLECTION).mongo_collection()
        self.collection.create_index('ip_addr', unique=True)
        self.topic = KAFKA_PROXY_CONSUMER_TOPIC
        self.partitions = Consumer().engine.partitions_for_topic(self.topic)  # topic的分区数:list
        self.group_id = 'ap_task'
        self.Consumer = Consumer(group_id=self.group_id,
                                 consumer_timeout_ms=50,
                                 value_deserializer=lambda m: json.loads(m.decode('ascii')))

    def run_consumer(self):

        for p in self.partitions:
            try:
                t = Thread(target=self.consumer_topic,
                           args=(
                               [{"topic": self.topic, "partition": p,
                                 "thread_id": "threadID_%s" % p}]))
                t.start()
                t.join()

                if CHECK_CONSUMER_PROXY_NOW:
                    proxy_list = filter_unavailable_proxy(thread_proxy_list, workers=len(thread_proxy_list))
                else:
                    proxy_list = thread_proxy_list
                logger.warning(proxy_list)
                self._insert_mongo(proxy_lists=proxy_list)
            except:
                logger.error(
                    "Error: failed to run consumer thread in tid: %s,topic:%s,partition:%s" % (p, self.topic, p))

    def consumer_topic(self, topics_partition: dict):

        thread_proxy_list.clear()

        messages = self.Consumer.set_clientId(topics_partition['thread_id']).assign_partition([topics_partition])

        c = messages.topic_consumer()
        while True:
            for v in c:
                messages.commit_offset(group_id=self.group_id, topic=v.topic, partition=v.partition,
                                       offset=v.offset)
                value = v.value
                # 多线程消费排序问题.根据timestamp排序
                value.update({'timestamp': v.timestamp, "offset": v.offset})
                thread_proxy_list.append(value)

            return thread_proxy_list

    def _insert_mongo(self, proxy_lists: list):
        if proxy_lists:
            try:
                self.collection.insert_many(proxy_lists)
            except errors.BulkWriteError as e:
                logger.error('出现重复的数据: %s' % e)
            except Exception as e:
                logger.error('插入mongo发生错误: %s' % e)
        else:
            pass


def close_task():
    for i in [explore_task_id, check_ip_task_id, consumer_topic_task_id]:
        mongodbManager(database, collection).mongo_collection().delete_one({'_id': i})

    return


if __name__ == '__main__':
    logger = get_logger(filename='apscheduler-task.txt').logger()

    scheduler._logger = logger

    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    scheduler.start()
