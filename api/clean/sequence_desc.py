# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/5 下午2:46
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : sequence_desc.py
# @Software: PyCharm
# @class : 所有商品简介的验证
from hanlp_restful import HanLPClient


class Sequence_Desc(object):

    # ==> 1. 商品详情图片数
    @classmethod
    def sequence_pic_nums(cls, pic_list: list, video_list: list, props_list: list):
        return len(pic_list), len(video_list), len(props_list)

    # ==> 2.商品简介
    @classmethod
    def sequence_title(cls, title):
        pass

