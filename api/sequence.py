# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/8 下午4:12
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : filter.py
# @Software: PyCharm
# @class : 序列器 -> 对所有的json进行验证

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

    @classmethod
    def validation_code(cls, data: dict):
        code_status = data['error_code']
        if code_status == '0000':
            return code_status, data
        elif code_status == '2000':
            print('===> 没有获取到该信息...')
            return code_status, None
        elif code_status == '5000':
            print('===> 数据未知错误...')
            return code_status, None
        elif code_status == '4017':
            print('===> 请求超时...')
            return code_status, None
        else:
            print(f'===> 【状态码】{code_status}')
            return code_status, None

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
