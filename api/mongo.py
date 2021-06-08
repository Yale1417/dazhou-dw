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


class mongo(object):

    def __init__(self):
        self.mongo = MongoClient('mongodb://admin:123456@192.168.0.16', 27017, )
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
    def mongo_insert(cls, tableName, data):
        try:
            tableName.insert(data)
        except DuplicateKeyError:
            tableName.update({"_id": data['_id']}, data)
