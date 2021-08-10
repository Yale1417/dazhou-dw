# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/5 下午5:29
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : sequence_nick.py
# @Software: PyCharm
# @class : 清晰店铺的相关信息

"""
字段说明：
1.nick_id ---->数据库自增
2.nick_name
3.nick
4.brand
5.company_name
6.platform
"""

from tools_class import Tools_Class


class Sequence_Nick(object):

    # 品牌提取
    @classmethod
    def sequence_brand(cls, data):
        # 1. 店铺名称
        seller = Sequence_Nick.sequence_seller(data=data)

        # 2.店铺编号
        sid = Tools_Class.tools_md5(nick=seller)
        # 3. 品牌
        brand = data['public']['brand']
        # 4. 平台
        platform = data['platform']
        if platform == 'taobao':
            tmall = data['public']['tmall']
            if tmall:
                platform = 'tmall'
            else:
                platform = 'taobao'

        platform = {
            'seller': seller,
            'nick_id': sid,
            'brand': brand,
            'platform': platform
        }

        return platform

    # 商品店铺名称
    @classmethod
    def sequence_seller(cls, data):
        try:
            seller = data['seller']
        except KeyError as k:
            seller = data['seller_nick']
            if seller is None:
                seller = data['public']['nick']
        return seller
