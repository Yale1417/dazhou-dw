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
import re


class Sequence_Price(object):

    @classmethod
    # 1.计算折扣价格
    def sequence_discount(cls, price, org_price):
        if price:
            price = float(price)
            org_price = float(org_price)
        try:
            if price < org_price:
                discount_level = int(price / org_price * 100)
                price_info = {'is_promotion': 1,
                              'discount_level': discount_level,
                              'price': price,
                              'orginal_price': org_price,
                              }
                return price_info
            else:
                price_info = {'is_promotion': 0,
                              'discount_level': 0,
                              'price': price,
                              'orginal_price': org_price,
                              }
                return price_info
        except Exception as e:
            print(e)

    # 2.销售量清洗
    @classmethod
    def sequence_sales(cls, sales):
        if sales:
            if type(sales) == str:
                sales_str = float(''.join(re.findall(r'\d+\.\d+|\d+', sales)))
                if '万' in str(sales):
                    return int(sales_str * 10000)
                else:
                    return int(sales_str)
            else:
                return sales
        else:
            return 0

    # 3. 价格字段清洗
    @classmethod
    def sequence_price(cls, price):
        if price:
            try:
                price = float(price)
                return {'price': price}
            except Exception as e:
                print(e)
                return {'price': 0}

        else:
            return {'price': 0}
