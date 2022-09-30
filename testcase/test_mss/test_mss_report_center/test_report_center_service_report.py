#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/13 14:50
# @Author: william.cao
# @File  : test_assets_list.py
import json
import os
import time
from datetime import datetime, timedelta

import allure
import pytest

from common.log import Log
from common.mysql_con import MySQLConnection
from common.public_methods import json_read, to_obtain_url_param_method, retry, json_edit
from common.request import RunMethod

@allure.feature("报告中心")
@pytest.mark.usefixtures("login_mss")
class TestReportCenterServiceReport(object):
    addr = '/data/mss_data/mss_report_center_data/'
    def setup_class(self):
        """
        数据初始化
        :return:
        """
        self.mss_request = RunMethod()
        self.log = Log()
        self.addr = '/data/mss_data/mss_report_center_data/'

    data_list = [json_read(addr + 'create_week_report_date.json'), json_read(addr + 'create_mouth_report_date.json'), json_read(addr + 'create_vulnerability_management_report_date.json'), json_read(addr + 'create_exposed_surface_report_date.json')]

    @allure.story("服务报告-生成周报、月报、漏洞管理、暴露面检测报告并删除")
    @allure.severity("blocker")
    @allure.testcase("测试用例的禅道链接地址_例子")
    @pytest.mark.parametrize("date", data_list)
    def test_mss_service_report_creat_and_delete_report(self, login_mss, date):
        """
        1.生成周报、月报、漏洞管理、暴露面检测报告
        2.查询生成报告成功
        3.删除报告
        4.校验报告删除成功
        :param login_mss: token值
        :return:
        """
        # 获取接口请求数据
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_record_create', api='api', token=login_mss)

        # 生成周报、月报、漏洞管理、暴露面检测报告
        creat_report_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=date, headers=api_date['headers'])
        self.log.info("生成报告返回结果：{}".format(creat_report_result.json()))
        assert creat_report_result.json()['message'] == 'RESPONSE_OK'

        # 生成报告查询
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_record_list', api='api', token=login_mss)
        report_list_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=json_read(self.addr + 'report_record_list.json'), headers=api_date['headers'])
        self.log.info("报告查询返回结果：{}".format(report_list_result.json()))
        assert str(creat_report_result.json()['data'][0]) in str(report_list_result.json()['data'])

        # 删除报告
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_record_remove_by_ids', api='api', token=login_mss)
        report_delete_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'] + creat_report_result.json()['data'][0], json={}, headers=api_date['headers'])
        assert report_delete_result.json()['message'] == 'RESPONSE_OK'

        # 删除报告查询
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_record_list', api='api', token=login_mss)
        report_list_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=json_read(self.addr + 'report_record_list.json'), headers=api_date['headers'])
        self.log.info("报告查询返回结果：{}".format(report_list_result.json()))
        assert str(creat_report_result.json()['data'][0]) not in str(report_list_result.json()['data'])


    @allure.story("服务报告-推送报告")
    @allure.severity("blocker")
    @allure.testcase("测试用例的禅道链接地址_例子")
    @pytest.mark.usefixtures('create_and_delete_report')
    @retry(delays=(1, 2, 1))
    def test_mss_service_report_send_mouth_report(self, create_and_delete_report, login_mss):
        """
        1.生成月报
        2.发送月报
        3.发送状态校验
        4.删除报告
        :param create_and_delete_report: 生成报告的id值
        :param login_mss: token值
        :return:
        """
        # 发送报告
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_record_send_report', api='api',token=login_mss)
        send_report_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'] + create_and_delete_report, json={}, headers=api_date['headers'])
        self.log.info("发送报告返回结果：{}".format(send_report_result.json()))
        assert send_report_result.json()['message'] == 'RESPONSE_OK'

        # 发送状态校验
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_record_list', api='api', token=login_mss)
        report_list_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=json_read(self.addr + 'report_record_list.json'), headers=api_date['headers'])
        for i in range(len(report_list_result.json()['data'])):
            if create_and_delete_report == report_list_result.json()['data']['id']:
                assert report_list_result.json()['data']['sendStatus'] != 0
                self.log.info("当前报告状态返回结果：{}".format(report_list_result.json()['data']['sendStatus']))


    @allure.story("服务报告-新增订阅报告")
    @allure.severity("blocker")
    @allure.testcase("测试用例的禅道链接地址_例子")
    @pytest.mark.usefixtures('add_and_delete_subscribe_report')
    def test_mss_service_report_add_and_delete_subscribe_report(self, add_and_delete_subscribe_report, login_mss):
        """
        1.生成订阅报告
        2.列表校验报告新增成功
        3.删除报告
        :param add_and_delete_subscribe_report: 新增订阅报告的id值
        :param login_mss: token值
        :return:
        """
        # 新增订阅报告查询
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_subscribe_page', api='api', token=login_mss)
        select_subscribe_report_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=json_read(self.addr + 'report_subscribe_page_date.json'), headers=api_date['headers'])
        self.log.info("订阅报告查询返回结果：{}".format(select_subscribe_report_result.json()))
        assert str(add_and_delete_subscribe_report) in str(select_subscribe_report_result.json()['data'])
        assert select_subscribe_report_result.json()['data'][0]['enable'] == 1
        assert select_subscribe_report_result.json()['data'][0]['enableCheck'] == 1
        assert select_subscribe_report_result.json()['data'][0]['fileType'] == 'word'


    @allure.story("服务报告-编辑订阅报告")
    @allure.severity("blocker")
    @allure.testcase("测试用例的禅道链接地址_例子")
    @pytest.mark.usefixtures('add_and_delete_subscribe_report')
    def test_mss_service_report_edit_subscribe_report(self, add_and_delete_subscribe_report, login_mss):
        """
        1.生成订阅报告(启用=打开，审核=打开)
        2.编辑订阅报告（启用=关闭，审核=关闭）
        3.校验编辑成功
        4.删除报告
        :param add_and_delete_subscribe_report: 新增订阅报告的id值
        :param login_mss: token值
        :return:
        """
        # 修改json文件中的id参数
        edit_data = json_read(self.addr + 'edit_subscribe_report_date.json')
        edit_data["id"] = add_and_delete_subscribe_report
        json_edit(edit_data, self.addr + 'edit_subscribe_report_date.json')

        # 修改订阅报告
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_subscribe_edit', api='api', token=login_mss)
        select_subscribe_report_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=json_read(self.addr+'edit_subscribe_report_date.json'), headers=api_date['headers'])
        self.log.info("订阅报告编辑返回结果：{}".format(select_subscribe_report_result.json()))

        # 校验编辑后的订阅报告
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_subscribe_page', api='api', token=login_mss)
        select_subscribe_report_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=json_read(self.addr + 'report_subscribe_page_date.json'), headers=api_date['headers'])
        self.log.info("订阅报告查询返回结果：{}".format(select_subscribe_report_result.json()))
        assert str(add_and_delete_subscribe_report) in str(select_subscribe_report_result.json()['data'])
        assert select_subscribe_report_result.json()['data'][0]['enable'] == 0
        assert select_subscribe_report_result.json()['data'][0]['enableCheck'] == 0
        assert select_subscribe_report_result.json()['data'][0]['fileType'] == 'pdf'


    @allure.story("服务报告-订阅报告启用状态编辑")
    @allure.severity("blocker")
    @allure.testcase("测试用例的禅道链接地址_例子")
    @pytest.mark.usefixtures('add_and_delete_subscribe_report')
    def test_mss_service_report_enable_subscribe_report(self, add_and_delete_subscribe_report, login_mss):
        """
        1.生成订阅报告（启用状态为打开）
        2.编辑启用状态为：关闭
        3.校验编辑关闭成功
        4.删除报告
        :param add_and_delete_subscribe_report: 新增订阅报告的id值
        :param login_mss: token值
        :return:
        """
        # 关闭启用状态
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_subscribe_enable', api='api', token=login_mss)
        enable_subscribe_report_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json={"enable":0,"ids":[add_and_delete_subscribe_report]}, headers=api_date['headers'])
        self.log.info("订阅报告打开启用状态返回结果：{}".format(enable_subscribe_report_result.json()))
        assert enable_subscribe_report_result.json()['message'] == 'RESPONSE_OK'

        # 校验关闭成功
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_subscribe_page', api='api', token=login_mss)
        select_subscribe_report_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=json_read(self.addr + 'report_subscribe_page_date.json'), headers=api_date['headers'])
        self.log.info("订阅报告查询返回结果：{}".format(select_subscribe_report_result.json()))
        assert select_subscribe_report_result.json()['data'][0]['enable'] == 0


    @allure.story("服务报告-订阅报告生成后审核发送")
    @allure.severity("blocker")
    @allure.testcase("测试用例的禅道链接地址_例子")
    @pytest.mark.usefixtures('add_and_delete_subscribe_report')
    def test_mss_service_report_audit_subscribe_report(self, add_and_delete_subscribe_report, login_mss):
        """
        1.生成订阅报告（启用状态为打开）
        2.链接数据库修改发送时间为当天
        3.历史报告列表生成审核数据
        4.登陆运营人员账号通过审核并发送
        5.删除发送的订阅报告
        6.删除订阅
        :param add_and_delete_subscribe_report: 新增订阅报告的id值
        :param login_mss: token值
        :return:
        """
        # 生成下次发送订阅报告时间
        next_send_time = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        # 链接数据库
        mysql_conn = MySQLConnection()
        values = {"time": next_send_time, "id": int(add_and_delete_subscribe_report)}

        # 修改数据库下次发送时间
        update_sql = mysql_conn.execute("UPDATE report_subscribe SET next_send_time=%(time)s WHERE id=%(id)s", param=values)
        time.sleep(1)
        mysql_conn.commit()
        mysql_conn.close()
        print(update_sql)

    def test_delete(self, login_mss):
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='report_record_remove_by_ids', api='api',
                                              token=login_mss)
        report_delete_result = self.mss_request.run_main(method=api_date['method'],
                                                         url=api_date['url'] + '21193',
                                                         json={}, headers=api_date['headers'])
        assert report_delete_result.json()['message'] == 'RESPONSE_OK'

if __name__ == "__main__":
    pass
