#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/7/22 16:38
# @Author: william.cao
# @File  : mss_report_center_data.py

class MssReportCenterData(object):

    # 生成周报
    creat_week_report_date = [{
        "reportFileType": "word",
        "reportName": "DAS-MSS-安全托管服务MSS周报",
        "statisticsEndTime": "2022-07-17",
        "statisticsStartTime": "2022-07-11",
        "tenantId": "24091376",
        "tenantName": "测试单位001",
        "typeId": "1",
        "typeName": "安全托管服务MSS周报",
        "userInfoRequestList": [{'userId': "92786503", 'userName': "测试002"}]
    }]

    # 生成月报
    creat_mouth_report_date = [{
        "reportFileType": "word",
        "reportName": "DAS-MSS-安全托管服务MSS月报",
        "statisticsEndTime": "2022-07-17",
        "statisticsStartTime": "2022-07-11",
        "tenantId": "24091376",
        "tenantName": "测试单位001",
        "typeId": "2",
        "typeName": "安全托管服务MSS月报",
        "userInfoRequestList": [{'userId': "92786503", 'userName': "测试002"}]
    }]

    # 生成漏洞管理报告
    creat_vulnerability_management_report_date = [{
        "reportFileType": "pdf",
        "reportName": "DAS-MSS-漏洞管理报告",
        "statisticsEndTime": "2022-07-17",
        "statisticsStartTime": "2022-07-11",
        "tenantId": "24091376",
        "tenantName": "测试单位001",
        "typeId": "3",
        "typeName": "漏洞管理报告",
        "userInfoRequestList": [{'userId': "92786503", 'userName': "测试002"}]
    }]

    # 历史报告查询
    history_report_list = {
        "createUser": "",
        "pageNo": 1,
        "pageSize": 10,
        "sendStatus": "",
        "tenantId": "24091376",
        "typeId": ""
    }