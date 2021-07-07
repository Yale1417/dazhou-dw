# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/5 下午5:41
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : osd_clean.py
# @Software: PyCharm
# @class : osd层数据的导入、筛选
from db.mongo_db import Mongo
import clean


class Ods_Extract(object):

    def __init__(self):
        self.table = Mongo().mongo_get_tables()

    # 按按照时间规则抽取平台的数据   --->　根据不同的商品的关键词来过滤　--->聚合
    def ods_get_platform(self, start_date, end_date, platform, keyword, start_page, end_page):
        table_list = self.table['table_list']
        describe_info = Mongo.mongo_data_describe(tableName=table_list,
                                                  start_page=start_page,
                                                  end_page=end_page,
                                                  startDate=start_date,
                                                  endDate=end_date,
                                                  platform=platform,
                                                  keyword=keyword)
        finished_item = describe_info['finished_item']
        # 字段清洗

        for item in finished_item:
            if len(item['public']) >3 :
                print(item['num_iid'])


