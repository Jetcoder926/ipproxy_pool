import datetime, logging
import multiprocessing
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from ipproxy_pool.config.config import THREADPOOL_NUM
from ipproxy_pool.db.MongodbManager import mongodbManager
from ipproxy_pool.db.model.proxymodel import proxy_operating
from ipproxy_pool.requester.requestEnginer import filter_proxy
from ipproxy_pool.service.log import get_logger

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


@scheduler.scheduled_job('interval', hours=3, id=explore_task_id, next_run_time=datetime.datetime.now())
def run_proxy_task():
    p = multiprocessing.Process(target=__explore_proxy_task)
    p.start()


@scheduler.scheduled_job('interval', args=[proxy_operating().find_limit_and_delete(limit=THREADPOOL_NUM), ], hours=1,
                         id=check_ip_task_id)
def __check_ip_availability(proxy_list):
    import concurrent.futures
    logger.info('开始定时任务')
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
                        logger.info('代理ip %s 在检查连接可以性超时或返回错误' % proxy_ip)
    else:
        logger.error('检查任务失败,ip代理池为空')


def close_task():
    mongodbManager(database, collection).mongo_collection().delete_one({'_id': explore_task_id})
    mongodbManager(database, collection).mongo_collection().delete_one({'_id': check_ip_task_id})
    return


if __name__ == '__main__':
    logger = get_logger(filename='apscheduler-task.txt').logger()

    scheduler._logger = logger

    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    scheduler.start()
