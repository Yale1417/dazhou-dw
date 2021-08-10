# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/28 下午5:11
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : clickhouse_dw.py
# @Software: PyCharm
# @class : clickhouse 操作
from abstract.db_base import DB_BASE
from clickhouse_driver import Client


class ClickHouse(DB_BASE):
    host = '127.0.0.1'
    port = 9004
    _user = 'default'
    _pass = 'ddfc272d99a308192ec5961f06133b14b56d2d89ae70ecb02d4acf40d21d1692'
    elec_database = 'dm_elce_goods_statis_1m'
    send_receive_timeout = 20

    # 连接
    def __init__(self):
        connectConf = {'host': '127.0.0.1', 'port': 9000,
                       'send_receive_timeout': self.send_receive_timeout,
                       'database': self.elec_database}
        self.conn = Client(**connectConf)


    # 2. 插入
    def db_insert(self):
        item = {'project_name': 1, 'num_iid': '561870297126', 'project_page': 1, 'time_year': '2021', 'time_mon': '07',
                'time_day': '05', 'time_stamp': 1625414400, 'is_promotion': 1, 'discount_level': 70, 'price': 279.0,
                'orginal_price': 398.0, 'pic_num': 5, 'video_num': 0, 'props_num': 0,
                'title': '泰国双莲即食燕窝孕妇木糖醇75mlx6瓶旗舰店官网正品进口礼盒2.8%', 'extract_word': '燕窝/孕妇/木糖醇/正品/礼盒', 'extract_specis': 75,
                'extract_cardinal': 6, 'seller': 'twinlotus海外旗舰店', 'brand': 'Twin Lotus/双莲', 'platform': 'tmall',
                'cid': '124128007', 'root_cid': '50020275', 'num': 0, 'num_level': '紧张', 'delivery_provins': '',
                'delivery_city': '', 'delivery_city_level': '', 'production_provins': '', 'production_city': '',
                'production_city_level': '', 'delivery_company': 'Twin Lotus Co., Ltd.', 'company_phone': '',
                'origin': '泰国', 'ingredients': '', 'sugar': 0, 'pack': '瓶装', 'net_content': 75, 'solid_content': '',
                'shelf': '', 'storage_way': 730, 'item_speci': '', 'sales': 2054, 'id': 'generateUUIDv4()'}

        # 增加uuid
        # 拆解

        _sql = f"INSERT INTO dm_elec_all_goods_info ({','.join(item)}) VALUES {tuple(item.values())}"
        self.conn.execute(_sql)

    # 3. 查询A
    def db_query(self, db, query_sql):
        ans = db.execute(query_sql)
        print(ans)

    # 4. 更新
    def db_update(self, data):
        pass


client = ClickHouse().db_insert()
# ClickHouse().db_query(db=client, query_sql=test)
