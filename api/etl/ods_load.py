# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/30 下午3:31
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : ods_load.py
# @Software: PyCharm
# @class :用于ods数据加载到dwd中

from db.mysql_db import MYSQL


class Ods_Load(object):
    def __init__(self):
        pass

    # 插入sql
    @classmethod
    def load_mysql_insert(cls, databaseName, collectionName, data):
        if 'id' in data:
            MYSQL(databaseName=databaseName, collectionName=collectionName).mysql_insert(data=data)
        else:
            data['id'] = 0
            MYSQL(databaseName=databaseName, collectionName=collectionName).mysql_insert(data=data)

