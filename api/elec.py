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

    # -->2. api_details 获取详情
    @classmethod
    def api_details(cls, items: dict):
        for item in items:
            print(item)
            data = API_Request().get_details(platform=item['platform'],
                                             num_iid=item['num_iid'])

            # data['keyword'] = item['keyword']
            # data['platform'] = item['platform']
            # data['page'] = item['page']
            # Elec.details_parse(jsons=data['item'], keyword=item['keyword'],
            #                    platform=item['platform'], page=item['page'])

    """
     获取所有满足条件的num_iid
    """

    @classmethod
    def get_list_id(cls, startDate, endDate, start_page, end_page, platform):
        list_id = []
        data = Mongo.mongo_query(tableName=Mongo().mongo_get_tables()['table_list'],
                                 startDate=startDate,
                                 endDate=endDate,
                                 platform=platform,
                                 start_page=start_page,
                                 end_page=end_page)

        for i in data:
            item_info = {'num_iid': i['num_iid'], 'keyword': i['keyword'], 'platform': i['platform'],
                         'page': i['page']}
            list_id.append(item_info)
        return list_id

    """
    parse and save to mongo
    """

    @classmethod
    def json_parse(cls, jsons, keyword, platform, page, ):
        tbale_list = Mongo().mongo_get_tables()['table_list']
        items = jsons['items']['item']
        for item in items:
            Mongo.mongo_insert(tableName=tbale_list, data=item, keyword=keyword,
                               platform=platform, page=page)

    """
    商品详情数据保存
    """

    @classmethod
    def details_parse(cls, jsons, keyword, platform, page, ):
        tbale_details = Mongo().mongo_get_tables()['table_details']
        Mongo.mongo_insert(tableName=tbale_details, data=jsons, keyword=keyword,
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
        max_page = 0
        items = data['items']
        if 'pagecount' in items:
            try:
                if int(items['pagecount']) > 0:
                    max_page = int(items['pagecount'])
            except Exception:
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

    # 测试
    @classmethod
    def taobao_details(cls):

        table_list = Mongo().mongo_get_tables()['table_list']
        keywords = ['即食燕窝', '即食花胶', '即食鲍鱼', '即食海参', '佛跳墙', '玻尿酸饮品', '燕窝多肽',
                    '冻干燕窝', '鱼胶冻']

        for keyword in keywords:
            items_id = []
            item_count = table_list.find({'platform': 'taobao', 'keyword': keyword}).count()
            mongo_data = table_list.find({'platform': 'taobao', 'keyword': keyword}).sort('sales')
            for i in mongo_data:
                items_id.append(i)

            # -->请求
            item_id = items_id[int(item_count - item_count * 0.05):]
            for item in item_id:
                data = API_Request().get_details(platform=item['platform'],
                                                 num_iid=item['num_iid'])
                print(data['item']['num_iid'])
                Elec.details_parse(jsons=data['item'], keyword=keyword,
                                   platform='taobao', page=1)
