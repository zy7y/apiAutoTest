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
        path_str.split('/')
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
        if 'null' in variable:
            variable = variable.replace('null', 'None')
        if 'true' in variable:
            variable = variable.replace('true', 'True')
        if 'false' in variable:
            variable = variable.replace('false', 'False')
        logger.info(f'最终的请求数据如下: {variable}')
        print(variable)
        return eval(variable)



if __name__ == '__main__':
    data = """{
    "case_001": {
        "data": null,
        "meta": {
            "msg": "参数错误",
            "status": 400
        }
    },
    "case_002": {
        "data": {
            "id": 500,
            "rid": 0,
            "username": "admin",
            "mobile": "12345678",
            "email": "adsfad@qq.com",
            "token": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjUwMCwicmlkIjowLCJpYXQiOjE2MDU3MTEwOTUsImV4cCI6MTYwNTc5NzQ5NX0.v4YsivyRT9I0kFnIIph7btKdTg7SfeeO6xsbhrGJC5w"
        },
        "meta": {
            "msg": "登录成功",
            "status": 200
        }
    },
    "case_003": {
        "data": {
            "total": 5,
            "pagenum": 1,
            "users": [
                {
                    "id": 500,
                    "role_name": "超级管理员",
                    "username": "admin",
                    "create_time": 1486720211,
                    "mobile": "12345678",
                    "email": "adsfad@qq.com",
                    "mg_state": true
                },
                {
                    "id": 502,
                    "role_name": "测试角色2",
                    "username": "linken",
                    "create_time": 1486720211,
                    "mobile": "1213213123",
                    "email": "asdf@qq.com",
                    "mg_state": false
                },
                {
                    "id": 508,
                    "role_name": "主管",
                    "username": "asdf1",
                    "create_time": 1511853015,
                    "mobile": "123123",
                    "email": "adfsa@qq.com",
                    "mg_state": true
                },
                {
                    "id": 509,
                    "role_name": "test",
                    "username": "asdf123",
                    "create_time": 1511853353,
                    "mobile": "1111",
                    "email": "asdf@qq.com",
                    "mg_state": false
                },
                {
                    "id": 510,
                    "role_name": "超级管理员",
                    "username": "小明111",
                    "create_time": 1605710570,
                    "mobile": "13288888888",
                    "email": "1232@qq.com",
                    "mg_state": false
                }
            ]
        },
        "meta": {
            "msg": "获取管理员列表成功",
            "status": 200
        }
    },
    "case_004": {
        "data": null,
        "meta": {
            "msg": "无效token",
            "status": 400
        }
    },
    "case_005": {
        "data": {
            "id": 511,
            "username": "tester_zy7y1213",
            "role_id": -1,
            "create_time": 1605711095
        },
        "meta": {
            "msg": "创建成功",
            "status": 201
        }
    },
    "case_006": {
        "data": {
            "id": 511,
            "rid": -1,
            "username": "tester_zy7y1213",
            "mobile": null,
            "email": null,
            "mg_state": 0
        },
        "meta": {
            "msg": "设置状态成功",
            "status": 200
        }
    },
    "case_007": {
        "data": {
            "id": 511,
            "rid": -1,
            "username": "tester_zy7y1213",
            "mobile": null,
            "email": null,
            "mg_state": 0
        },
        "meta": {
            "msg": "设置状态成功",
            "status": 200
        }
    },
    "case_008": {
        "data": null,
        "meta": {
            "msg": "删除成功",
            "status": 200
        }
    },
    "case_009": {
        "data": {
            "total": 5,
            "pagenum": 1,
            "users": [
                {
                    "id": 500,
                    "role_name": "超级管理员",
                    "username": "admin",
                    "create_time": 1486720211,
                    "mobile": "12345678",
                    "email": "adsfad@qq.com",
                    "mg_state": true
                },
                {
                    "id": 502,
                    "role_name": "测试角色2",
                    "username": "linken",
                    "create_time": 1486720211,
                    "mobile": "1213213123",
                    "email": "asdf@qq.com",
                    "mg_state": false
                },
                {
                    "id": 508,
                    "role_name": "主管",
                    "username": "asdf1",
                    "create_time": 1511853015,
                    "mobile": "123123",
                    "email": "adfsa@qq.com",
                    "mg_state": true
                },
                {
                    "id": 509,
                    "role_name": "test",
                    "username": "asdf123",
                    "create_time": 1511853353,
                    "mobile": "1111",
                    "email": "asdf@qq.com",
                    "mg_state": false
                },
                {
                    "id": 510,
                    "role_name": "超级管理员",
                    "username": "小明111",
                    "create_time": 1605710570,
                    "mobile": "13288888888",
                    "email": "1232@qq.com",
                    "mg_state": false
                }
            ]
        },
        "meta": {
            "msg": "获取管理员列表成功",
            "status": 200
        }
    }
}"""
    DataProcess.response_dict = json.loads(data)
    print(DataProcess.response_dict, type(DataProcess.response_dict))

    ds = "$.case_001.meta, $.case_001.data, $.case_003.data.users.0.mobile"

    varb = "{'name': 'zy7y', 'meta': &$.case_001.meta&, 'dd': '&$.case_003.data.users.0.mobile&'}"
    print(DataProcess.handle_data(varb, ds), type(DataProcess.handle_data(varb, ds)))
    print(DataProcess.handle_path('/&$.case_005.data.id&/state/&$.case_005.data.create_time&'))
