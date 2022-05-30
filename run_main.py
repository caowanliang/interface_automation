#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2022/5/30 19:10
# @Author: william.cao
# @File  : run_main.py

import sys
import subprocess

WIN = sys.platform.startswith('win')


def main():
    """
    主函数
    """
    steps = [
        "venv\\Script\\activate" if WIN else "source venv/bin/activate",
        "pytest --alluredir allure-results --clean-alluredir",
        "allure generate allure-results -c -o allure-report",
        "allure open allure-report"
    ]
    for step in steps:
        subprocess.run("call " + step if WIN else step, shell=True)


if __name__ == "__main__":
    main()