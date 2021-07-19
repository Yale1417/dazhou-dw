# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/14 下午2:22
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : guanzhan_comment.py
# @Software: PyCharm
# @class :  自定义评论获取
from api_request import API_Request
from mongo_db import Mongo


class Custom_Comment(object):

    # 1.手动获取id ---->txt获取
    @classmethod
    def get_id(cls):
        with open(r'官栈-tb-item-id.txt', 'r') as f:
            tb_id = f.read()
        tb_list = tb_id.split('\n')
        with open(r'官栈-jd-item-id.txt', 'r') as f:
            jd_id = f.read()
        jd_list = jd_id.split('\n')

        id_info = {'taobao': tb_list,
                   'jingdong': jd_list}

        return id_info

    # 2.请求评论
    @classmethod
    def get_comment(cls):
        id_info = Custom_Comment.get_id()
        jd_id = id_info['jingdong']
        tb_id = id_info['taobao']
        for num_iid in jd_id:
            data = API_Request().api_get_comments(num_iid=num_iid, platform='jingdong', page=1)
            if data:
                max_page = int(data['items']['totalpage'])
                for page in range(1, max_page):
                    data = API_Request().api_get_comments(num_iid=num_iid, platform='jingdong', page=page)
                    print(f'===>当前获取{num_iid}-----第{page}页-------共{max_page}页')
                    try:
                        items = data['items']['item']
                        for item in items:
                            item['num_iid'] = num_iid
                            Custom_Comment.save_comment(data=item,
                                                        platform='jingdong',
                                                        page=page,
                                                        keyword='官栈'
                                                        )
                    except Exception as e:
                        pass

        # ------------------------------------------------------
        # for num_iid in tb_id:
        #     data = API_Request().api_get_comments(num_iid=num_iid, platform='taobao', page=1)
        #     if data:
        #         max_page = int(data['items']['totalpage'])
        #         for page in range(1, max_page):
        #             data = API_Request().api_get_comments(num_iid=num_iid, platform='taobao', page=page)
        #             print(f'===>当前获取{num_iid}-----第{page}页-------共{max_page}页')
        #             try:
        #                 items = data['items']['item']
        #                 for item in items:
        #                     item['num_iid'] = num_iid
        #                     Custom_Comment.save_comment(data=item,
        #                                                 platform='taobao',
        #                                                 page=page,
        #                                                 keyword='官栈'
        #                                                 )
        #             except TypeError as e:
        #                 pass

    # 3.保存评论
    @classmethod
    def save_comment(cls, data, platform, page, keyword=''):
        table_comment = Mongo().mongo_get_tables()['table_comments']
        Mongo.mongo_insert(tableName=table_comment,
                           data=data,
                           keyword=keyword,
                           platform=platform,
                           page=page,
                           id_tuple=(data['rate_date'], data['display_user_nick']))
