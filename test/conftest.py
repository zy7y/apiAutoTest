#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: conftest.py
@ide: PyCharm
@time: 2020/12/8
@desc:
"""

import pytest

from tools.data_clearing import DataClearing
from tools.db import DB
from tools.read_file import ReadFile


@pytest.fixture(scope="session")
def data_clearing():
    """数据清洗"""
    DataClearing.server_init()
    # 1. 备份数据库
    DataClearing.backup_mysql()
    yield
    # 2. 恢复数据库
    DataClearing.recovery_mysql()
    DataClearing.close_client()


# 若不需要数据清洗功能，请把data_clearing去掉
@pytest.fixture(scope="session")
def get_db(data_clearing):
    """关于其作用域请移步查看官方文档"""
    try:
        db = DB()
        yield db
    finally:
        db.close()

# 不使用数据清洗 请把 下面代码解除注释 上面的get_db函数注释
# @pytest.fixture(scope="session")
# def get_db():
#     """关于其作用域请移步查看官方文档"""
#     try:
#         db = DB()
#         yield db
#     finally:
#         db.close()

@pytest.fixture(params=ReadFile.read_testcase())
def cases(request):
    """用例数据，测试方法参数入参该方法名 cases即可，实现同样的参数化
    目前来看相较于@pytest.mark.parametrize 更简洁。
    """
    return request.param
