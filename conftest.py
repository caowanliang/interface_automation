#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/12 19:42
# @Author: william.cao
# @File  : conftest.py

import pytest

from common.comm import to_obtain_url_param_method
from common.request import RunMethod
from common.log import Log


@pytest.fixture(scope="class")
def login_mss():
    """
    登陆安恒云平台
    :return:
    """
    global id_token
    log = Log()
    # 初始化请求
    mss_request = RunMethod()
    date = {
        "userName": "13052181105",
        "password": "eWYxdHVkeXU6MTY1NTE3MDgzNjAzOQ==",
        "verifyCode": "123"
    }
    # 读取登陆数据
    web_list_date = to_obtain_url_param_method(saas_type='MSS', api_name='mss_login', api='api', token='token')

    try:
        login_result = mss_request.run_main(method=web_list_date['method'], url=web_list_date['url'], json=date, headers=web_list_date['headers'])
        id_token = login_result.json()
        log.info('登陆信息{}'.format(id_token))
    except Exception as e:
        log.error('登录报错{}'.format(e))
    yield id_token['data']['access_token']
