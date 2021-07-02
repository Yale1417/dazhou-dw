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
from redis_mq import RedisMQ


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
    def api_details(cls, redis_key):
        request_data = eval(RedisMQ().redis_pop(redis_key))
        data = API_Request().get_details(platform=request_data['platform'],
                                         num_iid=request_data['num_iid'])
        print(data)

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
        data = Mongo.mongo_query(tableName=Mongo().mongo_get_tables()['table_list'],
                                 startDate=startDate,
                                 endDate=endDate,
                                 platform=platform,
                                 start_page=start_page,
                                 end_page=end_page)
        # 判断是否重新导入到redis
        redis_count = RedisMQ().redis_len(name='details_urls')
        is_add = input(f'==>当前已有【{redis_count}】个请求在队列中，是否清空details_urls重新添加？\n==>y/n?')
        if is_add == 'y':
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
