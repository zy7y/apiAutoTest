#!/usr/bin/env/ python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: test_api.py
@ide: PyCharm
@time: 2020/11/22
@desc: 测试方法
"""
import os
import shutil

import pytest

from tools import logger
from api.base_requests import BaseRequest
from tools.data_process import DataProcess
from tools.read_file import ReadFile

report = ReadFile.read_config('$.file_path.report')
logfile = ReadFile.read_config('$.file_path.log')
# 读取excel数据对象
cases = ReadFile.read_testcase()


class TestApi:

    @classmethod
    def run(cls):
        if os.path.exists('../report'):
            shutil.rmtree(path='../report')
        logger.add(logfile, enqueue=True, encoding='utf-8')
        logger.info('开始测试...')
        pytest.main(args=[f'--alluredir={report}/data'])
        os.system(f'allure generate {report}/data -o {report}/html --clean')
        logger.success('报告已生成')

    @pytest.mark.parametrize('case', cases)
    def test_main(self, case, get_db):
        # 发送请求
        response, expect, sql = BaseRequest.send_request(case)
        # 执行sql
        DataProcess.handle_sql(sql, get_db)
        # 断言操作
        DataProcess.assert_result(response, expect)


if __name__ == '__main__':
    TestApi.run()
