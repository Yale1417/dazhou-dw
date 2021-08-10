# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/4 下午1:59
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : __init__.py.py
# @Software: PyCharm·
# @PS : run main class
from elec import Elec
from etl.ods_extract import Ods_Extract
from etl.ods_transform import Ods_Transform
from etl.ods_load import Ods_Load

# ####################################【1.搜索列表】##########################################
# keywords = ['即食燕窝', '鲜炖燕窝', '即食花胶', '即食鲍鱼', '即食海参', '佛跳墙', '透明质酸钠饮品', '燕窝多肽饮品',
#             '冻干燕窝', '鱼胶冻','燕窝粥']
# for keyword in keywords:
#     Elec().api_search(keyword=keyword, platform='suning', is_all=True, start_page=1, end_page=200)

# 2.单机循环
# Elec().api_search(keyword='燕窝粥', platform='suning', is_all=True, start_page=1, end_page=200)


# ####################################【3.商品详情】##########################################
# keywords = ['即食燕窝', '鲜炖燕窝', '即食花胶', '即食鲍鱼', '即食海参', '佛跳墙', '透明质酸钠饮品', '燕窝粥',
#             '冻干燕窝', '鱼胶冻']
#
# for keyword in keywords:
#     item_count = Elec.get_list_id(startDate='2021-07-20',
#                                   endDate='2021-07-31',
#                                   platform='suning',
#                                   keyword=keyword)
#     for i in range(0, item_count):
#         Elec.api_details(redis_key='details_urls')
#  #####################################【3.异常处理】##########################################

# 异常处理
# while True:
#     Elec.api_details(redis_key='abnormal_urls')


#  ###################################【4.ETL操作】###########################################
# keywords = ['即食燕窝', '鲜炖燕窝', '即食花胶', '即食鲍鱼', '即食海参', '佛跳墙', '透明质酸钠饮品', '燕窝多肽饮品',
#             '冻干燕窝', '鱼胶冻']
# # platforms = ['jingdong', 'taobao', 'pdd', 'suning']
# for keyword in keywords:
#     extract_data = Ods_Extract(start_date='2021-07-01',
#                                end_date='2021-07-15',
#                                platform='jingdong',
#                                keyword=keyword,
#                                isCustom=False).osd_extract_list()

#  #################################【5.单机获取评论】#########################################
# Custom_Comment.get_comment()

#  #################################【6.修改京东价格】#########################################
#
# from spider.jd_sales import JD_SALES
#
# JD_SALES.get_jd_num_iid()