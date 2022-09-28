#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/16 14:47
# @Author: william.cao
# @File  : comm.py
import random
import time

from common.read_file import ReadFile


def to_obtain_url_param_method(saas_type, api_name, api, token):
    """
    根据接口获取URL,param,method,header
    :param api_name：yaml定义接口名称
    :param api：yaml对应的api
    :param token 登陆返回的token
    :param saas_type：业务线缩写 如：mss
    :return:
    """
    # 获取yaml接口数据
    saas_type = saas_type.upper()

    yaml_data = ReadFile().read_yaml(saas_type)[saas_type]

    # 获取url
    url = yaml_data['host'] + yaml_data[api_name][api]

    # 获取method
    method = yaml_data[api_name]['method']

    # 获取更新header下token的信息
    yaml_data[api_name]['headers']['Authorization'] = token
    headers = yaml_data[api_name]['headers']
    return {'url': url, 'method': method, 'headers': headers}


def random_phone():
    """
    随机生成一个电话号码
    :return:
    """
    pre_list = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
                "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    random_pre = random.choice(pre_list)
    number = "".join(random.choice("0123456789") for i in range(8))
    phone_num = random_pre + number
    return str(phone_num)


def get_time_stamp():
    """
    获取当前时间的毫秒级
    :return:
    """
    t = time.time()
    # 毫秒级时间戳
    now_time = lambda: int(round(t * 1000))
    return now_time()


if __name__ == '__main__':
    print(get_time_stamp())
