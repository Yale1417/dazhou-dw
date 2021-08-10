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
#
# import re
#
# string = '小仙炖鲜炖燕窝周套餐45g*7瓶 冰糖/无糖孕妇食品正品即食礼盒'
#
# new_string = re.findall(r'\d+[a-z A-z]\*\d+[\u4e00-\u9fa5]',string)
#
#
# from tools_class import Tools_Class
#
# print(Tools_Class.tools_spi_city('gjhghujghjg'))

# item = {'project_name': 1, 'num_iid': '561870297126', 'project_page': 1, 'time_year': '2021', 'time_mon': '07',
#         'time_day': '05', 'time_stamp': 1625414400, 'is_promotion': 1, 'discount_level': 70, 'price': 279.0,
#         'orginal_price': 398.0, 'pic_num': 5, 'video_num': 0, 'props_num': 0,
#         'title': '泰国双莲即食燕窝孕妇木糖醇75mlx6瓶旗舰店官网正品进口礼盒2.8%', 'extract_word': '燕窝/孕妇/木糖醇/正品/礼盒', 'extract_specis': 75,
#         'extract_cardinal': 6, 'seller': 'twinlotus海外旗舰店', 'brand': 'Twin Lotus/双莲', 'platform': 'tmall',
#         'cid': '124128007', 'root_cid': '50020275', 'num': 0, 'num_level': '紧张', 'delivery_provins': '',
#         'delivery_city': '', 'delivery_city_level': '', 'production_provins': '', 'production_city': '',
#         'production_city_level': '', 'delivery_company': 'Twin Lotus Co., Ltd.', 'company_phone': '',
#         'origin': '泰国', 'ingredients': '', 'sugar': 0, 'pack': '瓶装', 'net_content': 75, 'solid_content': '',
#         'shelf': '', 'storage_way': 730, 'item_speci': '', 'sales': 2054, 'id': 'generateUUIDv4()'}
#
#
# a = f'insert into test_1(id,test) VALUES {tuple(item.keys())}'
# print(a)


