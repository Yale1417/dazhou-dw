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


class API_Request(object):
    headers = {
        "Accept-Encoding": "gzip",
        "Connection": "close"
    }
    key = os.environ.get('WB_API_KEY')
    secret = os.environ.get('WB_API_SECRET')

    # 搜索列表---
    def get_search(self, platform, keyword, page, start_price=0, end_price=0, ):
        local_args = locals()
        base_url = self.create_urls(platform=platform, kwargs=local_args)
        # 打印请求链接
        print(base_url)
        responses = requests.get(url=base_url, headers=self.headers)
        try:
            data = json5.loads(responses.content, encoding='utf-8')
            return data
        except ValueError:
            pass

    # 详情列表
    def get_details(self, api_url, num_iid):
        base_url = f'{api_url}?key={self.key}&secret={self.secret}&num_iid={num_iid}' \
                   f'&is_promotion=1'
        responses = requests.get(url=base_url, headers=self.headers)
        data = json5.loads(responses, encoding='utf-8')
        return data

    # 不同平台链接构造
    def create_urls(self, platform, kwargs: dict):
        platform_url = {'taobao': f"https://api-gw.onebound.cn/taobao/item_search/?"
                                  f"key={self.key}&secret={self.secret}&q={kwargs['keyword']} "
                                  f"&start_price={kwargs['start_price']}&end_price={kwargs['end_price']}"
                                  f"&page={kwargs['page']}"
                                  f"&cat=0&discount_only=&sort=&page_size=&seller_info=&nick=&ppath=&imgid=&filter=",
                        'jingdong': f"https://api-gw.onebound.cn/jd/item_search/?"
                                    f"key={self.key}&secret={self.secret}&q={kwargs['keyword']}"
                                    f"&start_price={kwargs['start_price']}&end_price={kwargs['end_price']}"
                                    f"&page={kwargs['page']}&"
                                    f"cat=0&discount_only=&sort=&seller_info=no&nick=&seller_info=&nick=&ppath=&imgid=&filter=",
                        'pdd': '',
                        'suning': '',

                        }

        return platform_url[platform]
