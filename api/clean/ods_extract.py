# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/5 下午5:41
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : osd_clean.py
# @Software: PyCharm
# @class : osd层数据的导入、筛选
from db.mongo_db import Mongo
from clean.sequence_desc import Sequence_Desc
from clean.sequence_nick import Sequence_Nick
from clean.sequence_price import Sequence_Price
from clean.sequence_label import Sequence_Label
from clean.sequence_num import Sequence_Num
from clean.sequence_date import Sequence_Date

class Ods_Extract(object):

    def __init__(self):
        self.table = Mongo().mongo_get_tables()

    # 按按照时间规则抽取平台的数据   --->　根据不同的商品的关键词来过滤　--->聚合
    def ods_get_platform(self, start_date, end_date, platform, keyword, start_page, end_page, isCustom=False):
        table_list = self.table['table_list']
        describe_info = Mongo.mongo_data_describe(tableName=table_list,
                                                  start_page=start_page,
                                                  end_page=end_page,
                                                  startDate=start_date,
                                                  endDate=end_date,
                                                  platform=platform,
                                                  keyword=keyword,
                                                  isCustom=isCustom)
        finished_item = describe_info['finished_item']

        # 字段清洗
        for item in finished_item:
            # 1.项目维度
            project_latitude = {'project_name': keyword,
                                'project_page': item['page']
                                }

            # 2.日期维度
            date_latitude = Sequence_Date.sequence_date(data=item)
            # 3.价格维度
            # price_latitude = Sequence_Price.sequence_discount(item['public']['price'], item['public']['orginal_price'])

            # 4.商品简介维度
            # desc_latitude = Sequence_Desc.sequence_pic_nums(pic_list=item['public']['item_imgs'],
            #                                                 video_list=item['public']['video'],
            #                                                 props_list=item['public']['props_list'],
            #                                                 title=item['title']
            #                                                 )
            # 5.店铺维度
            # nick_latitude = Sequence_Nick.sequence_brand(data=item)

            # 6. 類別維度
            # label_latitude = Sequence_Label.sequence_label(data=item)

            # 7. 库存维度
            # num_latitude = Sequence_Num.sequence_num_level(data=item)
            print(date_latitude)

