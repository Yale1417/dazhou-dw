# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/5 下午5:29
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : sequence_nick.py
# @Software: PyCharm
# @class : 清晰店铺的相关信息
import hanlp


class Sequence_Nick(object):

    # 品牌提取
    @classmethod
    def sequence_brand(cls, data):
        if 'brand' in data:
            brand = data['brand']
            if len(brand) < 2:
                HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
                ner = HanLP(data['title'], tasks='ner/msra')
                print(ner)