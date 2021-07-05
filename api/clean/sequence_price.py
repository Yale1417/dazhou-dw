# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/5 上午10:51
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : data_sequence.py
# @Software: PyCharm
# @class : 所有价格参数的验证


class Sequence_Price(object):

    # ==> 1.验证价格
    @classmethod
    def sequence_price(cls, price):
        price = float(price)
        return price

    # ==> 2.验证折扣
    @classmethod
    def sequence_discount(cls, price, org_price):
        price = float(price)
        org_price = float(org_price)
        try:
            if price < org_price:
                is_promotion = 1
                discount_level = int(price / org_price * 100)
                return is_promotion, discount_level
            else:
                is_promotion = 0
                discount_level = 0
                return is_promotion, discount_level
        except Exception as e:
            print(e)
            is_promotion = 0
            discount_level = 0
            return is_promotion, discount_level
