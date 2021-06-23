# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/4 下午1:59
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : __init__.py.py
# @Software: PyCharm
# @PS : run main class

from elec import Elec

# keywords = ['即食燕窝','鲜炖燕窝','即食花胶','即食鲍鱼','即食海参','佛跳墙','玻尿酸饮品','燕窝多肽',
#            '冻干燕窝','鱼胶冻']
Elec().api_search(keyword='即食花胶', platform='jingdong',is_all=True)

