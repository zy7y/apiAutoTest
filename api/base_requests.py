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

from tools.read_data import ReadData


class BaseRequest(object):
    def __init__(self):
        # 修改时间：2020年9月14日17:09
        # 确保，整个接口测试中，使用同一个requests.Session() 来管理cookie
        self.session = requests.Session()

    # 请求
    def send_requests(self, method, url, parametric_key=None, data=None, file_var=None, file_path=None, header=None):
        """

        :param method: 请求方法
        :param url: 请求url
        :param parametric_key: 入参关键字， get/delete/head/options/请求使用params,
         post/put/patch请求可使用json（application/json）/data

        :param data: 参数数据，默认等于None
        :param file_var: 接口中接受文件的参数关键字
        :param file_path: 文件对象的地址， 单个文件直接放地址：/Users/zy7y/Desktop/vue.js
        多个文件格式：["/Users/zy7y/Desktop/vue.js","/Users/zy7y/Desktop/jenkins.war"]
        :param header: 请求头
        :return: 返回json格式的响应
        """
        # 修改时间：2020年9月14日17:09
        session = self.session

        if (file_var in [None, '']) and (file_path in [None, '']):
            files = None
        else:
            # 文件不为空的操作
            if file_path.startswith('[') and file_path.endswith(']'):
                file_path_list = eval(file_path)
                files = []
                # 多文件上传
                for file_path in file_path_list:
                    files.append((file_var, (open(file_path, 'rb'))))
            else:
                # 单文件上传
                files = {file_var: open(file_path, 'rb')}
        if parametric_key == 'params':
            res = session.request(method=method, url=url, params=data, headers=header)
        elif parametric_key == 'data':
            res = session.request(method=method, url=url, data=data, files=files, headers=header)
        elif parametric_key == 'json':
            res = session.request(method=method, url=url, json=data, files=files, headers=header)
        else:
            raise ValueError(
                '可选关键字为：get/delete/head/options/请求使用params, post/put/patch请求可使用json（application/json）/data')
        logger.info(f'请求方法:{method}，请求路径:{url}, 请求参数:{data}, 请求文件:{files}, 请求头:{header})')
        return res.json()