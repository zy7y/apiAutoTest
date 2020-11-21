#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest的副本
@author: zy7y
@file: save_response.py
@ide: PyCharm
@time: 2020/8/8
"""
import json

import jsonpath
from loguru import logger


class SaveResponse(object):
    def __init__(self):
        self.actual_response = {}

    # 保存实际响应
    def save_actual_response(self, case_key, case_response):
        """

        :param case_key:用例编号
        :param case_response:对应用例编号的实际响应
        :return:
        """
        self.actual_response[case_key] = case_response
        logger.info(f'当前字典数据{self.actual_response}')

    # 读取依赖数据
    def read_depend_data(self, depend):
        """

        :param depend: 需要依赖数据字典{"case_001":"['jsonpaht表达式1', 'jsonpaht表达式2']"}
        :return:
        """
        depend_dict = {}
        depend = json.loads(depend)
        for k, v in depend.items():
            # 取得依赖中对应case编号的值提取表达式
            try:
                for value in v:
                    # value : '$.data.id'
                    # 取得对应用例编号的实际响应结果
                    actual = self.actual_response[k]
                    # 返回依赖数据的key
                    d_k = value.split('.')[-1]
                    # 添加到依赖数据字典并返回
                    depend_dict[d_k] = jsonpath.jsonpath(actual, value)[0]
            except TypeError as e:
                logger.error(f'实际响应结果中无法正常使用该表达式提取到任何内容，发现异常{e}')

        return depend_dict

# 调试代码
# if __name__ == '__main__':
#     sr = SaveResponse()
#     sr.save_actual_response("case_001", {'data': None, 'meta': {'msg': '参数错误', 'status': 400}})
#     sr.save_actual_response("case_002", {'data': {'id': 500, 'rid': 0, 'username': 'admin', 'mobile': '13718940015', 'email': '1172366686@qq.com', 'token': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjUwMCwicmlkIjowLCJpYXQiOjE1OTY4NTYwNTQsImV4cCI6MTU5Njk0MjQ1NH0.6D9u4x8M4yVWAsK-zJPCw2e7sddClFV-JvntuQyZ8JA'}, 'meta': {'msg': '登录成功', 'status': 200}})
#
#     print(sr.actual_response, type(sr.actual_response))
#     depned_str = """{"case_002": ["$.data.id"],
# "case_001":["$.meta.msg","$.meta.status"]}"""
#
#     result = sr.read_depend_data(depned_str)
#     print(result)