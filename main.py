import logging
import time
from functools import wraps

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from dianping.spiders.dianping_spider import DianpingSpiderSpider

logging.basicConfig(level=logging.INFO)


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        begin = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logging.info(f'The function {func.__name__} cost {end - begin} seconds.')
        return result

    return wrapper


@timethis
def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(DianpingSpiderSpider)
    process.start()
    # export.export_excel('course', 'icourse163', './export.xlsx')


if __name__ == '__main__':
    main()
