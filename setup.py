#!/usr/local/bin/python3
# coding: utf-8

# deye - setup.py.py
# 11/7/21 10:15
#

__author__ = "Benny <benny.think@gmail.com>"

from setuptools import setup

setup(
    name='deye',
    version='0.0.3',
    py_modules=['deye','cli','config','mqtt','storage'],
    install_requires=[
        'Click',
        'requests',
        'paho-mqtt'
    ],
    entry_points='''
        [console_scripts]
        deye=cli:main
    ''',
)