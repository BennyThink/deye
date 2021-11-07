#!/usr/local/bin/python3
# coding: utf-8

# deye - storage.py
# 11/6/21 19:01
#

__author__ = "Benny <benny.think@gmail.com>"

import dbm
import json
import logging

from config import apply_log_formatter

apply_log_formatter()


class Storage:
    def insert(self, key: "str", value: "dict"):
        pass

    def delete(self, key: "str"):
        pass

    def select(self, key: "str"):
        pass

    def update(self, key: "str", value: "dict"):
        pass


class DBMStorage(Storage):
    def __init__(self, config_path):
        self.db = dbm.open(config_path, 'c')

    def __del__(self):
        self.db.close()

    @staticmethod
    def json_dumps(value):
        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False)
        raise TypeError('value must be dict')

    @staticmethod
    def json_loads(value):
        try:
            return json.loads(value)
        except TypeError:
            return {}

    def insert(self, key: "str", value: "dict"):
        logging.debug("Writing to _db key %s", key)
        value = self.json_dumps(value)
        self.db[key] = value

    def delete(self, key: "str"):
        if self.select(key):
            del self.db[key]

    def update(self, key: "str", value: "dict"):
        value = self.json_dumps(value)
        self.db[key] = value

    def select(self, key: "str"):
        logging.debug("Reading from db key %s", key)
        return self.json_loads(self.db.get(key))
