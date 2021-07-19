# !/usr/bin/python3
# sudo /usr/bin/python "$@"
# -*- coding: utf-8 -*-
# @Time : 2021/6/4 下午3:52
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : yesy的萨.py
# @Software: PyCharm
# @class :

# from mongo_db import Mongo
# from clean.tools_class import Tools_Class
# import time

# import hanlp
# import os
# #
#
# text = '官雀庄燕窝饮料冲泡即食孕妇正品金丝燕冰糖鲜炖燕窝羹15g*6袋'
# os.environ["CUDA_VISIBLE_DEVICES"] = '1'
# HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
# nlp_str = HanLP(text,taks=['dep','ner',])
# print(nlp_str)

# import paddlehub as hub
#
# # load model
# senta = hub.Module(name="senta_lstm")
# # load skep model
# # senta = hub.Module(name="ernie_skep_sentiment_analysis")
#
# # text
# test_text = [
#     "不错呦",
#     "哎，一般"
# ]

import re

string = '小仙炖鲜炖燕窝周套餐45g*7瓶 冰糖/无糖孕妇食品正品即食礼盒'

new_string = re.findall(r'\d+[a-z A-z]\*\d+[\u4e00-\u9fa5]',string)

