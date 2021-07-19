# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/19 下午7:43
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : sequence_region.py
# @Software: PyCharm
# @class : 发货地址

"""
1. region_id
2.delivery_provins -----> 发货省份
3.delivery_city  ------> 发货城市
4.production_city   -----> 生产城市
5.city_level  -------> 城市等级、
"""

class Sequence_Region(object):

    # 发货城市提取
    @classmethod
    def sequence_get_city(cls, data):
        # 分平台获取

        pass