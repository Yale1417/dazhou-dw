# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/4 下午2:04
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : api_request.py
# @Software: PyCharm
# @PS : 该类用作所有请求的基础类,实现列表请求和详情请求


import json5
import requests
import os

class api_request(object):

    headers = {
        "Accept-Encoding": "gzip",
        "Connection": "close"
    }
    key = os.environ.get('WB_API_KEY')
    secret =  os.environ.get('WB_API_SECRET')

    # 搜索列表
    def get_search(self, api_url, keyword, page, **kwargs):
        base_url = f"{api_url}?key={self.key}&secret={self.secret}&q={keyword}" \
                   f"&start_price={kwargs['start_price']}&end_price={kwargs['end_price']}" \
                   f"&page={page}&cat={kwargs['cat']}&discount_only={kwargs['discount_only']}" \
                   f"&sort={kwargs['sort']}&page_size={kwargs['page_size']}&seller_info=&nick=&ppath="

        responses = requests.get(url=base_url, headers=self.headers)
        data = json5.loads(responses, encoding='utf-8')
        return data

    # 详情列表
    def get_details(self, api_url, num_iid):
        base_url = f'{api_url}?key={self.key}&secret={self.secret}&num_iid=520813250866&is_promotion=1'
        responses = requests.get(url=base_url, headers=self.headers)
        data = json5.loads(responses, encoding='utf-8')
        return data










