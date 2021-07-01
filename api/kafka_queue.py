# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/7/1 下午4:19
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : kafka.py
# @Software: PyCharm
# @class : kafka配置

from confluent_kafka import Consumer, KafkaError


class Kafka(object):

    # 消息接收测试
    def kafka_consumer(self):
        consumer_conf = {'bootstrap.servers': '192.168.0.16:9092',
                         'group.id': '60997',
                         'auto.offset.reset': 'earliest'}

        consumer = Consumer(consumer_conf)
        consumer.subscribe(['latent'])
        #
        # print(consumer.list_topics(topic='latent'))
        # while True:
        #     msg = consumer.poll(1.0)
        #
        #     if msg is None:
        #         continue
        #     if msg.error():
        #         print("Consumer error: {}".format(msg.error()))
        #         continue
        #
        #     print('Received message: {}'.format(msg))
        #
        # consumer.close()


Kafka().kafka_consumer()
