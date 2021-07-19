# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/5 上午10:51
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : data_sequence.py
# @Software: PyCharm
# @class : 所有价格参数的验证

"""
字段说明:
1.price_id   ---> 数据库处理
2.price
3.orginal_price
4.range_price ---> 后续处理
5.is_promotion
6.discount_level
7.price_level ----> 后续处理

"""


class Sequence_Price(object):

    @classmethod
    def sequence_discount(cls, price, org_price):
        if price:
            price = float(price)
            org_price = float(org_price)
        try:
            if price < org_price:
                is_promotion = True
                discount_level = int(price / org_price * 100)
                price_info = {'is_promotion': is_promotion,
                              'discount_level': discount_level,
                              'price': price,
                              'orginal_price': org_price,
                              }
                return price_info
            else:
                price_info = {'is_promotion': False,
                              'discount_level': 0,
                              'price': price,
                              'orginal_price': org_price,
                              }
                return price_info
        except Exception as e:
            print(e)

