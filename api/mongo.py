# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/8 上午9:56
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : mongo.py
# @Software: PyCharm
# @class : mongoDB -> Data is stored

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import hashlib
import time


class Mongo(object):

    def __init__(self):
        self.mongo = MongoClient('mongodb://admin:Always@Latent==1@192.168.0.16', 27017, )
        self.db = self.mongo['ods_elec_wanbang_api']
        # table
        self.goods_list = self.db['ods_elec_goods_list']
        self.goods_details = self.db['ods_elec_goods_details']

    def mongo_get_tables(self):
        tables = {'table_list': self.goods_list,
                  'table_details': self.goods_details
                  }
        return tables

    @classmethod
    def mongo_index(cls, tableName, indexName):
        try:
            tableName.create_index([(indexName, 1)], unique=True)
        except DuplicateKeyError:
            pass

    @classmethod
    def mongo_insert(cls, tableName, data, keyword, platform, page):
        # add to keyword/_id/request_time/
        data['keyword'] = keyword
        data['request_date'] = time.strftime('%Y-%m-%d')
        data['platform'] = platform
        data['page'] = page
        data['_id'] = hashlib.md5(bytes(data['title'] + str(data['num_iid']) +
                                        str(data['sales']) + str(data['request_date'] +
                                                                 str(data['platform'])),
                                        encoding='utf-8')).hexdigest()

        try:
            tableName.insert(data)
        except DuplicateKeyError:
            print('==>数据更新')
            tableName.update({"_id": data['_id']}, data)

    """
    通过时间和关键词来查询商品列表的num_iid
    """

    @classmethod
    def mongo_query(cls, tableName, keyword, requestDate):
        pass
