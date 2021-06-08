# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/8 上午11:03
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : run.py
# @Software: PyCharm
# @class : Get all API data

from api_request import API_Request


class Elec(object):
    @classmethod
    # taobao
    def tb_search_parse(cls, keyword, start_page=1, end_page=1, is_all: bool = False):
        data = API_Request().get_search(api_url='https://api-gw.onebound.cn/taobao/item_search/',
                                        keyword=keyword,
                                        page=start_page)
        # 判断是否全部获取
        item = data['items']['item']
        max_page = data['items']['pagecount']

        print(data)
Elec().tb_search_parse(keyword='即食燕窝')

