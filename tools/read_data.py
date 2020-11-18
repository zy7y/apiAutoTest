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
from tools import *


class ReadData(object):
    excel_path = '../data/case_data.xlsx'

    @classmethod
    def get_data(cls):
        """

        :return: data_list - pytest参数化可用的数据
        """
        data_list = []
        book = xlrd.open_workbook(cls.excel_path)
        table = book.sheet_by_index(0)
        for norw in range(1, table.nrows):
            # 每行第4列 是否运行
            if table.cell_value(norw, 3) != '否':  # 每行第三列等于否将不读取内容
                value = table.row_values(norw)
                value.pop(3)
                logger.info(f'{value}')
                data_list.append(list(value))
        return data_list


if __name__ == '__main__':
    ReadData.get_data()