# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/13 上午9:28
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : jd_price.py
# @Software: PyCharm
# @class : 用于京东的销售量的补充
import requests
import json

import urllib3.exceptions

from clean.sequence_price import Sequence_Price
from db.mysql_db import MYSQL


class JD_SALES(object):

    # 1.读取需要修改价格的id
    @classmethod
    def get_jd_num_iid(cls):
        with open('spider/jd_sale_num_iid.txt', 'r') as f:
            all_id = f.read()
        return all_id.split('\n')

    # 2.随机读取ua
    @classmethod
    def get_spider_ua(cls):
        from random import choice
        with open(r'spider/user_agent.txt') as f:
            jsons = f.read()

        return choice(eval(jsons))

    # 3. 开启代理
    @classmethod
    def open_proxy(cls, isTrue):
        if isTrue:
            print('--->已开启代理！')
            # 代理服务器
            proxyHost = "http-dyn.abuyun.com"
            proxyPort = "9020"

            # 代理隧道验证信息
            proxyUser = "H0K2I5C024F0354D"
            proxyPass = "23B431835F27F570"

            proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                "host": proxyHost,
                "port": proxyPort,
                "user": proxyUser,
                "pass": proxyPass,
            }

            proxies = {
                "http": proxyMeta,
                "https": proxyMeta,
            }
            return proxies

    # 4.构建京东评论连接 --->仅仅采集第一页，当做销量 --->会检查UA
    @classmethod
    def jd_request(cls, num_iid):
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;'
                             'q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                   "Accept-Encoding": "gzip, deflate, br",
                   "Connection": "close",
                   "houst": "club.jd.com",
                   "User-Agent": JD_SALES.get_spider_ua(),
                   }

        base_urls = f"https://club.jd.com/comment/skuProductPageComments.action?" \
                    f"&productId={num_iid}&score=0" \
                    f"&sortType=5&page=1&pageSize=10&isShadowSku=0&fold=1"
        proxy = JD_SALES.open_proxy(isTrue=True)
        try:
            responses = requests.get(url=base_urls, headers=headers, proxies=proxy,).text
            time.sleep(0.5)
        except Exception:
            time.sleep(5)
            print('===> 请求异常，休息5秒！')
            return JD_SALES.jd_request(num_iid=num_iid)
        try:
            data = json.loads(responses)
            sales = Sequence_Price.sequence_sales(sales=data['productCommentSummary']['commentCountStr'])
            print(f'====> 当前获取的销售量为：{sales}')
            return sales
        except Exception as e:
            print('---> 请求失败！')
            return JD_SALES.jd_request(num_iid=num_iid)

    # 开始修改


items = JD_SALES.get_jd_num_iid()
for num_iid in items:
    import time

    sales = JD_SALES.jd_request(num_iid=num_iid)
    MYSQL(databaseName='dwd_dws_electricity_etl', collectionName='dwd_electricity_etl_list_202107'). \
        mysql_update(key='sales', value=sales, num_iid=num_iid)
