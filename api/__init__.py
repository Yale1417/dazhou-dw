# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/4 下午1:59
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : __init__.py.py
# @Software: PyCharm·
# @PS : run main class

from elec import Elec
from clean.ods_extract import Ods_Extract

# 淘宝搜索
# keywords = ['即食燕窝', '鲜炖燕窝', '即食花胶', '即食鲍鱼', '即食海参', '佛跳墙', '透明质酸钠饮品', '燕窝多肽饮品',
#             '冻干燕窝', '鱼胶冻']
# for keyword in keywords:
#     Elec().api_search(keyword='冻干燕窝', platform='taobao', is_all=True, start_page=1, end_page=200)

# 单机循环
# Elec().api_search(keyword='燕窝多肽饮品', platform='suning', is_all=True, start_page=1, end_page=200)

# 商品详情获取
# item_count = Elec.get_list_id(startDate='2021-07-01',
#                               endDate='2021-07-06',
#                               start_page=0,
#                               end_page=11,
#                               platform='suning')
#
# for i in range(0, item_count):
#     Elec.api_details(redis_key='details_urls')

# 淘宝测试
# Elec().taobao_details()


# 清洗测试
Ods_Extract().ods_get_platform(start_date='2021-06-01', end_date='2021-06-31',
                               platform='jingdong', keyword='即食燕窝',
                               start_page=1, end_page=11
                               )

