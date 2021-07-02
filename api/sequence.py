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
        except KeyError:
            print('==>key错误,字典中没有item属性...')

    # 检验data是否正常,设置必须带的属性
    @classmethod
    def validation_data(cls, data: dict,):
        try:
            price = data['item']['price']
            if float(price) != 0:
                return data

        except Exception as e:
            print(data)
            print('==> 返回值检验未通过....')
            return None

