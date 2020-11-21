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
            if table.cell_value(norw, 3) != '否':  # 每行第三列等于否将不读取内容
                value = table.row_values(norw)
                value.pop(3)
                # 配合将每一行转换成元组存储，迎合 pytest的参数化操作，如不需要可以注释掉 value = tuple(value)
                value = tuple(value)
                logger.info(f'{value}')
                data_list.append(value)
        return data_list
