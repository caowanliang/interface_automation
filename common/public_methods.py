#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/16 14:47
# @Author: william.cao
# @File  : public_methods.py
import functools
import itertools
import json
import os
import random
import time
from comm.read_file import ReadFile
from conftest import log


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


def retry(delays=(3, 10, 15), exceptions=(Exception, )):
    """
    重试装饰器
    :return:
    """
    def wrapper(function):
        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            problems = []
            for delay in itertools.chain(delays, [None]):
                try:
                    return function(*args, **kwargs)
                except exceptions as problem:
                    problems.append(problem)
                    if delay is None:
                        log.warning("在{num}次重试后，函数{func}失败. Exceptions: {p}".format(func=function.__name__, num=len(delays), p=problems))
                        raise
                    else:
                        log.warning("函数{func}失败的{expt_name}({expt_msg})。将在{delay}秒(s)内重试.".format(func=function.__name__, expt_name=type(problem).__name__, expt_msg=problem, delay=delay))
                        time.sleep(delay)
        return wrapped
    return wrapper

def json_read(json_file):
    """
    json文件读取
    :return:
    """
    open_file = os.path.join(os.path.dirname(os.path.dirname(__file__)) + json_file)
    with open(open_file, "r", encoding='utf-8') as jsonFile:
        read_data = json.load(jsonFile)
    return read_data

def json_edit(edit_data, json_file):
    """
    json文件修改
    :return:
    """
    open_file = os.path.join(os.path.dirname(os.path.dirname(__file__)) + json_file)
    with open(open_file, 'w', encoding='utf8') as fp:
        json.dump(edit_data, fp, indent=4, separators=(',', ': '), ensure_ascii=False)

