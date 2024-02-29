#!/usr/local/bin/python3
# coding: utf-8


__author__ = "Benny <benny.think@gmail.com>"
from distutils.core import setup

setup(
    name="deye",
    version="0.0.5",
    py_modules=["deye", "cli", "config", "mqtt", "storage"],
    url="https://github.com/BennyThink/deye",
    install_requires=["Click", "requests", "paho-mqtt"],
    entry_points="""
        [console_scripts]
        deye=cli:main
    """,
    description="deye controller",
    long_description="use python to control your deye device",
    author="BennyThink",
    author_email="benny.think@gmail.com",
    python_requires=">=3.6.0",
    license="MIT",
)
