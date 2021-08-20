# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/8/17 下午5:47
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : mong.py
# @Software: PyCharm
# @class :

"""
1. 抽取mysql数据
2. 重新采集details
3. json数据装入
"""

from db.mysql_db import MYSQL
from db.redis_mq import RedisMQ


class TMP_SUPPLEMENT_DETAILS(object):

    # 拉取所有id
    def get_id(self, platform):
        _sql = f"select * from dwd_electricity_etl_list_202107 where platform='{platform}'"
        mysql_data = MYSQL(databaseName='dwd_dws_electricity_etl', collectionName='dwd_electricity_etl_list_202107') \
            .mysql_query(query_str=_sql)
        for i in mysql_data:
            keyword = i[1]
            page = i[2]
            num_iid = i[3]
            platform = i[-1]
            date = i[4] + '-' + i[5] + '-' + i[6]
            info = {
                'keyword': keyword,
                'page': page,
                'num_iid': num_iid,
                'platform': platform,
                'date': date,
            }

            self.push_redis(platform=platform, msg=info)

    # 根据平台名称插入redis

    def push_redis(self, platform, msg: dict):
        key_name = f"{platform}-{msg['date']}"
        RedisMQ().redis_push(name=key_name, push_msg=msg)


# TMP_SUPPLEMENT_DETAILS().get_id('')


