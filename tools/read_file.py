#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: read_file.py
@ide: PyCharm
@time: 2020/7/31
@desc： 更新时间 2020/11/21 15：34 后续所有关于文件读取的方法全部收纳与此
"""
import yaml
import xlrd
from tools import extractor

from pathlib import Path


class ReadFile:
    config_dict = None
    config_path = f"{str(Path(__file__).parent.parent)}/config/config.yaml"

    @classmethod
    def get_config_dict(cls) -> dict:
        """读取配置文件，并且转换成字典
        return cls.config_dict
        """
        if cls.config_dict is None:
            # 指定编码格式解决，win下跑代码抛出错误
            with open(cls.config_path, "r", encoding="utf-8") as file:
                cls.config_dict = yaml.load(file.read(), Loader=yaml.FullLoader)
        return cls.config_dict

    @classmethod
    def read_config(cls, expr: str = ".") -> dict:
        """默认读取config目录下的config.yaml配置文件，根据传递的expr jsonpath表达式可任意返回任何配置项
        :param expr: 提取表达式, 使用jsonpath语法,默认值提取整个读取的对象
        return 根据表达式返回的值
        """
        return extractor(cls.get_config_dict(), expr)

    @classmethod
    def read_testcase(cls):
        """
        读取excel格式的测试用例,返回一个生成器对象
        :return 生成器
        """
        book = xlrd.open_workbook(cls.read_config("$.file_path.test_case"))
        # 读取第一个sheet页
        table = book.sheet_by_index(0)
        for norw in range(1, table.nrows):
            # 每行第4列 是否运行
            if table.cell_value(norw, 4) != "否":  # 每行第4列等于否将不读取内容
                value = table.row_values(norw)
                value.pop(4)
                yield value
