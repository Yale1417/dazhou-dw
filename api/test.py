# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/6/4 下午3:52
# @Author : Latent
# @Email : latentsky@gmail.com
# @File : yesy的萨.py
# @Software: PyCharm
# @class :

import redis

import redis

publisher = redis.Redis(host='192.168.0.16', port=6379)
message = ""
channel = "test"
while message != "exit":
    message = input("")
    send_message = "Python : " + message
    publisher.publish(channel, send_message)
