# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/19 下午6:06
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : sequence_label.py
# @Software: PyCharm
# @class : 类别

"""
字段说明：
1.nick_id ---->数据库自增
2.nick_name
3.nick
4.brand
5.company_name
6.platform
"""


class Sequence_Label(object):

    # 产品分类标签
    @classmethod
    def sequence_label(cls, data):
        # 只有淘宝和京东有类别
        platforms = ['jingdong', 'taobao']
        platform = data['platform']
        if platform in platforms:
            cid = data['public']['cid']
            root_id = data['public']['rootCatId']
        else:
            cid = ''
            root_id = ''

        label_info = {'cid': cid,
                      'root_cid': root_id
                      }
        return label_info
