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
    def kill_list_none(cls, json):
        if json:
            return json
        else:
            return None









