# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/20 下午5:11
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : set_specification.py
# @Software: PyCharm
# @class :  获取所有的规格，然后对规格合并后形成集合

from db.mongo_db import Mongo

class Get_Set_Sepeci(object):

    def __init__(self):
        tables = Mongo().mongo_get_tables()
        self.table_details = tables['table_details']

    #  抽取所有的 规格 放到集合中  -----> 只针对props
    def sepeci_get_props(self, startDate, endDate , keyword):
        if keyword:
            match = {
                "$match": {"$and": [{"keyword":keyword},
                                    {"request_date": {"$gte": startDate,
                                                      "$lte": endDate}},
                                    ]
                           }
            }
        else:
            match = {
                "$match": {"$and": [
                                    {"request_date": {"$gte": startDate,
                                                      "$lte": endDate}},
                                    ]
                           }
            }

        mongo_data = self.table_details.aggregate([match])
        set_sepeci = set()
        for data in mongo_data:
            try:
                props = data['props']
                if props:
                    for prop in props:
                        set_sepeci.add(prop['name'])
            except KeyError:
                pass







