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

@allure.feature("资产中心")
@pytest.mark.usefixtures("login_mss")
class TestReportCenterServiceReport(object):
    addr = '/data/mss_data/mss_operating_center_data/'
    def setup_class(self):
        """
        数据初始化
        :return:
        """
        self.mss_request = RunMethod()
        self.log = Log()
        self.addr = '/data/mss_data/mss_operating_center_data/'


    @allure.story("资产中心-资产列表")
    @allure.severity("blocker")
    @allure.testcase("测试用例的禅道链接地址_例子")
    def test_mss_asset_center_asset_page_list(self, login_mss):
        """
        1.查询资产中心的资产列表
        :param login_mss: token值
        :return:
        """
        asset_data = json_read(self.addr + 'mss_asset_center_page_list_data.json')

        # 获取接口请求数据
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_page_list', api='api', token=login_mss)

        # 获取资产列表
        list_asset_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=asset_data, headers=api_date['headers'])
        self.log.info("资产列表返回结果：{}".format(list_asset_result.json()))
        assert list_asset_result.json()['message'] == 'RESPONSE_OK'
        assert len(list_asset_result.json()['data']) >= 0


    @allure.story("资产中心-搜索客户单位")
    @allure.severity("blocker")
    @allure.testcase("测试用例的禅道链接地址_例子")
    def test_mss_asset_center_asset_tenant_asset_count_page_list(self, login_mss):
        """
        1.查询指定客户单位
        :param login_mss: token值
        :return:
        """
        tenant_asset_data = json_read(self.addr + 'mss_asset_center_tenant_asset_count_page_data.json')

        # 获取接口请求数据
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_tenant_asset_count_page_list', api='api', token=login_mss)

        # 获取资产列表
        list_asset_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=tenant_asset_data, headers=api_date['headers'])
        self.log.info("客户单位列表返回结果：{}".format(list_asset_result.json()))
        assert list_asset_result.json()['message'] == 'RESPONSE_OK'
        assert list_asset_result.json()['data'][0]['tenantId'] == '65089721'
        assert list_asset_result.json()['data'][0]['tenantName'] == '测试已开始单位'


    @allure.story("资产中心-新增资产")
    @allure.severity("blocker")
    @allure.testcase("测试用例的禅道链接地址_例子")
    def test_mss_asset_center_asset_add(self, login_mss):
        """
        1.新增资产
        2.查询新增成功
        3.删除资产
        :param login_mss: token值
        :return:
        """
        add_asset_data = json_read(self.addr + 'mss_asset_center_add.json')
        # 获取接口请求数据
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_center_add', api='api', token=login_mss)

        # 新增资产
        add_asset_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=add_asset_data, headers=api_date['headers'])
        self.log.info("新增资产返回结果：{}".format(add_asset_result.json()))
        assert add_asset_result.json()['message'] == 'RESPONSE_OK'

        # 查询新增成功
        search_asset_data = json_read(self.addr + 'mss_asset_center_page_list_data.json')
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_page_list', api='api', token=login_mss)
        list_asset_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=search_asset_data, headers=api_date['headers'])
        self.log.info("新增后资产列表返回结果：{}".format(list_asset_result.json()))
        assert str(add_asset_result.json()['data']) in str(list_asset_result.json()['data'])

        # 删除资产
        delete_asset_data = json_read(self.addr + 'mss_asset_center_delete.json')
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_center_delete', api='api', token=login_mss)
        delete_asset_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=delete_asset_data, headers=api_date['headers'])
        self.log.info("删除资产返回结果：{}".format(list_asset_result.json()))
        assert delete_asset_result.json()['message'] == 'RESPONSE_OK'

        # 查询删除成功
        asset_data = json_read(self.addr + 'mss_asset_center_page_list_data.json')
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_page_list', api='api', token=login_mss)
        list_asset_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=asset_data, headers=api_date['headers'])
        self.log.info("删除后资产列表返回结果：{}".format(list_asset_result.json()))
        assert str(add_asset_result.json()['data']) not in str(list_asset_result.json()['data'])


    @allure.story("资产中心-查看资产详情")
    @allure.severity("blocker")
    @allure.testcase("测试用例的禅道链接地址_例子")
    @pytest.mark.usefixtures('add_and_delete_asset_center')
    def test_mss_asset_get_detail(self, login_mss, add_and_delete_asset_center):
        """
        1.新增资产
        2.查看资产详情
        3.删除资产
        :param login_mss: token值
        :return:
        """
        # 获取接口请求数据
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_center_get_detail', api='api', token=login_mss)

        # 查看资产详情
        asset_get_detail_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'] + str(add_and_delete_asset_center), json={}, headers=api_date['headers'])
        self.log.info("资产详情返回结果：{}".format(asset_get_detail_result.json()))
        assert asset_get_detail_result.json()['message'] == 'RESPONSE_OK'
        assert asset_get_detail_result.json()['data']['asset']['id'] == add_and_delete_asset_center
        assert asset_get_detail_result.json()['data']['asset']['domain'] == '10.50.27.199'

    @allure.story("资产中心-编辑资产")
    @allure.severity("blocker")
    @allure.testcase("测试用例的禅道链接地址_例子")
    @pytest.mark.usefixtures('add_and_delete_asset_center')
    def test_mss_asset_update_one(self, login_mss, add_and_delete_asset_center):
        """
        1.新增资产
        2.编辑资产
        3.查询编辑资产成功
        4.删除资产
        :param login_mss: token值
        :return:
        """
        # 修改json文件中的id参数
        edit_data = json_read(self.addr + 'mss_asset_center_update.json')
        edit_data["id"] = add_and_delete_asset_center
        json_edit(edit_data, self.addr + 'mss_asset_center_update.json')

        # 获取接口请求数据
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_center_update_one', api='api', token=login_mss)

        # 编辑资产信息
        update_asset_data = json_read(self.addr + 'mss_asset_center_update.json')
        asset_update_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=update_asset_data, headers=api_date['headers'])
        self.log.info("编辑资产返回结果：{}".format(asset_update_result.json()))
        assert asset_update_result.json()['message'] == 'RESPONSE_OK'

        # 查询编辑资产成功
        asset_data = json_read(self.addr + 'mss_asset_center_page_list_data.json')
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_page_list', api='api', token=login_mss)
        list_asset_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=asset_data, headers=api_date['headers'])
        self.log.info("编辑后资产列表返回结果：{}".format(list_asset_result.json()))
        for i in range(len(list_asset_result.json()['data'])):
            if list_asset_result.json()['data'][i]['id'] == add_and_delete_asset_center:
                assert list_asset_result.json()['data'][i]['assetName'] == '被修改的名称'
                assert list_asset_result.json()['data'][i]['serverTypes'] == ["THREAT_DETECTION_AND_RESPONSE_SERVICES"]
                assert list_asset_result.json()['data'][i]['level'] == 'normal'
                assert list_asset_result.json()['data'][i]['typeId'] == 100
                break
            else:
                self.log.error("查询资产修改信息返回结果：{}".format(list_asset_result.json()))

    service_scope_list = ['IN_SERVICE', 'OUT_SERVICE']

    @allure.story("资产中心-批量编辑资产范围")
    @allure.severity("blocker")
    @allure.testcase("测试用例的禅道链接地址_例子")
    @pytest.mark.parametrize('service_scope', service_scope_list)
    def test_mss_asset_batch_update_service_scope(self, login_mss, service_scope):
        """
        1.批量编辑资产-批量编辑资产范围（服务内、服务外）
        2.查询批量编辑资产成功
        :param login_mss: token值
        :return:
        """
        ids_list = []
        # 查询资产列表
        search_asset_data = json_read(self.addr + 'mss_asset_center_page_list_data.json')
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_page_list', api='api', token=login_mss)
        list_asset_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=search_asset_data, headers=api_date['headers'])
        for i in range(len(list_asset_result.json()['data'])):
            ids_list.append(list_asset_result.json()['data'][i]['id'])
        self.log.info("修改资产id列表结果：{}".format(ids_list))

        # 获取接口请求数据
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_center_batch_update', api='api', token=login_mss)
        # 批量编辑资产信息
        batch_asset_update_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json={"ids":ids_list,"tenantId":"65089721","serviceRangeType":service_scope}, headers=api_date['headers'])
        self.log.info("批量编辑资产的服务范围返回结果：{}".format(batch_asset_update_result.json()))
        assert batch_asset_update_result.json()['message'] == 'RESPONSE_OK'

        # 查询编辑资产成功
        asset_data = json_read(self.addr + 'mss_asset_center_page_list_data.json')
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_page_list', api='api', token=login_mss)
        list_asset_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=asset_data, headers=api_date['headers'])
        self.log.info("查询编辑后资产列表返回结果：{}".format(list_asset_result.json()))
        for i in range(len(list_asset_result.json()['data'])):
            if service_scope == 'OUT_SERVICE':
                assert list_asset_result.json()['data'][i]['serviceRangeType'] == 'OUT_SERVICE'
            elif service_scope == 'IN_SERVICE':
                assert list_asset_result.json()['data'][i]['serviceRangeType'] == 'IN_SERVICE'

    how_important_list = ['core', 'importance', 'normal']

    @allure.story("资产中心-批量编辑资产重要程度")
    @allure.severity("blocker")
    @allure.testcase("测试用例的禅道链接地址_例子")
    @pytest.mark.parametrize('how_important', how_important_list)
    def test_mss_asset_batch_update_how_important(self, login_mss, how_important):
        """
        1.批量编辑资产-批量编辑资产重要程度(核心、重要、一般)
        2.查询批量编辑资产成功
        :param login_mss: token值
        :return:
        """
        ids_list = []
        # 查询资产列表
        search_asset_data = json_read(self.addr + 'mss_asset_center_page_list_data.json')
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_page_list', api='api', token=login_mss)
        list_asset_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=search_asset_data, headers=api_date['headers'])
        for i in range(len(list_asset_result.json()['data'])):
            ids_list.append(list_asset_result.json()['data'][i]['id'])
        self.log.info("修改资产id列表结果：{}".format(ids_list))

        # 获取接口请求数据
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_center_batch_update', api='api', token=login_mss)
        # 批量编辑资产信息
        batch_asset_update_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json={"ids":ids_list,"tenantId":"65089721","assetLevel":how_important}, headers=api_date['headers'])
        self.log.info("批量编辑资产的重要程度返回结果：{}".format(batch_asset_update_result.json()))
        assert batch_asset_update_result.json()['message'] == 'RESPONSE_OK'

        # 查询编辑资产成功
        asset_data = json_read(self.addr + 'mss_asset_center_page_list_data.json')
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='asset_page_list', api='api', token=login_mss)
        list_asset_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=asset_data, headers=api_date['headers'])
        self.log.info("查询编辑后资产列表返回结果：{}".format(list_asset_result.json()))
        for i in range(len(list_asset_result.json()['data'])):
            if how_important == 'core':
                assert list_asset_result.json()['data'][i]['level'] == 'core'
            elif how_important == 'important':
                assert list_asset_result.json()['data'][i]['level'] == 'important'
            elif how_important == 'normal':
                assert list_asset_result.json()['data'][i]['level'] == 'normal'


if __name__ == "__main__":
    pass
