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
from sequence import Sequence
from db.redis_mq import RedisMQ


class API_Request(object):
    headers = {
        "Accept-Encoding": "gzip",
        "Connection": "close",
    }
    key = os.environ.get('WB_API_KEY')
    secret = os.environ.get('WB_API_SECRET')

    # 请求次数限制

    # 搜索列表---
    def get_search(self, platform, keyword, page, start_price=0, end_price=0, ):
        local_args = locals()
        base_url = self.create_search_urls(platform=platform, kwargs=local_args)
        # 打印请求链接
        print(base_url)
        responses = requests.get(url=base_url, headers=self.headers, )
        try:
            data = json5.loads(responses.content, encoding='utf-8')
            return data
        except Exception:
            pass

    # 详情列表
    def get_details(self, platform, num_iid):
        base_url = API_Request().create_details_urls(platform=platform, num_iid=num_iid)
        responses = requests.get(url=base_url, headers=self.headers, )
        try:
            data = Sequence.validation_data(json5.loads(responses.text, encoding='utf-8', ))
            if data is not None:
                return data
            # 使用redis记录异常请求的请求信息
            else:
                redis_msg = {'num_iid': num_iid, 'platform': platform}
                RedisMQ().redis_push(name='abnormal_urls', push_msg=redis_msg)
        except Exception:
            pass

    # 搜索url
    def create_search_urls(self, platform, kwargs: dict):
        search_url = {'taobao': f"https://api-gw.onebound.cn/taobao/item_search/?"
                                f"key={self.key}&secret={self.secret}&q={kwargs['keyword']} "
                                f"&start_price={kwargs['start_price']}&end_price={kwargs['end_price']}"
                                f"&page={kwargs['page']}"
                                f"&cat=0&discount_only=&sort=&page_size=&seller_info=&nick=&ppath=&imgid=&filter=",
                      'jingdong': f"https://api-gw.onebound.cn/jd/item_search/?"
                                  f"key={self.key}&secret={self.secret}&q={kwargs['keyword']}"
                                  f"&start_price={kwargs['start_price']}&end_price={kwargs['end_price']}"
                                  f"&page={kwargs['page']}&"
                                  f"cat=0&discount_only=&sort=&seller_info=no&nick=&seller_info=&nick=&ppath=&imgid="
                                  f"&filter=",
                      'pdd': f"https://api-gw.onebound.cn/pinduoduo/item_search/?"
                             f"key={self.key}&secret={self.secret}&q={kwargs['keyword']}"
                             f"&start_price={kwargs['start_price']}&end_price={kwargs['end_price']}"
                             f"&page={kwargs['page']}"
                             f"&cat=0&discount_only=&sort=&page_size=",
                      'suning': f"https://api-gw.onebound.cn/suning/item_search/?"
                                f"key={self.key}&secret={self.secret}&q={kwargs['keyword']}"
                                f"&start_price={kwargs['start_price']}&end_price={kwargs['end_price']}"
                                f"&page={kwargs['page']}"
                                f"&cat=&discount_only=&sort=&page_size=&seller_info=&nick=&ppath=",

                      }

        return search_url[platform]

    # 详情url
    def create_details_urls(self, platform, num_iid):
        details_url = {'taobao': f"https://api-gw.onebound.cn/taobao/item_get/"
                                 f"?key={self.key}&secret={self.secret}"
                                 f"&num_iid={num_iid}&is_promotion=1",
                       'jingdong': f"https://api-gw.onebound.cn/jd/item_get/"
                                   f"?key={self.key}&secret={self.secret}"
                                   f"&num_iid={num_iid}",
                       'pdd': f"https://api-gw.onebound.cn/pinduoduo/item_get/"
                              f"?key={self.key}&secret={self.secret}"
                              f"&num_iid={num_iid}",
                       'suning': f"https://api-gw.onebound.cn/suning/item_get/"
                                 f"?key={self.key}&secret={self.secret}"
                                 f"&num_iid={num_iid}",

                       }

        return details_url[platform]
