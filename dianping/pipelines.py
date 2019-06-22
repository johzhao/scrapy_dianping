import logging

import pymongo

from dianping.settings import mongo_db_host, mongo_db_port

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ScrapyDianpingPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(mongo_db_host, mongo_db_port)
        self.database = self.client['scrapy']
        self.collection = self.database['dianping']

    def process_item(self, item, spider):
        data = dict(item)
        self.collection.update({'_id':data['_id']}, data, True)
        return item
