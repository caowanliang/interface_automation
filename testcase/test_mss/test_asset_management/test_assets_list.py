#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/13 14:50
# @Author: william.cao
# @File  : test_assets_list.py
import os

import allure
import pytest

from common.comm import to_obtain_url_param_method
from common.log import Log
from common.request import RunMethod


@pytest.mark.usefixtures("login_mss_platform")
class TestMssAssetManagement(object):
    log = Log()

    @allure.feature('登录功能')
    @allure.story('登录成功')
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

    api_list = ['web_api', 'ip_api', 'domain_api', 'port_api']

    @allure.story('资产列表-资产列表查询')
    @pytest.mark.parametrize("api", api_list)
    def test_mss_search_web_list(self, login_mss_platform, api):
        """
        资产列表-web资产列表查询
        :param :
        :return:
        """
        date = {
            "pageNumber": 0,
            "pageSize": 10,
            "riskLevel": '',
            "orderKey": "",
            "order": "",
            "orgCodes": [],
            "userCodes": [],
            "groupCodes": [],
            "incloudSub": True,
            "term": '',
            "searchParam": [{
                "name": "orgCodes",
                "searchCriteria": "=",
                "searchRelation": "and",
                "incloudSub": True,
                "value": "root_org",
                "selectData": []
            }]
        }
        # 获取接口请求数据
        web_list_date = to_obtain_url_param_method(saas_type='mss', api_name='asset_list_query', api=api, token=login_mss_platform)
        try:
            web_list_result = self.mss_request.run_main(method=web_list_date['method'], url=web_list_date['url'], json=date, headers=web_list_date['headers'])
            self.log.info("列表返回结果：{}".format(web_list_result.json()))
            assert web_list_result.json()['code'] == 200
        except Exception as e:
            self.log.error("用例运行报错：{}".format(e))


if __name__ == "__main__":
    pytest.main(['-s', 'test_assets_list.py'])
    # pytest /Users/caowanliang/cloud_line/testcase/test_mss/test_asset_management/test_assets_list.py --alluredir=./report/result
    # allure serve ./report/result

