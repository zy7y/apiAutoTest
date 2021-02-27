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
import re

import allure

from jsonpath import jsonpath
from loguru import logger

from tools.hooks import *


def extractor(obj: dict, expr: str = '.') -> object:
    """
    根据表达式提取字典中的value，表达式, . 提取字典所有内容， $.case 提取一级字典case， $.case.data 提取case字典下的data
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


def rep_expr(content: str, data: dict, expr: str = '&(.*?)&') -> str:
    """从请求参数的字符串中，使用正则的方法找出合适的字符串内容并进行替换
    :param content: 原始的字符串内容
    :param data: 在该项目中一般为响应字典，从字典取值出来
    :param expr: 查找用的正则表达式
    return content： 替换表达式后的字符串
    """
    for ctt in re.findall(expr, content):
        content = content.replace(f'&{ctt}&', str(extractor(data, ctt)))
        
    # 增加自定义函数得的调用，函数写在tools/hooks.py中
    for func in re.findall('@(.*?)@', content):
        content = content.replace(f'@{func}@', exec_func(func))

    return content


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
        dict_str = json.loads(dict_str)
    except Exception as e:
        if 'null' in dict_str:
            dict_str = dict_str.replace('null', 'None')
        elif 'true' in dict_str:
            dict_str = dict_str.replace('true', 'True')
        elif 'false' in dict_str:
            dict_str = dict_str.replace('false', 'False')
        dict_str = eval(dict_str)
        logger.error(e)
    return dict_str


def allure_title(title: str) -> None:
    """allure中显示的用例标题"""
    allure.dynamic.title(title)


def allure_step(step: str, var: str) -> None:
    """
    :param step: 步骤及附件名称
    :param var: 附件内容
    """
    with allure.step(step):
        allure.attach(json.dumps(var, ensure_ascii=False, indent=4), step, allure.attachment_type.TEXT)