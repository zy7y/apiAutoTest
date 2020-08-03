#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: base_requests.py
@ide: PyCharm
@time: 2020/7/31
"""
from loguru import logger
import requests


class BaseRequest(object):
    def __init__(self):
        pass

    # 请求
    def base_requests(self, method, url, data=None, file_var=None, file_path=None, header=None):
        """

        :param method: 请求方法
        :param url: 接口path
        :param data: 数据,请传入dict样式的字符串
        :param file_path: 上传的文件路径
        :param file_var: 接口中接收文件对象的参数名
        :param header: 请求头
        :return: 完整的响应对象
        """
        session = requests.Session()
        if (file_var in [None, '']) and (file_path in [None, '']):
            files = None
        else:
            # 文件不为空的操作
            files = {file_var: open(file_path, 'rb')}
        # get 请求参数传递形式 params
        if method == 'get':
            res = session.request(method=method, url=url, params=data, headers=header)
        else:
            res = session.request(method=method, url=url, data=data, files=files, headers=header)
        logger.info(f'请求方法:{method}，请求路径:{url}, 请求参数:{data}, 请求文件:{files}, 请求头:{header})')
        return res.json()

