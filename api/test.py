# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/4 下午3:52
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : yesy的萨.py
# @Software: PyCharm
# @class :

import hanlp
text = '冰糖官燕:即食冰糖官燕70g*8礼盒葡萄'
HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)

print(HanLP(text, ))
