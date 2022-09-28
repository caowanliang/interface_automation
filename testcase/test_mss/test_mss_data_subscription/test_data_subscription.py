#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/13 14:50
# @Author: william.cao
# @File  : test_assets_list.py
import os

import allure
import pytest

from common.comm import to_obtain_url_param_method, get_time_stamp
from common.log import Log
from common.request import RunMethod


@pytest.mark.usefixtures("login_mss")
class TestDataSubscription(object):
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

    @allure.story('数据订阅-人读报告')
    def test_mss_people_read_the_report(self, login_mss):
        """
        人读报告-应急漏洞报告发送
        :param login_mss: token值
        :return:
        """
        date = {
            "update_time": get_time_stamp(),
            "title": 'Apache CouchDB远程代码执行漏洞风险提示（CVE-2022-24706）',
            "content": '<center>\n<img src=\"https://xasoc-micro.oss-cn-hangzhou.aliyuncs.com/31da455e-25ac-4b96-8d28-0866783b3dc6/640.png\" style=\"width:100%\"/>\n</center>\n\n> #### 漏洞公告\n> \n> 近日，安恒信息CERT监测到Apache官方发布安全公告，披露了Apache CouchDB中的一个远程代码执行漏洞（CVE-2022-24706）。该漏洞允许未经身份验证的攻击者通过访问特定端口，绕过权限验证并获得管理员权限。\n> \n> 参考链接：\n> https://docs.couchdb.org/en/stable/cve/2022-24706.html\n\n# 一 影响范围\n\n**受影响的Apache CouchDB版本:**\nApache CouchDB < 3.2.2\n\n# 二 漏洞描述\n\n**远程代码执行漏洞（CVE-2022-24706）：** 在受影响版本的 Apache CouchDB 中，未授权的远程攻击者可以通过访问特定端口，绕过权限验证并获得管理员权限，从而可能造成服务器被接管。\n\nCouchDB官方建议在所有CouchDB安装前设置防火墙。完整的CouchDB API在注册的端口5984上可用，这是单节点安装需要公开的唯一端口。不将单独的分发端口暴露给外部访问的安装不易受到攻击。\n\n| **细节是否公开** | **POC 状态** | **EXP 状态** | **在野利用** |\n| :----------------: | :------------: | :------------: | :------------: |\n|        否        |    未公开    |    公开    |     未知     |\n\n# 三 缓解措施\n\n**高危：** 目前漏洞细节和利用代码已公开，官方已发布新版本修复了此漏洞，建议受影响用户及时升级更新到Apache CouchDB 3.2.2或更高版本。\n\n下载链接：\n\nhttps://couchdb.apache.org/\n\n相关参考链接：\n\nhttps://lists.apache.org/thread/w24wo0h8nlctfps65txvk0oc5hdcnv00\n\nhttps://www.openwall.com/lists/oss-security/2022/04/26/1\n\nhttps://www.mail-archive.com/announce@apache.org/msg07264.html\n\nhttps://docs.couchdb.org/en/3.2.2/setup/cluster.html\n'
        }
        # 获取接口请求数据
        api_date = to_obtain_url_param_method(saas_type='MSS', api_name='emergency_vulnerability_report', api='api', token=login_mss)
        try:
            send_report_result = self.mss_request.run_main(method=api_date['method'], url=api_date['url'], json=date, headers=api_date['headers'])
            self.log.info("列表返回结果：{}".format(send_report_result.json()))
            assert send_report_result.json()['message'] == 'RESPONSE_OK'
        except Exception as e:
            self.log.error("用例运行报错：{}".format(e))


if __name__ == "__main__":
    pytest.main(['-s', 'test_assets_list.py'])
    # pytest /Users/caowanliang/cloud_line/testcase/test_mss/test_asset_management/test_assets_list.py --alluredir=./report/result
    # allure serve ./report/result

