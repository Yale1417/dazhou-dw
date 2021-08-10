# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/28 下午5:22
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : base_db.py
# @Software: PyCharm
# @class : 所有数据库类的基类

from abc import ABCMeta, abstractmethod


class DB_BASE(metaclass=ABCMeta):

    # 2. 查询
    @abstractmethod
    def db_query(self, **kwargs):
        pass

    # 3. 插入
    @abstractmethod
    def db_insert(self, **kwargs):
        pass

    # 4.修改
    @abstractmethod
    def db_update(self, **kwargs):
        pass
