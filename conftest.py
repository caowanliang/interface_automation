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
def login_mss_platform():
    """
    登陆MSS SaaS平台
    :return:
    """
    log = Log()
    # 初始化请求
    mss_request = RunMethod()
    date = {
        "username": "admin",
        "password": "fac758632483f4f4b089f77455995a68",
        "rememberMe": False,
        "verifyCode": ""
    }
    # 读取登陆数据
    web_list_date = to_obtain_url_param_method(saas_type='mss', api_name='mss_login', api='api', token='token')

    try:
        login_result = mss_request.run_main(method=web_list_date['method'], url=web_list_date['url'], json=date, headers=web_list_date['headers'])
        id_token = login_result.json()
        log.info('登陆信息{}'.format(id_token))
    except Exception as e:
        log.error('登录报错{}'.format(e))
    yield id_token['data']['id_token']

