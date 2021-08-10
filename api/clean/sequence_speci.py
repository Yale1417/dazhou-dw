# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/21 下午2:47
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : sequence_speci.py
# @Software: PyCharm
# @class : 规格清洗

"""
1. delivery_address   ----> 生产地址
2. delivery_company   ----->生产企业
3. company＿phone   ----> 企业电话
4. pack ---> 包装方式
5. solid_content   ---->固形物含量
6. storage_way  ---->  贮存方式
7. net_content  ------> 净含量
8. props_brand  ------> 规格-品牌
9. origin   -----> 原产地
10. ingredients  ----> 配料表
11. sugar ----->   是否含糖
12. shelf  ------> 保质期
13. protein -----> 蛋白质含量
14. item_speci


"""
import re


class Sequence_Speci(object):

    def __init__(self):
        # 判断props属性的字典
        with open('./clean/json_file/set_props.json', 'r') as f:
            self.set_props = eval(f.read())
        # 根据关键词验证产品规格属性 ----> 标准字典
        with open('./clean/json_file/standard_props.json', 'r') as r:
            self.standard_props = eval(r.read())

    # 1. 规格提取
    def sequence_speci(self, data):
        props = data['public']['props']
        if props:
            props_info = Sequence_Speci().speci_props(props=props)
            return props_info
        else:
            props_info = {
                "delivery_address": '',
                "delivery_company": '',
                "company_phone": '',
                "pack": '',
                "solid_content": '',
                "storage_way": '',
                "net_content": '',
                "props_brand": '',
                "origin": '',
                "ingredients": '',
                "sugar": '',
                "protein": '',
                "shelf": '',
                "item_speci": '',
            }
            return props_info

    # ---> props_list 属性提取
    def speci_props(self, props: list):
        speci_info = {}
        for item in props:
            for key in self.set_props:
                for i in list(self.set_props[key].values())[0]:
                    if i in item['name']:
                        speci_info[list(self.set_props[key].keys())[0]] = item['value']

        # 验证speci_info
        props_info = {
            "delivery_address": '',
            "delivery_company": '',
            "company_phone": '',
            "pack": '',
            "solid_content": '',
            "storage_way": '',
            "net_content": '',
            "props_brand": '',
            "origin": '',
            "ingredients": '',
            "sugar": '',
            "protein": '',
            "shelf": '',
            "item_speci": '',
        }

        diff_set = set(props_info) - set(speci_info)
        if diff_set:
            for i in diff_set:
                speci_info[i] = ''
            return speci_info
        else:
            return speci_info

    # 2. 包装清洗
    @classmethod
    def speci_pack(cls, string):
        if string:
            # 规格设置
            dict_pack = {
                "盒装": "盒",
                "罐装": "罐",
                "瓶装": "瓶",
                "袋装": "袋",
                "碗装": "碗"
            }
            for pack in dict_pack:
                if dict_pack[pack] in string:
                    return pack
                else:
                    return string
        else:
            return ''
    # 3. 固形物含量等级
    @classmethod
    def speci_shelf_level(cls, string):
        try:
            shelf = re.findall(r"\d+", string)[-1]
            if shelf:
                shelf = int(shelf)
            else:
                shelf = ''
            if shelf < 30:
                return '低'
            elif 30 <= shelf <= 60:
                return '中'
            else:
                return '高'
        except IndexError:
            return ''

    # 4. 燕窝净含量
    @classmethod
    def speci_net(cls, string):
        try:
            shelf = re.findall(r"\d+", string)[-1]
            if shelf:
                shelf = int(shelf)
                return shelf
            else:
                shelf = ''
                return shelf
        except IndexError:
            return ''

    # 5. 保质期
    @classmethod
    def speci_storage_way(cls, string):
        try:
            shelf_list = int(''.join(re.findall(r'\d', string)))
            if '年' in string:
                return shelf_list*365
            elif '月' in string:
                return shelf_list*30
            elif '日' and '天':
                return shelf_list
            else:
                return shelf_list
        except Exception as e:
            print(e)
            return ''


    # 6. 是否含糖
    @classmethod
    def speci_sugar(cls, string):
        if '不' and '非' and '无' in string:
            return 0
        else:
            return 1







