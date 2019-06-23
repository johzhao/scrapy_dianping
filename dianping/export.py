import datetime
import logging

import pymongo
import xlwt

from dianping.settings import mongo_db_host, mongo_db_port

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def export_excel(db_name: str, collection_name: str, filepath: str):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('dianping')
    _export_title(sheet)

    client = pymongo.MongoClient(mongo_db_host, mongo_db_port)
    database = client[db_name]
    collection = database[collection_name]
    for row, record in enumerate(collection.find().sort('comments', -1), start=1):
        _export_record(sheet, row, record)

    wbk.save(filepath)


def _export_title(sheet: xlwt.Worksheet):
    sheet.write(0, 0, '商户ID')
    sheet.write(0, 1, '商户')
    sheet.write(0, 2, '商户星级')
    sheet.write(0, 3, '评论数量')
    sheet.write(0, 4, '人均消费')
    sheet.write(0, 5, '产品得分')
    sheet.write(0, 6, '环境得分')
    sheet.write(0, 7, '服务得分')
    sheet.write(0, 8, '地址')
    sheet.write(0, 9, '电话')
    sheet.write(0, 10, 'URL')


def _export_record(sheet: xlwt.Worksheet, row: int, record: dict):
    col = 0
    if '_id' in record:
        sheet.write(row, col, record['_id'])
    col += 1

    if 'name' in record:
        sheet.write(row, col, record['name'])
    col += 1

    if 'rating' in record:
        sheet.write(row, col, record['rating'])
    col += 1

    if 'comments' in record:
        sheet.write(row, col, record['comments'])
    col += 1

    if 'cost_avg' in record:
        sheet.write(row, col, record['cost_avg'])
    col += 1

    if 'product_rating' in record:
        sheet.write(row, col, record['product_rating'])
    col += 1

    if 'enviroment_rating' in record:
        sheet.write(row, col, record['enviroment_rating'])
    col += 1

    if 'service_rating' in record:
        sheet.write(row, col, record['service_rating'])
    col += 1

    if 'address' in record:
        sheet.write(row, col, record['address'])
    col += 1

    if 'phone_number' in record:
        sheet.write(row, col, record['phone_number'])
    col += 1

    if 'url' in record:
        sheet.write(row, col, record['url'])
    col += 1


def _get_date_by_time(d: int) -> str:
    return datetime.datetime.fromtimestamp(d).strftime('%Y-%m-%d')
