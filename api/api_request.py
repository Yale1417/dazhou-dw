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
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Origin': 'http://open.onebound.cn',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'http://open.onebound.cn/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
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
        except Exception as e :
            print(e)

    # 详情列表
    def get_details(self, platform, num_iid):
        base_url = API_Request().create_details_urls(platform=platform, num_iid=num_iid)
        responses = requests.get(url=base_url, headers=self.headers, )
        # --->将数据字段验证修改为状态码验证
        code_status, data = Sequence.validation_code(json5.loads(responses.text, encoding='utf-8', ))
        if code_status == '0000':
            return data
        # 使用redis记录异常请求的请求信息
        elif code_status in ['2000', '4006', '4007', '4008', '4016', '4017']:
            redis_msg = {'code_status': code_status, 'num_iid': num_iid, 'platform': platform}
            RedisMQ().redis_push(name='abnormal_urls', push_msg=redis_msg)
        else:
            redis_msg = {'code_status': code_status, 'num_iid': num_iid, 'platform': platform}
            RedisMQ().redis_push(name='error_urls', push_msg=redis_msg)

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

    # 评论url
    def create_comment_urls(self, platform, num_iid , page):
        comment_urls = {'taobao':f"https://api-gw.onebound.cn/taobao/item_review/?"
                                 f"key={self.key}&&num_iid={num_iid}&data=&page={page}"
                                 f"&&lang=zh-CN&secret={self.secret}",
                        'jingdong':"https://api-gw.onebound.cn/jd/item_review/?"
                                   f"key={self.key}&&num_iid={num_iid}&"
                                   f"page={page}&&lang=zh-CN&secret={self.secret}",
        }

        return comment_urls[platform]

    # 获取评论
    def api_get_comments(self, platform, num_iid, page):
        base_url = API_Request().create_comment_urls(platform=platform,
                                                     num_iid=num_iid,
                                                     page=page)
        print(base_url)
        responses = requests.get(url=base_url, headers=self.headers, )
        code_status, data = Sequence.validation_code(json5.loads(responses.text, encoding='utf-8', ))
        if code_status == '0000':
            return data




