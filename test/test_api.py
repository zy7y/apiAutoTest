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
from .conftest import pytest

from api import BaseRequest
from tools.data_process import DataProcess


# https://www.cnblogs.com/shouhu/p/12392917.html
# reruns 重试次数 reruns_delay 次数之间的延时设置（单位：秒）
# 失败重跑，会影响总测试时长，如不需要 将 @pytest.mark.flaky(reruns=3, reruns_delay=5) 注释即可
# @pytest.mark.flaky(reruns=2, reruns_delay=1)
# def test_main(cases, get_db):     # 使用数据库功能(包含sql查询，数据备份，数据恢复)
#     # 此处的cases入参来自与 conftest.py  文件中 cases函数，与直接使用 @pytest.mark.parametrize
#     # 有着差不多的效果
#     # 发送请求
#     response, expect, sql = BaseRequest.send_request(cases)
#     # 执行sql
#     DataProcess.handle_sql(sql, get_db)
#     # 断言操作
#     DataProcess.assert_result(response, expect)

def test_main(cases):   # 不使用数据库功能
    # 发送请求
    response, expect, sql = BaseRequest.send_request(cases)
    # 断言操作
    DataProcess.assert_result(response, expect)
