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

from tools.db import DB
from tools.read_file import ReadFile


@pytest.fixture(scope="session")
def get_db():
    """关于其作用域请移步查看官方文档"""
    try:
        db = DB()
        yield db
    finally:
        db.close()


@pytest.fixture(params=ReadFile.read_testcase())
def cases(request):
    """用例数据，测试方法参数入参该方法名 cases即可，实现同样的参数化
    目前来看相较于@pytest.mark.parametrize 更简洁。
    """
    return request.param
