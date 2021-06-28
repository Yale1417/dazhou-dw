# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/4 下午1:59
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : __init__.py.py
# @Software: PyCharm
# @PS : run main class

from elec import Elec
from mongo import Mongo

# # 淘宝搜索
# keywords = ['即食燕窝','鲜炖燕窝','即食花胶','即食鲍鱼','即食海参','佛跳墙','玻尿酸饮品','燕窝多肽',
#            '冻干燕窝','鱼胶冻']
# for keyword in keywords:
#     Elec().api_search(keyword=keyword, platform='taobao',is_all=True)

tables = Mongo().mongo_get_tables()




for i in data:
    print(i)