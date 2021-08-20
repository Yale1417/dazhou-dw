# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/1 下午4:19
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : kafka.py
# @Software: PyCharm
# @class :  用于redis 的消息队列  -->生产消费者

import redis


class RedisMQ(object):
    def __init__(self):
        self.redis_mq = redis.Redis(host='127.0.0.1', port='6379', db=1, decode_responses=True, charset='UTF-8',
                                    encoding='UTF-8',health_check_interval=30)

    # ==> 1. Producer
    def redis_push(self, name: str, push_msg: dict):
        try:
            self.redis_mq.lpush(name, str(push_msg))
            return 'ok'
        except Exception as e:
            print('==> redis入队列出现问题:', e)
            return None

    # ==> 2.Consumer
    def redis_pop(self, name: str):
        try:
            pop_value = self.redis_mq.rpop(name)
            return pop_value
        except Exception as e:
            print('==> redis出队出现问题', e)
            return None

    # ==> 3.查询队列的长度
    def redis_len(self, name:str):
        count = self.redis_mq.llen(name)
        return count

    # ==> 4.获取所有的key
    def redis_getkey(self):
        keys = self.redis_mq.scan_iter()
        return list(keys)


    # ==> 5.清空队列
    def redis_delete(self, redis_key):
        self.redis_mq.delete(redis_key)
        return 'ok'

    # ==> 6.url 去重集合
    def redis_set(self, msg):
        pass





