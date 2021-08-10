# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/5 下午5:41
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : osd_clean.py
# @Software: PyCharm
# @class : osd层数据按照需求数据加载 --并清晰部分数据
import sequence_price
from db.mongo_db import Mongo
from clean.sequence_desc import Sequence_Desc
from clean.sequence_nick import Sequence_Nick
from clean.sequence_price import Sequence_Price
from clean.sequence_label import Sequence_Label
from clean.sequence_num import Sequence_Num
from clean.sequence_date import Sequence_Date
from clean.sequence_region import Sequence_Region
from clean.sequence_speci import Sequence_Speci
from etl.ods_transform import Ods_Transform
from clean.tools_class import Tools_Class


class Ods_Extract(object):

    def __init__(self, start_date, end_date, platform, keyword, isCustom=False):
        print(f'\n===> 数据正在加载.....【{keyword}】\n')
        self.start_date = start_date
        self.end_date = end_date
        self.platform = platform
        self.keyword = keyword
        self.isCustom = isCustom
        table = Mongo().mongo_get_tables()
        table_list = table['table_list']
        self.describe_info = Mongo.mongo_data_describe(tableName=table_list,
                                                       startDate=self.start_date,
                                                       endDate=self.end_date,
                                                       platform=self.platform,
                                                       keyword=self.keyword,
                                                       isCustom=self.isCustom)

    # 按按照时间规则抽取平台的数据   --->　根据不同的商品的关键词来过滤　--->聚合
    # 1.所有对应的数据加载
    def ods_extract_all(self):
        # 获取list+detials对应的
        finished_item = self.describe_info['finished_item']
        # 字段清洗
        for item in finished_item:
            try:
                item_page = item['page']
            except KeyError :
                item_page = 0
            # 1.项目维度
            project_latitude = {'project_name': self.keyword,
                                'project_page': item_page,
                                'num_iid': item['num_iid'],

                                }

            # 2.日期维度
            date_latitude = Sequence_Date.sequence_date(data=item)
            # 3.价格维度
            price_latitude = Sequence_Price.sequence_discount(item['public']['price'], item['public']['orginal_price'])

            # 4.商品简介维度
            desc_latitude = Sequence_Desc.sequence_pic_nums(pic_list=item['public']['item_imgs'],
                                                            video_list=item['public']['video'],
                                                            props_list=item['public']['props_list'],
                                                            title=item['title']
                                                            )
            # 5.店铺维度
            nick_latitude = Sequence_Nick.sequence_brand(data=item)

            # 6. 類別維度
            label_latitude = Sequence_Label.sequence_label(data=item)

            # 7. 库存维度
            num_latitude = Sequence_Num.sequence_num_level(data=item)

            # 8.地区维度
            region_latitude = Sequence_Region.sequence_get_city(data=item)

            # 9.规格清洗
            props_latitude = Sequence_Speci().sequence_speci(data=item)

            # 10.销量维度
            sales_latitude = {"sales": Sequence_Price.sequence_sales(sales=item['sales'])}
            all_latitude = project_latitude | date_latitude | price_latitude | desc_latitude | nick_latitude | \
                           label_latitude | num_latitude | region_latitude | props_latitude | sales_latitude

            print(all_latitude)
            return all_latitude

    # 2.对list进行加载处理
    def osd_extract_list(self):

        ods_list = self.describe_info['ods_list']
        for data in ods_list:
            try:
                item_page = data['page']
            except KeyError:
                item_page = 0
            # 1.项目维度 ---> 添加mysql_id  标识 (时间 + num_iid)
            project_latitude = {'project_name': self.keyword,
                                'project_page': item_page,
                                'num_iid': str(data['num_iid']),
                                'mysql_id': Tools_Class.tools_md5(id=data['num_iid'],
                                                                  date=data['request_date'])
                                }
            # 2.日期维度
            date_latitude = Sequence_Date.sequence_date(data=data)

            # 3.价格维度
            price_latitude = Sequence_Price.sequence_price(data['price'])

            # 4.商品简介维度
            desc_latitude = Sequence_Desc.sequence_title(title=data['title'])

            # 5.店铺维度
            seller_nick = Sequence_Nick.sequence_seller(data=data)
            nick_latitude = {
                'seller_nick': seller_nick,
                'platform' : data['platform']
            }
            # 6. 销售量
            sales_latitude = {"sales": Sequence_Price.sequence_sales(sales=data['sales'])}
            all_latitude = project_latitude | date_latitude | price_latitude | desc_latitude | nick_latitude \
                           | sales_latitude

            # 转换
            Ods_Transform.transform_list(data=all_latitude)
