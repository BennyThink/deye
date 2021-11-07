#!/usr/local/bin/python3
# coding: utf-8

# deye - config_path.py
# 11/6/21 19:20
#

__author__ = "Benny <benny.think@gmail.com>"

import logging
import os

config_path = os.path.join(os.getenv("HOME"), ".deye.dbm")
BASE_URL = "https://api.deye.com.cn/v3/enduser/"

LOGIN_URL = f"{BASE_URL}login/"
REFRESH_URL = f"{BASE_URL}refreshToken/"
DEVICE_LIST_URL = f"{BASE_URL}deviceList/?app=new/"
USER_INFO = f"{BASE_URL}userInfo/"
MTQQ_INFO = f"{BASE_URL}mqttInfo/"


def apply_log_formatter():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s %(filename)s:%(lineno)d %(levelname).1s] %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )