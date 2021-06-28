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
    1. about all requests
    """

    @classmethod
    def search_request(cls, keyword, page, maxPage, platform):
        Elec.show_info(keyword=keyword, page=page, maxPage=maxPage, platform=platform)
        data = API_Request().get_search(keyword=keyword,
                                        page=page,
                                        platform=platform)
        # 验证data
        item = Sequence.kill_list_none(data)
        if item:
            Elec.json_parse(jsons=data, keyword=keyword, platform=platform, page=page)
        else:
            pass

    """
    api_search 获取列表
    """

    @classmethod
    def api_search(cls, keyword, platform, start_page=1, end_page=1, is_all: bool = False):
        # keyword => url

        data = API_Request().get_search(keyword=keyword,
                                        platform=platform,
                                        page=1)

        item = Sequence.kill_list_none(data)
        if item:
            max_page = Elec.get_max_page(data)
            if is_all:
                for page in range(1, max_page):
                    Elec.search_request(keyword=keyword,
                                        page=page,
                                        maxPage=max_page,
                                        platform=platform)
                    time.sleep(1)
            else:
                for page in range(start_page, end_page):
                    Elec.search_request(keyword=keyword,
                                        page=page,
                                        maxPage=max_page,
                                        platform=platform)
        else:
            pass


    """
    api_details 获取详情
    """
    @classmethod
    def api_details(cls, platform, ):
        pass

    """
     获取所有满足条件的num_iid
    """
    @classmethod
    def get_list_id(cls, startDate, endDate, page, platform):
        list_id = []
        data = Mongo.mongo_query(tableName=Mongo().mongo_get_tables()['table_list'],
                                 startDate=startDate,
                                 endDate=endDate,
                                 platform=platform,
                                 page=page)
        if len(data) > 1:
            for i in data:
                list_id.append(i['num_iid'])
            return list_id
        else:
            print(f'没有查询到{startDate}----{endDate}的数据！！！，请验证...')





    """
    parse and save to mongo
    """

    @classmethod
    def json_parse(cls, jsons, keyword, platform, page):
        tbale_list = Mongo().mongo_get_tables()['table_list']
        items = jsons['items']['item']
        for item in items:
            Mongo.mongo_insert(tableName=tbale_list, data=item, keyword=keyword,
                               platform=platform, page=page)

    """
    show api-info  
    """

    @classmethod
    def show_info(cls, keyword, page, maxPage, platform):
        print(f'-->当前任务:【{platform}】--【{keyword}】\n-->任务进度：【{page}】--【{maxPage}】')

    """
    最大页面获取。判断page_size、real_total_results、list_count是否存在
    """

    @classmethod
    def get_max_page(cls, data):
        global max_page
        items = data['items']
        if 'pagecount' in items:
            try:
                if int(items['pagecount']) > 0:
                    max_page = int(items['pagecount'])
            except Exception :
                max_page = 0

        elif 'page_size' in items:
            if int(items['page_size']) > 0:
                max_page = int(int(data['items']['real_total_results']) / int(data['items']['page_size']))

        elif 'list_count' in items:
            if int(items['list_count']) > 0:
                max_page = int(int(data['items']['real_total_results']) / int(data['items']['list_count']))

        if max_page > 0:
            return max_page
        else:
            return 50
