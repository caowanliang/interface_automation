#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/30 13:48
# @Author: william.cao
# @File  : test_organization_and_people_management.py

import allure
import pytest

from common.comm import to_obtain_url_param_method, random_phone
from common.log import Log
from common.request import RunMethod


@pytest.mark.usefixtures("login_mss_platform")
class TestMssAssetManagement(object):
    log = Log()

    @allure.feature('系统功能')
    def setup_class(self):
        """
        数据初始化
        :return:
        """
        self.mss_request = RunMethod()

    def teardown_class(self):
        """
        数据清理
        :return:
        """
        pass

    @allure.story('系统管理-新增单位')
    def test_mss_system_create_unit(self, login_mss_platform):
        """
        系统管理-新增单位
        :param :
        :return:
        """
        date = {
            "city": "杭州市",
            "district": "",
            "name": "西湖区",
            "orgAttribute": "",
            "orgEncipher": "",
            "pid": 1,
            "province": "浙江省",
            "sorder": "002"
        }
        # 获取接口请求数据
        web_list_date = to_obtain_url_param_method(saas_type='mss', api_name='system_add_unit', api='api', token=login_mss_platform)
        try:
            create_unit_result = self.mss_request.run_main(method=web_list_date['method'], url=web_list_date['url'], json=date, headers=web_list_date['headers'])
            self.log.info("新增单位结果：{}".format(create_unit_result.json()))
            assert create_unit_result.status_code == 200
        except Exception as e:
            self.log.error("用例运行报错：{}".format(e))

    @allure.story('系统管理-新增用户')
    def test_mss_system_create_user(self, login_mss_platform):
        """
        系统管理-新增用户
        :param :
        :return:
        """
        date = {
            "confirmPassword": "Xj123456!@#",
            "email": "",
            "expireTime": '',
            "jobLevel": 1,
            "loginName": "dw",
            "orgIds": [1],
            "password": "Xj123456!@#",
            "phone": random_phone(),
            "roleIds": [1, 2, 3],
            "userName": ""
        }
        # 获取接口请求数据
        web_list_date = to_obtain_url_param_method(saas_type='mss', api_name='system_create_user', api='api', token=login_mss_platform)
        try:
            create_user_result = self.mss_request.run_main(method=web_list_date['method'], url=web_list_date['url'], json=date, headers=web_list_date['headers'])
            self.log.info("新增用户结果：{}".format(create_user_result.json()))
            assert create_user_result.status_code == 200
        except Exception as e:
            self.log.error("用例运行报错：{}".format(e))


if __name__ == "__main__":
    pytest.main(['-s', 'test_assets_list.py'])
    # pytest /Users/caowanliang/cloud_line/testcase/test_mss/test_asset_management/test_assets_list.py --alluredir=./report/result
    # allure serve ./report/result
