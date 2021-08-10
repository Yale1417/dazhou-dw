# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/22 下午5:02
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : ods_transform.py
# @Software: PyCharm
# @class : 数据转换　　－－－＞　对所有的现存属性 进行统一单位

"""
CREATE TABLE  dm_elec_all_goods_info(

    --- 项目维度
	id UUID COMMENT '用于所有插入记录',
	project_name String comment '搜索关键词',
	project_page UInt32 comment 'item所属wen页面',
	num_iid String comment '商品id',

	--- 时间维度
	time_year String comment '采集年份',
	time_mon String comment '月',
	time_day String comment '日',
	time_stamp DateTime64 comment '日期时间戳',

	--- 价格维度
	is_promotion UInt8 comment '0/1表示是否有折扣',
	discount_level UInt8 comment '折扣等级',
	price Float64 comment '当前价格',
	orginal_price Float64 comment '原价',

	--- 商品描述维度
	pic_num UInt16 comment '商品主图图片数量',
	video_num UInt16 comment '商品主图视频数量',
	props_num UInt8 comment '商品选择规格数量',
    title String comment '商品名称',
    extract_word String comment '商品名称关键词',
    extract_specis Float64 comment '商品体积规格',
    extract_cardinal UInt8 comment '商品规格数量',

    --- 店铺维度
    seller String comment '店铺名称',
    brand String comment '品牌名称',
    platform String comment '所属平台',

    --- 商品类别标签维度
    cid String comment '所属二级分类',
    root_cid String comment '所属一级分类',

    --- 库存维度
    num UInt32 comment '当前商品库存',
    num_level String comment '库存等级',

    --- 商品地域维度
    delivery_provins String comment '商品发货省份',
    delivery_city String comment '商品发货城市',
    delivery_city_level String comment '城市所属等级',
    production_provins String comment '产品生产省份',
    production_city String comment '产品生产城市',
    company_phone String comment '生产企业联系方式',
    origin String comment '进出口情况',

    --- 商品配料维度
    ingredients String comment '商品配料表',
    sugar UInt8 comment '商品是否含糖',

    --- 商品规格维度
    pack String comment '商品包装',
    net_content String comment '净含量等级',
    solid_content String comment '固形物含量等级',
    shelf String comment '保质期',
    protein String comment '蛋白质含量'

)
-- 表设置
ENGINE=MergeTree()
PRIMARY KEY id
-- 分区规则：按照 商品关键词、平台、月
PARTITION BY (project_name,time_year,time_mon)
order by id;
"""
from tools_class import Tools_Class
from clean.sequence_speci import Sequence_Speci
from etl.ods_load import Ods_Load


class Ods_Transform(object):
    # 1.字段转换
    @classmethod
    def transform_all(cls, data):
        i = data
        print('\n===> 数据正在转换.....\n')
        extract_specis = Tools_Class.tools_regular_digital(string=i['extract_specis'])
        extract_cardinal = Tools_Class.tools_regular_digital(string=i['extract_cardinal'])
        produc_add = Tools_Class.tools_spi_city(cityName=i['delivery_address'])
        production_provins = produc_add['province']
        production_city = produc_add['city']
        production_city_level = produc_add['city_level']
        pack = Sequence_Speci.speci_pack(i['pack'])
        net_content = Sequence_Speci.speci_net(i['net_content'])
        solid_content = Sequence_Speci.speci_shelf_level(i['solid_content'])
        storage_way = Sequence_Speci.speci_storage_way(i['storage_way'])

        transform_info = {
            # 项目维度
            'project_name': i['project_page'],
            'num_iid': i['num_iid'],
            'project_page': int(i['project_page']),

            # 时间维度
            'time_year': i['time_year'],
            'time_mon': i['time_month'],
            'time_day': i['time_day'],
            'time_stamp': i['time_stamp'],

            # 价格维度
            'is_promotion': i['is_promotion'],
            'discount_level': i['discount_level'],
            'price': i['price'],
            'orginal_price': i['orginal_price'],

            # 商品描述
            'pic_num': i['pic_num'],
            'video_num': i['video_num'],
            'props_num': i['props_num'],
            'title': i['title'],
            'extract_word': i['extract_word'],
            'extract_specis': extract_specis,
            'extract_cardinal': extract_cardinal,

            # 店铺维度
            'seller': i['seller'],
            'brand': i['brand'],
            'platform': i['platform'],

            # 商品类别标签维度
            'cid': i['cid'],
            'root_cid': i['root_cid'],

            # 库存维度
            'num': i['num'],
            'num_level': i['num_level'],

            # 商品地域维度
            'delivery_provins': i['delivery_provins'],
            'delivery_city': i['delivery_city'],
            'delivery_city_level': i['delivery_city_level'],
            'production_provins': production_provins,
            'production_city': production_city,
            'production_city_level': production_city_level,
            'delivery_company': i['delivery_company'],
            'company_phone': i['company_phone'],
            'origin': i['origin'],

            # 商品配料维度
            'ingredients': i['ingredients'],
            'sugar': Sequence_Speci.speci_sugar(i['sugar']),

            # 商品规格维度
            'pack': pack,
            'net_content': net_content,
            'solid_content': solid_content,
            'shelf': i['shelf'],
            'storage_way': storage_way,
            'item_speci': i['item_speci'],

            # 销售维度
            'sales': i['sales']

        }
        print(len(transform_info))
        print(transform_info)

    # 2.list转换 ----> dwd_elec_etl_list
    @classmethod
    def transform_list(cls, data: dict):
        # 规格清洗
        data['extract_specis'] = Tools_Class.tools_regular_digital(string=data['extract_specis'])
        data['extract_cardinal'] = Tools_Class.tools_regular_digital(string=data['extract_cardinal'])
        # 数据加载---mysql
        Ods_Load.load_mysql_insert(databaseName='dwd_dws_electricity_etl',
                                   collectionName='dwd_electricity_etl_list_202107',
                                   data=data)

    # 3.数据类型检验
