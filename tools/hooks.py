#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
@project: apiAutoTest
@file: hooks.py
@author: zy7y
@time: 2021/2/27
@site: https://cnblogs.com/zy7y
@github: https://github.com/zy7y
@gitee: https://gitee.com/zy7y
@desc: 扩展方法, 2021/02/27
关于exec执行python代码可查阅资料：https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p23_executing_code_with_local_side_effects.html

"""
import json
import time


def get_current_highest():
    """获取当前时间戳"""
    return int(time.time())


def sum_data(a, b):
    """计算函数"""
    return a + b


def set_token(token: str):
    """设置token，直接返回字典"""
    return {"Authorization": token}

