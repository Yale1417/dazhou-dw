# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/13 上午9:28
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : jd_price.py
# @Software: PyCharm
# @class : 用于京东的价格爬取
import requests
from mongo_db import Mongo


class JD_PRICE(object):

    def __init__(self):
        table = Mongo().mongo_get_tables()
        self.table_details = table['table_details']


    @classmethod
    def jd_get_item_id(cls):
        pass
    @classmethod
    def jd_get_price(cls):
        pass

    def jd_edit_price(self):
        pass
