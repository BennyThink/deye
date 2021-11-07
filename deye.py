#!/usr/local/bin/python3
# coding: utf-8

# untitled - deye.py
# 11/6/21 15:34
#

__author__ = "Benny <benny.think@gmail.com>"

import logging
import os

import requests

from config import (DEVICE_LIST_URL, LOGIN_URL, MTQQ_INFO, REFRESH_URL,
                    USER_INFO, apply_log_formatter, config_path)
from storage import DBMStorage

apply_log_formatter()


class Workflow:
    pass


class E12A3Workflow(Workflow):
    # get token from username and password, make sure it's valid
    def __init__(self, username: "str" = None, password: "str" = None):
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": "DeyeApp/2.2.6 (iPhone; iOS 15.1; Scale/3.00)"})
        self._db = DBMStorage(config_path)

        self._username = username
        self._password = password
        self.token = None

        self.__login()

    def __login(self):
        select = self._db.select("login")
        self.token = select.get("data", {}).get("token")
        self._session.headers.update({"Authorization": f"JWT {self.token}"})
        if not self.__validate():
            self.__app_login()

    def __validate(self):
        if self._session.get(USER_INFO).json()["meta"]["code"] != 0:
            logging.critical("⚠️ Invalid user, please check your username or password.")
            return False
        return True

    def __app_login(self):
        logging.debug("Login to app...")
        data = requests.post(
            LOGIN_URL,
            data={
                "loginname": self._username,
                "password": self._password,
                "appid": "a774310e-a430-11e7-9d4c-00163e0c1b21",
                "extend": '{"pushtype": "None"}'}
        ).json()

        if data["meta"]["code"] != 0:
            logging.error("❌ Login failed, please check your username or password.")
            os.remove(config_path)
            return

        self._db.insert("login", data)
        self.token = data["data"]["token"]
        self._session.headers.update({"Authorization": f"JWT {self.token}"})

    def __app_refresh_token(self):
        self._session.headers.update({"Authorization": f"JWT {self.token}"})
        data = requests.post(REFRESH_URL).json()
        self._db.insert("login", data)

    @property
    def device_list(self):
        logging.debug("Get device list...")
        data = self._session.get(DEVICE_LIST_URL).json()
        return data

    @property
    def mtqq_info(self):
        logging.debug("Get mtqq info...")
        data = self._session.get(MTQQ_INFO).json()
        # TODO or add it in db? Since it won't change frequently
        #  self._db.insert("mtqq", data)
        return data

    def __str__(self):
        return f"User {self._username} Token {self.token}"


if __name__ == '__main__':
    username = os.getenv("username")
    password = os.getenv("password")
    dev = E12A3Workflow(username, password)
    print(dev.device_list)
