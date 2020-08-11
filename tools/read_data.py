#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: read_data.py
@ide: PyCharm
@time: 2020/7/31
"""
import xlrd
from test import logger


class ReadData(object):
    def __init__(self, excel_path):
        self.excel_file = excel_path
        self.book = xlrd.open_workbook(self.excel_file)

    def get_data(self):
        """

        :return: data_list - pytest参数化可用的数据
        """
        data_list = []

        table = self.book.sheet_by_index(0)
        for norw in range(1, table.nrows):
            # 每行第4列 是否运行
            if table.cell_value(norw, 3) == '否':
                continue
            # 返回该行的所有单元格组成的数据 table.row_values(0) 0代表第1列
            case_number = table.cell_value(norw, 0)
            case_title = table.cell_value(norw, 1)
            path = table.cell_value(norw, 2)
            is_token = table.cell_value(norw, 4)
            method = table.cell_value(norw, 5)
            # 入参关键字
            parametric_key = table.cell_value(norw, 6)
            file_var = table.cell_value(norw, 7)
            file_path = table.cell_value(norw, 8)
            # 路径参数
            parameters = table.cell_value(norw, 9)
            dependent = table.cell_value(norw, 10)
            data = table.cell_value(norw, 11)
            expect = table.cell_value(norw, 12)
            value = [case_number, case_title, path, is_token, method, parametric_key, file_var, file_path, parameters, dependent, data, expect]
            # 配合将每一行转换成元组存储，迎合 pytest的参数化操作，如不需要可以注释掉 value = tuple(value)
            value = tuple(value)
            logger.info(f'{value}')
            data_list.append(value)
        return data_list
