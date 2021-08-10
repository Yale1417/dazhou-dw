# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/8 下午4:12
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : filter.py
# @Software: PyCharm
# @class : 序列器 -> 对所有的json进行验证
from db.redis_mq import RedisMQ
import json
class Sequence(object):

    # Determine whether it is empty
    @classmethod
    def kill_list_none(cls, data: dict):
        # 请求验证
        try:
            if data['items']['item']:
                return data
            else:
                print('--> item列表为空')
                return None
        except Exception as e:
            print('==>字典中没有item属性...')
            print(e)

    # 请求状态验证
    @classmethod
    def validation_code(cls, validation_data: dict):
        # 验证响应代码
        jsons = validation_data['item']
        num_iid = validation_data['num_iid']
        platform = validation_data['platform']
        keyword = validation_data['keyword']
        code_status = jsons['error_code']
        if code_status == '0000':
            return jsons
        elif code_status in ['2000', '4006', '4007', '4008', '4016', '4017']:
            redis_msg = {'code_status': code_status,
                         'num_iid': num_iid,
                         'platform': platform,
                         'keyword': keyword}
            RedisMQ().redis_push(name='abnormal_urls', push_msg=redis_msg)
            print('===> 【请求异常】已存入RedisMQ...')
        else:
            redis_msg = {'code_status': code_status,
                         'num_iid': num_iid,
                         'platform': platform,
                         'keyword': keyword}
            RedisMQ().redis_push(name='abnormal_urls', push_msg=redis_msg)
            print('===> 【请求异常】已存入RedisMQ...')




    # 检验data是否正常,设置必须带的属性
    @classmethod
    def validation_data(cls, data: dict, ):
        try:
            price = data['item']['price']
            if price:
                if float(price) != 0:
                    if data['error'] == '':
                        return data
                    else:
                        print(data)
                        print('===> 数据出错... ')



        except Exception as e:
            print(data)
            print(e)
            print('==> 返回值检验未通过....')
