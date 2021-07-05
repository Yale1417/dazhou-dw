# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/4 下午3:52
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : yesy的萨.py
# @Software: PyCharm
# @class :

import hanlp
text = '邦成即食人参燕窝10瓶/礼盒装中老年 成人滋补品节日送礼 送朋友'
HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)

print(HanLP(text, tasks='ner/msra'))
