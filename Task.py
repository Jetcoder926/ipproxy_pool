import datetime, os, logging
from logging.handlers import RotatingFileHandler
import multiprocessing
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.twisted import TwistedScheduler

from ipproxy_pool.config.config import THREADPOOL_NUM
from ipproxy_pool.db.MongodbManager import mongodbManager
from ipproxy_pool.db.model.proxymodel import proxy_operating
from ipproxy_pool.requester.requestEnginer import filter_proxy

Runnumber = 20
database = 'apscheduler_task'
collection = 'task'
explore_task_id = 'explore_proxy'
check_ip_task_id = 'check_ip'

jobstores = {

    'default': MongoDBJobStore(database=database, collection=collection, client=mongodbManager.mongo_client())
}
executors = {
    'default': ThreadPoolExecutor(THREADPOOL_NUM),
    'processpool': ProcessPoolExecutor(multiprocessing.cpu_count() * 2 + 1)

}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}


def my_listener(event):
    if event.exception:
        logging.error('任务出错 % s' % event.exception)
    else:
        logging.info('任务照常运行...')


def __check_ip_availability(proxy_list):
    import concurrent.futures
    logging.info('开始定时任务')

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADPOOL_NUM) as executor:
        future_data = {executor.submit(filter_proxy, proxy_data): proxy_data for proxy_data in proxy_list}
        for i in concurrent.futures.as_completed(future_data):
            f = future_data[i]
            proxy_ip = '%s:%s' % (f['ip_addr'], f['port'])
            try:
                data = i.result()
            except Exception as e:
                logging.error('代理ip %r 线程任务产生了错误: %s' % (f, e))
            else:
                if data is None:
                    proxy_operating().reduce_proxy_score(proxy_ip)
                    proxy_operating().plus_proxy_failure_time(proxy_ip)
                    logging.info('代理ip %s 在检查连接可以性超时或返回错误' % proxy_ip)


from twisted.internet import reactor


def __explore_proxy_task():
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.project import get_project_settings
    runner = CrawlerRunner(get_project_settings())

    from ipproxy_pool.spiders.proxySpiders.xiciSpider import xiciSpider
    from ipproxy_pool.spiders.proxySpiders.SixsixSpider import SixsixSpider
    from ipproxy_pool.spiders.proxySpiders.KuaidailiSpider import kuaidailiSpider

    for spider in [SixsixSpider, xiciSpider, kuaidailiSpider]:
        runner.crawl(spider)


def close_task():
    mongodbManager(database, collection).mongo_collection().delete_one({'_id': explore_task_id})
    mongodbManager(database, collection).mongo_collection().delete_one({'_id': check_ip_task_id})
    return


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='log/apschedulerLog.txt',
                        filemode='a')

    # https://github.com/agronholm/apscheduler/blob/master/examples/schedulers/twisted_.py
    # 为什么要搞2个实例呢. 因为检查任务不是twisted异步结构.
    scheduler = TwistedScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
    scheduler2 = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

    scheduler.add_job(__explore_proxy_task, id=explore_task_id, trigger='interval', hours=5,
                      next_run_time=datetime.datetime.now())

    scheduler2.add_job(__check_ip_availability, args=[proxy_operating().find_limit_and_delete(Runnumber), ],
                       id=check_ip_task_id,
                       trigger='interval', minutes=30)

    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler2.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler._logger = logging
    scheduler2._logger = logging

    scheduler2.start()
    scheduler.start()
    reactor.run()
