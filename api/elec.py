# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/8 上午11:03
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : run.py
# @Software: PyCharm
# @class : Get all the data from the api
from api_request import API_Request
from sequence import Sequence
from mongo import Mongo
import time


class Elec(object):
    """
    about all requests
    """

    @classmethod
    def api_request(cls, api_url, keyword, page, max_page, platform):
        data = API_Request().get_search(api_url=api_url,
                                        keyword=keyword,
                                        page=page)
        Elec.show_info(keyword=keyword, page=page, max_page=max_page, platform=platform)
        Elec.json_parse(jsons=data, keyword=keyword)

    """
    api_search
    """

    @classmethod
    def api_search(cls, keyword, platform, start_page=1, end_page=1, is_all: bool = False):
        # keyword => url
        url_dict = {
            'taobao': 'https://api-gw.onebound.cn/taobao/item_search/',
            'jingdong':'https://api-gw.onebound.cn/jd/item_search/',


        }
        data = API_Request().get_search(api_url=url_dict[platform],
                                        keyword=keyword,
                                        page=start_page)
        # 使用real_total_results/page_size来取最大页面
        item = Sequence.kill_list_none(data['items']['item'])
        if item:
            max_page = int(data['items']['real_total_results'] / data['items']['page_size'])
            if is_all:
                for page in range(1, max_page):
                    Elec.api_request(api_url=url_dict[platform],
                                     keyword=keyword,
                                     page=page,
                                     max_page=max_page,
                                     platform=platform)
                    time.sleep(1)
            else:
                for page in range(start_page, end_page):
                    Elec.api_request(api_url=url_dict[platform],
                                     keyword=keyword,
                                     page=page,
                                     max_page=max_page,
                                     platform=platform)
        else:
            print('没有获取到商品列表信息,请验证请求是否正确...')

    """
    parse and save to mongo
    """

    @classmethod
    def json_parse(cls, jsons, keyword, platform):
        tbale_list = Mongo().mongo_get_tables()['table_list']
        items = jsons['items']['item']
        for item in items:
            Mongo.mongo_insert(tableName=tbale_list, data=item, keyword=keyword,
                               platform=platform)

    """
    show api-info  
    """

    @classmethod
    def show_info(cls, keyword, page, max_page , platform):
        print(f'-->当前任务:【{platform}】--【{keyword}】\n-->任务进度：【{page}】--【{max_page}】')

    """
    记录api请求次数
    """
