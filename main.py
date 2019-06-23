import logging
import time
from functools import wraps

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from dianping.spiders.dianping_spider import DianpingSpiderSpider
from dianping.spiders.dianping_comments_spider import DianpingCommentsSpider
import dianping.export

import pymongo
from dianping.settings import mongo_db_host, mongo_db_port

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
    # process = CrawlerProcess(get_project_settings())
    # process.crawl(DianpingSpiderSpider)
    # process.start()

    # dianping.export.export_excel('scrapy', 'dianping', './shops.xls')

    # client = pymongo.MongoClient(mongo_db_host, mongo_db_port)
    # database = client['scrapy']
    # collection = database['dianping']
    # with open('./shop_ids.txt', 'w') as shop_id_file:
    #     for row, record in enumerate(collection.find({}, {'_id': 1}), start=1):
    #         shop_id_file.write(f'{record["_id"]}\n')

    process = CrawlerProcess(get_project_settings())
    process.crawl(DianpingCommentsSpider)
    process.start()
    pass


if __name__ == '__main__':
    main()
