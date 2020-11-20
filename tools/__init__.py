#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: __init__.py.py
@ide: PyCharm
@time: 2020/7/31
"""
import json
import allure

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


def convert_json(dict_str: str) -> dict:
    """
    :param dict_str: 长得像字典的字符串
    return json格式的内容
    """
    try:
        if 'None' in dict_str:
            dict_str = dict_str.replace('None', 'null')
        elif 'True' in dict_str:
            dict_str = dict_str.replace('True', 'true')
        elif 'False' in dict_str:
            dict_str = dict_str.replace('False', 'false')
        return json.loads(dict_str)
    except Exception as e:
        logger.error(f'{e}， json.loads转字典失败')
        return eval(dict_str)


def allure_title(title: str) -> None:
    """allure中显示的用例标题"""
    allure.dynamic.title(title)


def allure_step(step: str, title: object, var: str) -> None:
    """
    :param step: 步骤名称
    :param title: 附件标题
    :param var: 附件内容
    """
    with allure.step(step):
        allure.attach(json.dumps(var, ensure_ascii=False, indent=4), title, allure.attachment_type.TEXT)

if __name__ == '__main__':
    print(convert_json('["1","2"]'))