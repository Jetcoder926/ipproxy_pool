from scrapy.crawler import CrawlerProcess
from ipproxy_pool.config.config import get_log_config
from scrapy.utils.project import get_project_settings
from multiprocessing import Process
from ipproxy_pool.spiders.proxySpiders.xiciSpider import xiciSpider
from ipproxy_pool.spiders.proxySpiders.SixsixSpider import SixsixSpider
from ipproxy_pool.spiders.proxySpiders.KuaidailiSpider import kuaidailiSpider
from ipproxy_pool.spiders.yourSpider.TestSpider import TestSpider
# from ipproxy_pool.requester.requestEnginer import check_proxy_ip_task
settings = get_project_settings()


def start_spider(spider_list):
    process = CrawlerProcess(settings)
    for spider in spider_list:
        process.crawl(spider)
    process.start()


if __name__ == "__main__":
    get_log_config()
    proxy_spiders_list = [SixsixSpider, xiciSpider, kuaidailiSpider]

    your_spiders_list = [TestSpider, ]
    #
    proxySpiders = Process(target=start_spider, args=(proxy_spiders_list,))
    yourSpiders = Process(target=start_spider, args=(your_spiders_list,))
    proxySpiders.start()
    proxySpiders.join()
    yourSpiders.start()
