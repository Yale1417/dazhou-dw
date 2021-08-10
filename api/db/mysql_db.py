# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/31 下午3:19
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : mysql_sb.py
# @Software: PyCharm
# @class :  用于中间数据储存
# from abstract.db_base import DB_BASE
import pymysql


class MYSQL(object):

    def __init__(self, databaseName, collectionName, ):
        self.collectionName = collectionName
        conn = pymysql.connect(host='192.168.0.16',
                               port=3306,
                               user='root',
                               passwd='Always@Latent==1',
                               db=databaseName,
                               charset='utf8',
                               autocommit=True,

                               )
        self.cur = conn.cursor()

    # 插入
    def mysql_insert(self, data):
        _sql = f"insert into {self.collectionName}({','.join(data.keys())})VALUES{tuple(data.values())}"

        try:
            self.cur.execute(_sql)
            self.cur.close()
            print(f"===> 插入成功！当前项目【{data['time_date']}----{data['project_name']}---{data['platform']}】")
        except Exception as e:
            print(e)

    # 修改数据
    def mysql_update(self, key, value, **where):
        where_key = ''.join(where.keys())
        where_values = where[where_key]
        _sql = f"UPDATE {self.collectionName} SET {key}={value} WHERE {where_key}='{where_values}'"
        try:
            self.cur.execute(_sql)
            print(f"{where['num_iid']}==> 价格修改成功！")
        except Exception as e:
            print(e)
