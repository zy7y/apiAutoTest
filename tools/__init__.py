#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: __init__.py.py
@ide: PyCharm
@time: 2020/7/31
"""
from jsonpath import jsonpath
from loguru import logger


def extractor(obj: dict, expr: str = '.') -> object:
    """
    :param obj :json/dict类型数据
    :param expr: 表达式, . 提取字典所有内容， $.case 提取一级字典case， $.case.data 提取case字典下的data
    $.0.1 提取字典中的第一个列表中的第二个的值
    """
    try:
        result = jsonpath(obj, expr)[0]
    except Exception as e:
        logger.error(f'提取不到内容，丢给你一个错误！{e}')
        result = None
    return result

