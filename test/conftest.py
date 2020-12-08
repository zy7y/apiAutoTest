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


@pytest.fixture(scope="session")
def get_db():
    """关于其作用域请移步查看官方文档"""
    db = DB()
    yield db
    db.close()
