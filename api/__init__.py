# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/4 下午1:59
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : __init__.py.py
# @Software: PyCharm
# @PS : run main class

from elec import Elec

# # 淘宝搜索
# keywords = ['即食燕窝','鲜炖燕窝','即食花胶','即食鲍鱼','即食海参','佛跳墙','玻尿酸饮品','燕窝多肽',
#            '冻干燕窝','鱼胶冻']
# for keyword in keywords:
#     Elec().api_search(keyword=keyword, platform='taobao',is_all=True)

# 商品详情获取

items = Elec.get_list_id(startDate='2021-06-01',
                         endDate='2021-06-31',
                         start_page=0,
                         end_page=11,
                         platform='jingdong')
Elec.api_details(items=items)

# 淘宝测试
# Elec().taobao_details()
