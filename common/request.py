#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/12 17:31
# @Author: william.cao
# @File  : request.py

import requests
import urllib3 as urllib3
from comm.log import Log


class RunMethod:
    log = Log()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def __init__(self):
        """session管理器"""
        self.session = requests.session()

    def run_main(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        return self.session.request(method, url, params=params, data=data, json=json, headers=headers, verify=False, **kwargs)

    def close_session(self):
        """关闭session"""
        self.session.close()
