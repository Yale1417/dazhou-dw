# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/29 上午9:59
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : show_request_info.py
# @Software: PyCharm
# @class : 用于展示terminal的信息
import functools


class ShowRequestInfo(object):

    # 展示当前请求的参数
    @classmethod
    def decorator_request_show(cls, funcName: str):
        if funcName == 'list':
            def decorator_list(func):
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    print(locals())

                return wrapper

            return decorator_list
        elif funcName == 'details':
            def decorator_details(func):
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    print('当前正在运行details...')

                return wrapper

            return decorator_details
