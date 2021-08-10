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
        self.goods_comments = self.db['ods_elec_goods_comments']

    def mongo_get_tables(self):
        tables = {'table_list': self.goods_list,
                  'table_details': self.goods_details,
                  'table_comments': self.goods_comments
                  }
        return tables

    # 1.输入数据库、表名后获取该表
    def mongo_get_table_public(self, databaseName, collectionName):
        return self.mongo[databaseName][collectionName]


    @classmethod
    def mongo_index(cls, tableName, indexName):
        try:
            tableName.create_index([(indexName, 1)], unique=True)
        except DuplicateKeyError:
            pass

    """
        数据插入 -->_id 由tuple 合并
    """

    @classmethod
    def mongo_insert(cls, tableName, data, keyword, platform, page, id_tuple: tuple):
        # add to keyword/_id/request_time/
        data['keyword'] = keyword
        data['platform'] = platform
        data['page'] = page
        # _id 规则:tuple + request_date  ===>md5
        # 元组拆出并拼接
        id_str = ''.join(list(map(lambda x: str(x), id_tuple)))
        try:
            data['_id'] = hashlib.md5(bytes(id_str, encoding='utf-8')).hexdigest()
        except Exception as e:
            print(e)
            print(data)
        try:
            tableName.insert(data)
        except DuplicateKeyError:
            print('==>数据重复')
            # tableName.update({"_id": data['_id']}, data)

    """
    通过时间/页面来查询商品列表的num_iid
    """

    @classmethod
    def mongo_query(cls, tableName, startDate, endDate, platform, keyword):
        # 日期条件筛选
        match = {
            "$match": {"$and": [{"request_date": {"$gte": startDate,
                                                  "$lte": endDate}},
                                {"platform": platform},
                                {'keyword': keyword}
                                ]
                       }
        }
        data = tableName.aggregate([match])
        return data

    # ===>4. 验证list和detail的数据对应的完整性 ----> 返回完成的数据和未完成数据的id
    # ===>注意！聚合后，仅返回public[0]的数据，故传入日期的时间要分清楚月底和月初
    # ====>【2021/07/30】 添加 ---> return osd_list
    @classmethod
    def mongo_data_describe(cls, tableName, startDate, endDate, platform, keyword, isCustom=False):
        # 监听查询时间
        mongo_start_time = time.time()
        unfinished_data = []
        finished_data = []
        ods_list = []

        lookup = {'$lookup': {'from': 'ods_elec_goods_details',
                              'localField': 'num_iid',
                              'foreignField': 'num_iid',
                              'as': 'public'
                              }
                  }
        match = {
            "$match": {"$and": [
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
        # public 拆解
        unwind = {
            '$unwind': "$public"
        }

        # 从表过滤----> 自定义设置

        if isCustom:
            new_startDate = input('===> 请输入初始日期：\n')
            new_endDate = input('===> 请输入结束日期：\n')
            match_slave = {
                "$match": {"public.request_date": {"$gte": new_startDate,
                                                   "$lte": new_endDate}
                           }
            }
        else:
            match_slave = {
                "$match": {"public.request_date": {"$gte": startDate,
                                                   "$lte": endDate}
                           }
            }

        # 匹配源数据中列表数据
        ods_list_match = {"$and": [{"request_date": {"$gte": startDate, "$lte": endDate}},
                                   {"platform": platform},
                                   {"keyword": keyword},
                                   ]
                          }
        pipelines = [match, lookup, unwind, match_slave, project]
        data = tableName.aggregate(pipelines)
        list_count = tableName.count(ods_list_match)
        ods_data = tableName.find(ods_list_match)
        # 商品列表数据集合
        list(map(lambda x: ods_list.append(x),ods_data))
        # 对应的商品列表数据集合
        list(map(lambda x: finished_data.append(x) if x['public'] else unfinished_data.append(x), data))
        finished_count = len(finished_data)
        unfinished_count = len(unfinished_data)
        # 查询时间
        mongo_end_time = time.time()-mongo_start_time
        describe_info = {'count': finished_count + unfinished_count,
                         'finished_count': finished_count,
                         'unfinished_count': unfinished_count,
                         'finished_item': finished_data,
                         'unfinished_item': unfinished_data,
                         'ods_list': ods_list,
                         }

        print("=====================================================================\n"
              f"【查询时间】: {mongo_end_time}\n"
              f"【日期】: {startDate}----{endDate}\n"
              f"【平台】: {platform}\n"
              f"【类别】: {keyword}\n"
              f"【item列表总数据】: {list_count}\n"
              f"【对应数据总共】: {describe_info['count']}\n"
              f"【匹配成功数据】: {describe_info['finished_count']}\n"
              f"【缺失数据】: {describe_info['unfinished_count']}\n"
              f"【从表过滤条件】: {match_slave}\n"
              "=====================================================================")
        return describe_info

    # ==>５．清洗完数据导入mongoDb ---> 表名：dwd_目标主题_当前数据用途_脚本标识_时间标识
    @classmethod
    def mongo_insert_public(cls, tableName, data, id_tuple: tuple):
        # 元组拆出并拼接
        id_str = ''.join(list(map(lambda x: str(x), id_tuple)))
        data['_id'] = hashlib.md5(bytes(id_str, encoding='utf-8')).hexdigest()
        try:
            tableName.insert(data)
        except DuplicateKeyError:
            print(f'==> 【{tableName}】中_id重复....')

