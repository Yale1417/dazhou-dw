# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/19 下午7:00
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : sequence_num.py
# @Software: PyCharm
# @class : 对于库存的清洗
"""
字段说明：
1.inventory_id ---->数据库自增
2.num ---> 当前库存
3.num_level ---> 库存等级

"""


class Sequence_Num(object):

    # 1. 库存等级换算 ------> 库存0-50->紧张  50-100 -> 正常 100以上充足
    @classmethod
    def sequence_num_level(cls, data):
        platform = data['platform']
        if platform != 'pdd':
            item_num = int(data['public']['num'])
            if item_num <= 50:
                num_level = '紧张'
            elif 50 < item_num <= 100:
                num_level = '正常'
            else:
                num_level = '充足'
        else:
            item_num = int(data['public']['num'])
            if item_num <= 300:
                num_level = '紧张'
            elif 300 < item_num <= 999:
                num_level = '正常'
            else:
                num_level = '充足'

        num_info = {'num': item_num,
                    'num_level': num_level}

        return num_info
