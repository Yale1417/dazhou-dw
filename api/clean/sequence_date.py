# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/19 下午7:18
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : sequence_date.py
# @Software: PyCharm
# @class : 时间的分割

"""
1. time_stamp ----->采集时间戳
2. time_year
3. time_month
4. time_day
5. date_id   ------> 自动创建
"""
import time


class Sequence_Date(object):

    # 时间转换 与 拆解
    @classmethod
    def sequence_date(cls, data):
        request_date = data['request_date']
        date_list = request_date.split('-')
        date_year = date_list[0]
        date_month = date_list[1]
        date_day = date_list[2]
        # 转化
        time_date = f'{request_date} 00:00:00'
        time_stamp = int(time.mktime(time.strptime(time_date, '%Y-%m-%d %H:%M:%S')))

        date_indo = {'time_year': date_year,
                     'time_month': date_month,
                     'time_day': date_day,
                     'time_stamp': time_stamp}

        return date_indo
