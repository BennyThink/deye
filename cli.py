#!/usr/local/bin/python3
# coding: utf-8

# deye - cli.py
# 11/6/21 20:18
#

__author__ = "Benny <benny.think@gmail.com>"

import logging
import os

import click

from config import apply_log_formatter, config_path
from deye import E12A3Workflow
from mqtt import DYD_E12A3

apply_log_formatter()


@click.command()
@click.option("--username", prompt="请输入用户名", help="用户名", type=str)
@click.option("--password", prompt="请输入密码", help="密码", type=str, hide_input=True)
def user_login(username, password):
    logging.warning("Trying to login...")
    return E12A3Workflow(username, password)


if not os.path.exists(config_path):
    wf = user_login()
else:
    wf = E12A3Workflow()
dev_list = wf.device_list
max_index = len(dev_list["data"])
operation_map = {
    1: {"value": "开机", "function": "online"},
    2: {"value": "关机", "function": "offline"},
}
control = None


@click.command()
@click.option("--device_number", prompt="请输入要操作的设备序号", help="序号", type=click.IntRange(1, max_index))
def select_device(device_number):
    index = device_number - 1
    for i, v in operation_map.items():
        print(f"{i}. {v['value']}")
    product_id = dev_list["data"][index]["product_id"]
    device_id = dev_list["data"][index]["device_id"]
    global control
    control = DYD_E12A3(**wf.mtqq_info["data"], product_id=product_id, device_id=device_id)

    do_job()


@click.command()
@click.option('--op_number', prompt='选择操作', help='开机关机', type=int)
def do_job(op_number):
    func_name = operation_map.get(op_number)["function"]
    getattr(control, func_name)()


def main():
    for dev in dev_list["data"]:
        index = dev_list["data"].index(dev) + 1
        product_name = dev["product_name"]
        device_name = dev["device_name"]
        print(f"{index}. {product_name} {device_name}")
    select_device()


if __name__ == '__main__':
    main()
