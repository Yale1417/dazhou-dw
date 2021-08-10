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
2.delivery_provins -----> 发货份
3.delivery_city  ------> 发货城市
4.production_city   -----> 生产城市
5.city_level  -------> 城市等级、
"""
from tools_class import Tools_Class
class Sequence_Region(object):

    # 发货城市提取
    @classmethod
    def sequence_get_city(cls, data):
        addres = data['public']['location']
        # 1. 发货城市/省份/级别
        delivery_info = Tools_Class.tools_spi_city(addres)
        if delivery_info:
            region_info = {
                'delivery_provins':delivery_info['province'],
                'delivery_city':delivery_info['city'],
                'delivery_city_level':delivery_info['city_level']
            }

            return region_info
        else:
            region_info = {
                'delivery_provins': '',
                'delivery_city': '',
                'delivery_city_level': ''
            }
            return region_info
