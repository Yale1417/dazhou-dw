# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/5 下午2:46
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : sequence_desc.py
# @Software: PyCharm
# @class : 所有商品简介的验证

"""
字段说明：
1.desc_id ---->数据库自增
2.pic_num
3.video_num
4.title
5.props_num
"""

from tools_class import Tools_Class


class Sequence_Desc(object):

    # ==> 1. 商品详情图片数
    @classmethod
    def sequence_pic_nums(cls, pic_list, video_list, props_list, title):
        _func = (lambda x: x if (x is not None) else 0)
        pic_list = _func(pic_list)
        video_list = _func(video_list)
        props_list = _func(props_list)
        # 提取关键词
        extract_keyword = []
        extract_word = Tools_Class.tools_nlp_nn(title=title, )
        han_tok = extract_word['tok/fine']
        han_pos = extract_word['pos/ctb']
        for tok, pos in zip(han_tok, han_pos):
            if pos == 'NN':
                extract_keyword.append(tok)
        keyword_str = '/'.join(extract_keyword)
        # 规格 /单位提取  ---->cardinal数量
        extract_specis = Tools_Class.tools_regular_str(string=title,
                                                       _re=r'\d+[a-z A-z]+',)[0]
        extract_cardinal = Tools_Class.tools_regular_str(string=title,
                                                         _re=r'\d+[\u4e00-\u9fa5]')[0]
        desc_latitude = {'pic_num': len(pic_list),
                         'video_num': len(video_list),
                         'props_num': len(props_list),
                         'title': title,
                         'extract_word': keyword_str,
                         'extract_specis':extract_specis,
                         'extract_cardinal':extract_cardinal,
                         }
        print(desc_latitude)

    # ==> 2.商品简介
    @classmethod
    def sequence_title(cls, title):
        pass
