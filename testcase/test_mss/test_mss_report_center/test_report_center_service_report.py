#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/13 14:50
# @Author: william.cao
# @File  : test_assets_list.py

import allure
import pytest

from common.comm import to_obtain_url_param_method, get_time_stamp
from common.log import Log
from common.request import RunMethod
from data.mss_data.mss_report_center_data import MssReportCenterData


@pytest.mark.usefixtures("login_mss")
class TestReportCenterServiceReport(object):
    log = Log()
    mss_report_center_data = MssReportCenterData()

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

    data_list = [mss_report_center_data.creat_week_report_date, mss_report_center_data.creat_mouth_report_date, mss_report_center_data.creat_vulnerability_management_report_date]

    @allure.story('报告中心-服务报告-生成报告')
    @pytest.mark.parametrize("date", data_list)
    def test_mss_service_report_creat_report(self, login_mss, date):
        """
        服务报告-生成报告
        :param login_mss: token值
        :return:
        """
        # 获取接口请求数据
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='create_report', api='api', token=login_mss)

        # 生成报告
        creat_report_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=date, headers=api_date['headers'])
        self.log.info("列表返回结果：{}".format(creat_report_result.json()))
        assert creat_report_result.json()['message'] == 'RESPONSE_OK'

        # 生成报告查询
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='history_report_list', api='api', token=login_mss)
        report_list_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=self.mss_report_center_data.history_report_list, headers=api_date['headers'])
        self.log.info("列表返回结果：{}".format(report_list_result.json()))


if __name__ == "__main__":
    pytest.main(['-s', 'test_assets_list.py'])
    # pytest /Users/caowanliang/cloud_line/testcase/test_mss/test_asset_management/test_assets_list.py --alluredir=./report/result
    # allure serve ./report/result

