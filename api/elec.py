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
from db.mongo_db import Mongo
from db.redis_mq import RedisMQ
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
    def api_details(cls, redis_key):

        if redis_key == 'abnormal_urls':
            try:
                request_data = eval(RedisMQ().redis_pop(redis_key))
            except Exception:
                request_data = eval(RedisMQ().redis_pop(redis_key))

            data = API_Request().get_details(platform=request_data['platform'],
                                             num_iid=request_data['num_iid'],
                                             keyword=request_data['keyword'])

            print(f"==> 当前执行---{request_data['num_iid']}")
            if data:
                Elec.details_parse(jsons=data['item'], keyword=request_data['keyword'],
                                   platform=request_data['platform'], page='')

        else:
            request_data = eval(RedisMQ().redis_pop(redis_key))
            # 测试请求时间
            start_time = time.time()
            data = API_Request().get_details(platform=request_data['platform'],
                                             num_iid=request_data['num_iid'],
                                             keyword=request_data['keyword'])
            end_time = time.time() - start_time
            print(f"==> 当前执行【{request_data['platform']}】----{request_data['keyword']}------{request_data['num_iid']}"
                  f"-------请求时长【{end_time}】")
            if data:
                Elec.details_parse(jsons=data['item'], keyword=request_data['keyword'],
                                   platform=request_data['platform'], page=request_data['page'])



    """
     获取所有满足条件的num_iid
    """

    @classmethod
    def get_list_id(cls, startDate, endDate, platform, keyword):
        data = Mongo.mongo_query(tableName=Mongo().mongo_get_tables()['table_list'],
                                 startDate=startDate,
                                 endDate=endDate,
                                 platform=platform,
                                 keyword=keyword)
        # 判断是否重新导入到redis
        # redis_count = RedisMQ().redis_len(name='details_urls')
        # is_add = input(f'==>当前已有【{redis_count}】个请求在队列中，是否清空details_urls重新添加？\n==>y/n?')
        # --->直接获取
        if 'y' == 'y':
            RedisMQ().redis_delete('details_urls')
            for i in data:
                item_info = {'num_iid': i['num_iid'], 'keyword': i['keyword'], 'platform': i['platform'],
                             'page': i['page']}
                RedisMQ().redis_push(name='details_urls', push_msg=item_info)
            print('==>重新添加成功~')
            return RedisMQ().redis_len(name='details_urls')

        else:
            return RedisMQ().redis_len(name='details_urls')

    """
     搜索接口详情
    """

    @classmethod
    def json_parse(cls, jsons, keyword, platform, page, ):
        tbale_list = Mongo().mongo_get_tables()['table_list']
        items = jsons['items']['item']
        for item in items:
            item['request_date'] = time.strftime('%Y-%m-%d')
            Mongo.mongo_insert(tableName=tbale_list, data=item, keyword=keyword,
                               platform=platform, page=page,
                               id_tuple=(item['request_date'], item['num_iid'], item['price']))

    """
    商品详情数据保存
    """

    @classmethod
    def details_parse(cls, jsons, keyword, platform, page, ):
        jsons['request_date'] = time.strftime('%Y-%m-%d')
        tbale_details = Mongo().mongo_get_tables()['table_details']
        Mongo.mongo_insert(tableName=tbale_details, data=jsons, keyword=keyword,
                           platform=platform, page=page,
                           id_tuple=(jsons['num_iid'], jsons['request_date']))

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
            except Exception as e:
                print(e)
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
