from scrapy.crawler import CrawlerProcess
from ipproxy_pool.config.config import get_log_config
from scrapy.utils.project import get_project_settings
from ipproxy_pool.spiders.yourSpider.TestSpider import TestSpider
settings = get_project_settings()


def start_spider():
    process = CrawlerProcess(settings)
    for spider in your_spiders_list:
        process.crawl(spider)
    process.start()


if __name__ == "__main__":
    get_log_config()
    your_spiders_list = [TestSpider, ]

    start_spider()
