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
from urllib import parse

class Mongo(object):

    def __init__(self):
        mongo_user = parse.quote_plus('admin')
        mongo_pass = parse.quote_plus('Always@Latent==1')
        self.mongo = MongoClient(f'mongodb://{mongo_user}:{mongo_pass}@192.168.0.16', 27017, )
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

    """
    api-search数据插入
    """

    @classmethod
    def mongo_insert(cls, tableName, data, keyword, platform, page):
        # add to keyword/_id/request_time/
        data['keyword'] = keyword
        data['request_date'] = time.strftime('%Y-%m-%d')
        data['platform'] = platform
        data['page'] = page
        try:
            data['_id'] = hashlib.md5(bytes(data['title'] + str(data['num_iid']) +
                                            str(data['sales']) + str(data['request_date'] +
                                                                     str(data['platform'])),
                                            encoding='utf-8')).hexdigest()
        except Exception:
            print(data)
        try:
            tableName.insert(data)
        except DuplicateKeyError:
            print('==>数据更新')
            tableName.update({"_id": data['_id']}, data)

    """
    通过时间/页面来查询商品列表的num_iid
    """

    @classmethod
    def mongo_query(cls, tableName, startDate, endDate, start_page, end_page, platform):
        # 日期条件筛选
        match = {
            "$match": {"$and": [{"page": {"$gt": start_page,
                                          "$lt": end_page}},
                                {"request_date": {"$gte": startDate,
                                                  "$lte": endDate}},
                                {"platform": platform}
                                ]
                       }
        }

        data = tableName.aggregate([match])
        return data

    # ===>4. 验证list和detail的数据对应的完整性 ----> 返回完成的数据和未完成数据的id
    # ===>注意！聚合后，仅返回public[0]的数据，故传入日期的时间要分清楚月底和月初
    @classmethod
    def mongo_data_describe(cls, tableName, startDate, endDate, platform, keyword, start_page, end_page, ):
        unfinished_data = []
        finished_data = []
        lookup = {'$lookup': {'from': 'ods_elec_goods_details',
                              'localField': 'num_iid',
                              'foreignField': 'num_iid',
                              'as': 'public'
                              }
                  }
        match = {
            "$match": {"$and": [{"page": {"$gte": start_page,
                                          "$lte": end_page}},
                                {"request_date": {"$gte": startDate,
                                                  "$lte": endDate}},
                                {"platform": platform},
                                {"keyword": keyword},
                                ]
                       }
        }
        project = {
            "$project": {
                "_id": 0,
                "pic_url": 0,
                "public": {
                    "_id": 0,
                    "num_iid": 0,
                    "price": 0,
                    "total_price": 0,
                    "suggestive_price": 0,
                    "orginal_price": 0,
                    "created_time": 0,
                    "modified_time": 0,
                    "delist_time": 0,
                    "desc": 0,
                    "desc_short": 0,
                    "item_weight": 0,
                    "item_size": 0,
                    "post_fee": 0,
                    "express_fee": 0,
                    "ems_fee": 0,
                    "shipping_to": 0,
                    "is_virtual": 0,
                    "sample_id": 0,
                    "property_alias": 0,
                    "total_sold": 0,
                    "seller_id": 0,
                    "error": 0,
                    "has_discount": 0,
                    "data_from": 0,
                    "shop_item": 0,
                    "relate_items": 0,
                    "url_log": 0,
                },


            }
        }
        # 从表过滤
        match_slave = {
            "$match": {"public.request_date": {"$gte": '2021-06-01',
                                               "$lte": '2021-06-30'}
                       }
        }

        pipelines = [match, lookup, project]
        data = tableName.aggregate(pipelines)
        list(map(lambda x: finished_data.append(x) if x['public'] else unfinished_data.append(x), data))
        finished_count = len(finished_data)
        unfinished_count = len(unfinished_data)
        describe_info = {'count': finished_count + unfinished_count,
                         'finished_count': finished_count,
                         'unfinished_count': unfinished_count,
                         'finished_item': finished_data,
                         'unfinished_item': unfinished_data,
                         }
        print("=====================================================================\n"
              f"【日期】: {startDate}----{endDate}\n"
              f"【页面】: {start_page}----{end_page}\n"
              f"【平台】: {platform}\n"
              f"【类别】: {keyword}\n"
              f"【总共】: {describe_info['count']}\n"
              f"【完整数据】: {describe_info['finished_count']}\n"
              f"【详情缺失数据】: {describe_info['unfinished_count']}\n"
              "=====================================================================")
        return describe_info
