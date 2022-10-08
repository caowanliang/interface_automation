#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/12 19:42
# @Author: william.cao
# @File  : conftest.py

import pytest

from common.log import Log
from common.public_methods import json_read, to_obtain_url_param_method
from common.request import RunMethod

# 初始化请求
log = Log()
mss_request = RunMethod()

@pytest.fixture(scope="class")
def login_mss():
    """
    登陆Mss运营平台超管账号
    :return: access_token
    """
    global id_token
    date = json_read('/data/mss_data/mss_login_data/mss_login_super_root.json')
    # 读取登陆数据
    web_list_date = to_obtain_url_param_method(saas_type='MSS', api_name='mss_login', api='api', token='token')

    try:
        login_result = mss_request.run_main(method=web_list_date['method'], url=web_list_date['url'], json=date, headers=web_list_date['headers'])
        id_token = login_result.json()
        log.info('登陆返回结果{}'.format(id_token))
    except Exception as e:
        log.error('登录报错{}'.format(e))
    yield id_token['data']['access_token']

    # 读取退出登陆数据
    web_list_date = to_obtain_url_param_method(saas_type='MSS', api_name='mss_login_out', api='api', token='token')
    try:
        login_out_result = mss_request.run_main(method=web_list_date['method'], url=web_list_date['url'], json={"token":id_token['data']['access_token']}, headers=web_list_date['headers'])
        log.info('退出登陆返回结果{}'.format(login_out_result.json()))
    except Exception as e:
        log.error('退出登录报错{}'.format(e))


@pytest.fixture(scope="function")
def create_and_delete_report(login_mss):
    """
    新增并删除生成报告
    :param login_mss: token值
    :return: 生成报告的id值
    """
    date = json_read('/data/mss_data/mss_report_center_data/create_mouth_report_date.json')

    # 获取接口请求数据
    api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_record_create', api='api', token=login_mss)

    # 生成月报
    creat_report_result = mss_request.run_main(method=api_date['method'], url=api_date['url'], json=date, headers=api_date['headers'])
    log.info("生成月报返回结果：{}".format(creat_report_result.json()))

    yield creat_report_result.json()['data'][0]

    # 删除报告
    api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_record_remove_by_ids', api='api', token=login_mss)
    report_delete_result = mss_request.run_main(method=api_date['method'], url=api_date['url'] + creat_report_result.json()['data'][0], json={}, headers=api_date['headers'])
    log.info("删除报告结果：{}".format(report_delete_result.json()))


@pytest.fixture(scope="function")
def add_and_delete_subscribe_report(login_mss):
    """
    新增并删除订阅报告
    :param login_mss: token值
    :return: 生成报告的id值
    """
    date = json_read('/data/mss_data/mss_report_center_data/report_subscribe_add_date.json')
    # 获取接口请求数据
    api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_subscribe_add', api='api', token=login_mss)
    # 生成订阅报告
    add_subscribe_report_result = mss_request.run_main(method=api_date['method'], url=api_date['url'], json=date, headers=api_date['headers'])
    log.info("新增订阅返回结果：{}".format(add_subscribe_report_result.json()))

    yield add_subscribe_report_result.json()['data'][0]

    # 删除订阅报告
    # api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_subscribe_delete', api='api', token=login_mss)
    # report_delete_result = mss_request.run_main(method=api_date['method'], url=api_date['url'], json={'ids': [add_subscribe_report_result.json()['data'][0], ]}, headers=api_date['headers'])
    # log.info("删除报告结果：{}".format(report_delete_result.json()))


@pytest.fixture(scope="function")
def add_and_delete_asset_center(login_mss):
    """
    新增并删除订阅报告
    :param login_mss: token值
    :return: 新增资产的id值
    """
    add_asset_data = json_read('/data/mss_data/mss_operating_center_data/mss_asset_center_add.json')

    # 获取接口请求数据
    api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_center_add', api='api', token=login_mss)

    # 获取新增资产结果
    add_asset_result = mss_request.run_main(method=api_date['method'], url=api_date['url'], json=add_asset_data, headers=api_date['headers'])
    log.info("新增资产返回结果：{}".format(add_asset_result.json()))

    yield add_asset_result.json()['data']

    # 删除资产
    delete_asset_data = json_read('/data/mss_data/mss_operating_center_data/mss_asset_center_delete.json')
    api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_center_delete', api='api', token=login_mss)
    delete_asset_result = mss_request.run_main(method=api_date['method'], url=api_date['url'], json=delete_asset_data, headers=api_date['headers'])
    log.info("删除资产返回结果：{}".format(delete_asset_result.json()))
