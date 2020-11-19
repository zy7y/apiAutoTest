#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: data_process.py
@ide: PyCharm
@time: 2020/11/18
"""
import json
import re
from tools import *
from tools.read_config import ReadConfig


class DataProcess:
    response_dict = {}
    header = {}
    null_header = {}

    @classmethod
    def save_response(cls, key: str, value: object) -> None:
        """
        保存实际响应
        :param key: 保存字典中的key，一般使用用例编号
        :param value: 保存字典中的value，使用json响应
        """
        cls.response_dict[key] = value
        logger.info(f'添加key: {key}, 对应value: {value}')

    @classmethod
    def handle_path(cls, path_str: str = '') -> str:
        """路径参数处理
        :param path_str: 带提取表达式的字符串 /&$.case_005.data.id&/state/&$.case_005.data.create_time&
        上述内容表示，从响应字典中提取到case_005字典里data字典里id的值，假设是500，后面&$.case_005.data.create_time& 类似，最终提取结果
        return  /511/state/1605711095
        """
        # /&$.case.data.id&/state/&$.case_005.data.create_time&
        for i in re.findall('&(.*?)&', path_str):
            path_str = path_str.replace(f'&{i}&', str(extractor(cls.response_dict, i)))
        logger.info(f'提取出的路径地址: {path_str}')
        return path_str

    @classmethod
    def handle_header(cls, is_token: str, response: dict, reg) -> dict:
        """处理header"""
        if is_token == '写':
            cls.header['Authorization'] = extractor(response, reg)
            return cls.header
        elif is_token == '':
            return cls.null_header
        else:
            return cls.header

    @classmethod
    def handle_data(cls, variable: str) -> dict:
        """请求数据处理
        :param variable: 请求数据，传入的是可转换字典/json的字符串,其中可以包含变量表达式
        return 处理之后的json/dict类型的字典数据
        """
        if variable == '':
            return
        for i in re.findall('&(.*?)&', variable):
            variable = variable.replace(f'&{i}&', str(extractor(cls.response_dict, i)))
        if 'None' in variable:
            variable = variable.replace('None', 'null')
        if 'True' in variable:
            variable = variable.replace('True', 'true')
        if 'False' in variable:
            variable = variable.replace('False', 'false')
        logger.info(f'最终的请求数据如下: {variable}')
        return json.loads(variable)
