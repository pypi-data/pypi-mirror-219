#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: notmmao@gmail.com
Date: 2022-06-02 10:11:48
LastEditors: notmmao@gmail.com
LastEditTime: 2023-04-11 18:25:02
Description: 
'''
import os
import time
import json
import datetime
import argparse
import hashlib
from typing import Union, Dict

import can


def now():
    n = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return n


def save_json(tag, data: dict):
    n = now()
    fn = f"json/{tag}_{n}.json"
    with open(fn, "w+", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"save {fn} success")


def filter_uds(bus: can.BusABC):
    filters = [
        {"can_id": 0x700, "can_mask": 0xf00, "extended": False},
    ]
    bus.set_filters(filters)


def filter_sk(bus: can.BusABC):
    filters = [
        {"can_id": 0x700, "can_mask": 0xf00, "extended": False},
        # {"can_id": 0x40B, "can_mask": 0xfff, "extended": False},
        {"can_id": 0x456, "can_mask": 0xfff, "extended": False},
        {"can_id": 0x45c, "can_mask": 0xfff, "extended": False},
        {"can_id": 0x47d, "can_mask": 0xfff, "extended": False},
        {"can_id": 0x47f, "can_mask": 0xfff, "extended": False},
        # {"can_id": 0x2EA, "can_mask": 0xfff, "extended": False},
    ]
    bus.set_filters(filters)


def parser_bus(t: str):
    if t == "vector":
        bus = can.interface.Bus(
            bustype='vector', channel=0, app_name="python_can", fd=True)
    elif t == "vector0":
        bus = can.interface.Bus(
            bustype='vector', channel=0, app_name="python_can", fd=True)
    elif t == "vector1":
        bus = can.interface.Bus(
            bustype='vector', channel=1, app_name="python_can", fd=True)
    elif t.startswith("vcan"):
        bus = can.interface.Bus(bustype='socketcan', channel=t, bitrate=500000)
    elif t.startswith("can"):
        bus = can.interface.Bus(bustype='socketcan', channel=t, bitrate=500000)
    else:
        bus = can.interface.Bus(bustype='virtual')
    return bus


def parser_canid(id):
    # print(id)
    try:
        canid = int(id)
    except ValueError:
        canid = int(id, 16)

    return canid


def parser_hex(data: str):
    data = data.replace(" ", "")
    data = bytearray.fromhex(data)
    return data


def common_parser(description: str = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-l', '--log', help='log文件')
    parser.add_argument('-t', '--txid', default=0x707, type=parser_canid,
                        help='Tester tx id')
    parser.add_argument('-r', '--rxid', default=0x717, type=parser_canid,
                        help='Tester rx id')
    parser.add_argument('-v', '--vin', default="LVTDB21B6ND167534",
                        help='VIN')
    parser.add_argument('-b', '--bus', type=parser_bus, default='vector')
    parser.add_argument('--app-name', default='python_can')
    parser.add_argument('--busses',  type=parser_bus, nargs="+")
    parser.add_argument('-d', '--dbc', default="gp01.dbc")
    parser.add_argument('--data', type=parser_hex)
    parser.add_argument('--mask', type=parser_canid)

    parser.add_argument('-a', '--action')
    parser.add_argument('-p', '--platform',
                        choices=["m1e", "t18p", "m1e_tenpao"], default="m1e")

    return parser


def get_input(dump=False) -> Union[Dict, None]:
    '''从环境变量获取客户端传来的input参数

    :param bool dump: 是否打印输入字符串, defaults to False
    :return None or dict: None或者解析后的dict类型参数
    '''
    input = os.getenv('input')
    if input is not None:
        if dump:
            print(input)
        input.replace('\\', '\\\\')
        input = json.loads(input)

    return input


# 一个装饰器, 在函数执行前后打印日志
def run_script(func):
    def wrapper(*args, **kwargs):
        try:
            print(f"开始")
            result = func(*args, **kwargs)
            print(f"结束")
        except Exception as e:
            print(e)
            exit(-1)
        return result
    return wrapper


def md5file(fn):
    '''计算文件的md5值

    :param function fn: 要计算md5值的文件
    :return str: MD5摘要值, hex格式
    '''
    md5 = hashlib.md5()
    with open(fn, "rb") as f:
        while True:
            d = f.read(4096)
            if not d:
                break
            md5.update(d)
        return md5.hexdigest()


def debounce(wait):
    def decorator(fn):
        last_call_time = 0

        def debounced(*args, **kwargs):
            nonlocal last_call_time

            elapsed_time = time.time() - last_call_time
            if elapsed_time < wait:
                return None

            result = fn(*args, **kwargs)
            last_call_time = time.time()

            return result
        return debounced
    return decorator


__version__ = '1.0.0'
__author__ = 'notmmao@gmail.com'


def main():
    parser = common_parser("hello")
    args = parser.parse_args()
    print(args)


if __name__ == '__main__':
    main()
