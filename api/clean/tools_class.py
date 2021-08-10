# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/13 下午2:05
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : public_class.py
# @Software: PyCharm
# @class : 工具类  --> md5转换/日期/关键词提取
import hashlib
import hanlp
import os
import re


class Tools_Class(object):

    # 1.MD5  ---->对多个任意参数进行合并
    @classmethod
    def tools_md5(cls, **kwargs):
        md5_str = hashlib.md5(bytes(''.join(list(map(lambda x: str(x), kwargs.values()))),
                                    encoding='utf-8',
                                    )).hexdigest()
        return md5_str

    #  2. date -->自动创建时间 自动加入时间戳、年份、月份
    @classmethod
    def tools_date(cls, ):
        pass

    # 3. NN 提取   tasks=['tok', 'pos', 'dep']
    #   地名、品牌 -->ner/msra
    @classmethod
    def tools_nlp_nn(cls, title: str):
        os.environ["CUDA_VISIBLE_DEVICES"] = '1'
        HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
        han_nn = HanLP(title, ['dep', 'tok', 'pos/ctb', 'ner/msra'])
        return han_nn

    # 4. 根据词性名称提取 --> ["余仁生", "PERSON", 0, 1], ========> 弃用，提取不稳定
    # PERSON / LOCATION / DECIMAL / PERCENT / MEASURE
    # @classmethod
    # def tools_nlp_dismantling(cls, attName: list, keyword_list):
    #     if keyword_list:
    #         for _ags in attName:
    #             _list = list(map(lambda x: x if _ags in x else False, keyword_list))
    #             for word in _list:
    #                 if word:
    #                     return word[0]
    #     else:
    #         print('===> 不存在ner/msra属性！')
    #         return ''

    # 5. 正则获取
    @classmethod
    def tools_regular_str(cls, string, _re):
        new_string = re.findall(_re, string)
        if new_string:
            return new_string
        else:
            return ['']

    # 6. 根据地名分割省份和城 并 返回城等级
    @classmethod
    def tools_spi_city(cls, cityName):

        if cityName:
            with open('clean/json_file/city_name.json', 'r') as f:
                city_json = eval(f.read())

            with open('clean/json_file/city_level.json', 'r') as r:
                city_level = eval(r.read())

            for city in city_json:
                set1 = set(city['name'])
                set2 = set(cityName)
                if len(set1 & set2) > 1:
                    # 城市分割
                    if city['name'] in ['上海', '北京', '重庆', '天津']:
                        _province = city['name']
                        _city = city['name']
                    else:
                        _province = city['name']
                        _city = cityName.replace(city['name'], '')
                    """
                    注意：浙江杭州　->需要匹配浙江杭州市
                    """
                    # 城市等级
                    for level in city_level:
                        for _city_level in city_level[level]:
                            if _city_level in _city:
                                reslut_level = level
                                city_info = {
                                    'province': _province,
                                    'city': _city_level,
                                    'city_level': reslut_level,
                                }
                                return city_info

                            city_info = {
                                'province': _province,
                                'city': _city,
                                'city_level': '',
                            }
                            return city_info
                else:
                    city_info = {
                        'province': '',
                        'city': '',
                        'city_level': '',
                    }
                    return city_info
        else:
            city_info = {
                'province': '',
                'city': '',
                'city_level': '',
            }
            return city_info



    # 7. 正则获取数字
    @classmethod
    def tools_regular_digital(cls, string):
        digital = ''.join(re.findall(r'\d+', string))
        if digital:
            return int(digital)
        else:
            return 0
