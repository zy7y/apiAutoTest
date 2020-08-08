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
    def base_requests(self, method, url, parametric_key, data=None, file_var=None, file_path=None, header=None):
        """

        :param method: 请求方法
        :param url: 请求url
        :param parametric_key: 入参关键字， get/delete/head/options/请求使用params,
         post/put/patch请求可使用json（application/json）/data

        :param data: 参数数据，默认等于None
        :param file_var: 接口中接受文件的参数关键字
        :param file_path: 文件对象的地址
        :param header: 请求头
        :return: 返回json格式的响应
        """
        session = requests.Session()
        if (file_var in [None, '']) and (file_path in [None, '']):
            files = None
        else:
            # 文件不为空的操作
            files = {file_var: open(file_path, 'rb')}
        # # get 请求参数传递形式 params
        # if method == 'get':
        #     res = session.request(method=method, url=url, params=data, headers=header)
        # else:
        #     res = session.request(method=method, url=url, data=data, files=files, headers=header)
        # logger.info(f'请求方法:{method}，请求路径:{url}, 请求参数:{data}, 请求文件:{files}, 请求头:{header})')
        # return res.json()

        if parametric_key == 'params':
            res = session.request(method=method, url=url, params=data, headers=header)
        elif parametric_key == 'data':
            res = session.request(method=method, url=url, data=data, files=files, headers=header)
        elif parametric_key == 'json':
            res = session.request(method=method, url=url, json=data, files=files, headers=header)
        else:
            raise ValueError('可选关键字为：get/delete/head/options/请求使用params, post/put/patch请求可使用json（application/json）/data')
        logger.info(f'请求方法:{method}，请求路径:{url}, 请求参数:{data}, 请求文件:{files}, 请求头:{header})')
        return res.json()


