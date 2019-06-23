import logging

import pymongo

from dianping.settings import mongo_db_host, mongo_db_port
from dianping.items import DianpingShopItem, DianpingReviewItem

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ScrapyDianpingPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(mongo_db_host, mongo_db_port)
        self.database = self.client['scrapy']
        self.collection = self.database['dianping']
        self.review_collection = self.database['review']

    def process_item(self, item, spider):
        if isinstance(item, DianpingShopItem):
            data = dict(item)
            self.collection.update({'_id':data['_id']}, data, True)
        elif isinstance(item, DianpingReviewItem):
            data = dict(item)
            self.review_collection.insert(data)
        return item
