# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/5 下午5:41
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : osd_clean.py
# @Software: PyCharm
# @class : osd层数据的导入、筛选
from api.mongo import Mongo
class Ods_Extract(object):

    def __init__(self):
        self.table = Mongo().mongo_get_tables()

    # 按按照时间规则抽取平台的数据   --->　根据不同的商品的关键词来过滤　
    @classmethod
    def ods_get_platform(cls, start_date, end_date):
        pass





