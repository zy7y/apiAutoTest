#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: data_tearing.py
@ide: PyCharm
@time: 2020/8/10
"""
import json
from json import JSONDecodeError

import jsonpath
from test import logger


class TreatingData(object):
    """
    处理hader/path路径参数/请求data依赖数据代码
    """

    def __init__(self):
        self.no_token_header = {}
        self.token_header = {}

    def treating_data(self, is_token, parameters, dependent, data, save_response_dict):
        # 使用那个header
        if is_token == '':
            header = self.no_token_header
        else:
            header = self.token_header
        logger.info(f'处理依赖前data的数据:{data}')
        # 处理依赖数据data
        if dependent != '':
            if dependent.find('=') != -1:
                dependent_key = dependent.split('=')[0]
                dependent_value = dependent.split('=')[1]
                dependent_data = {dependent_key: save_response_dict.read_depend_data(dependent_value)}
            else:
                dependent_data = save_response_dict.read_depend_data(dependent)
            logger.debug(f'依赖数据解析获得的字典{dependent_data}')
            if data != '':
                data = json.loads(data)
                exists_key = False
                # 处理data与依赖中有相同key的问题, 目前之支持列表，字典,本地 列表形式调试通过，需要在定义时，data中该key定义成列表
                # 实例{"id": [1],"user":{"username":"123"}}
                for k, v in data.items():
                    for dk, dv in dependent_data.items():
                        if k == dk:
                            if isinstance(data[k], list):
                                data[k].append(dv)
                            if isinstance(data[k], dict):
                                data[k].update(dv)
                            exists_key = True
                if exists_key is False:
                    # 合并组成一个新的data
                    dependent_data.update(data)
                    data = dependent_data
                    logger.info(f'data有数据，依赖有数据时 {data}')

            else:
                # 赋值给data
                data = dependent_data
                logger.info(f'data无数据，依赖有数据时 {data}')
        else:
            if data == '':
                data = None
                logger.info(f'data无数据，依赖无数据时 {data}')
            else:
                data = json.loads(data)
                logger.info(f'data有数据，依赖无数据 {data}')

        # 处理路径参数Path的依赖
        # 传进来的参数类似 {"case_002":"$.data.id"}/item/{"case_002":"$.meta.status"}，进行列表拆分
        path_list = parameters.split('/')
        # 获取列表长度迭代
        for i in range(len(path_list)):
            # 按着
            try:
                # 尝试序列化成dict:   json.loads('2') 可以转换成2
                path_dict = json.loads(path_list[i])
            except JSONDecodeError as e:
                # 序列化失败此path_list[i]的值不变化
                logger.error(f'无法转换字典，进入下一个检查，本轮值不发生变化:{path_list[i]},{e}')
                # 跳过进入下次循环
                continue
            else:
                # 解析该字典，获得用例编号，表达式
                logger.info(f'{path_dict}')
                # 处理json.loads('数字')正常序列化导致的AttributeError
                try:
                    for k, v in path_dict.items():
                        try:
                            # 尝试从对应的case实际响应提取某个字段内容
                            path_list[i] = jsonpath.jsonpath(save_response_dict.actual_response[k], v)[0]
                        except TypeError as e:
                            logger.error(f'无法提取，请检查响应字典中是否支持该表达式,{e}')
                except AttributeError as e:
                    logger.error(f'类型错误:{type(path_list[i])}，本此将不转换值 {path_list[i]},{e}')
        # 字典中存在有不是str的元素:使用map 转换成全字符串的列表
        path_list = map(str, path_list)

        # 将字符串列表转换成字符：500/item/200
        parameters_path_url = "/".join(path_list)
        logger.info(f'path路径参数解析依赖后的路径为{parameters_path_url}')
        return data, header, parameters_path_url