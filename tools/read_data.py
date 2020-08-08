#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: read_data.py
@ide: PyCharm
@time: 2020/7/31
"""
import json

import jsonpath
import xlrd
from xlutils.copy import copy
from loguru import logger


class ReadData(object):
    def __init__(self, excel_path):
        self.excel_file = excel_path
        self.book = xlrd.open_workbook(self.excel_file)

    def get_data(self):
        """

        :return: data_list - pytest参数化可用的数据， title_list pytest参数化 ids关键字用到的标题数据
        """
        data_list = []
        title_list = []

        table = self.book.sheet_by_index(0)
        for norw in range(1, table.nrows):
            # 每行第4列 是否运行
            if table.cell_value(norw, 3) == '否':
                continue
            # 每行第3列， 标题单独拿出来
            title_list.append(table.cell_value(norw, 1))

            # 返回该行的所有单元格组成的数据 table.row_values(0) 0代表第1列
            case_number = table.cell_value(norw, 0)
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
            actual = table.cell_value(norw, 13)
            value = [case_number, path, is_token, method, parametric_key, file_var, file_path, parameters, dependent, data, expect, actual]
            logger.info(value)
            # 配合将每一行转换成元组存储，迎合 pytest的参数化操作，如不需要可以注释掉 value = tuple(value)
            value = tuple(value)
            data_list.append(value)
        return data_list, title_list

    def write_result(self, case_number, result):
        """

        :param case_number: 用例编号：case_001
        :param result: 需要写入的响应值
        :return:
        """
        row = int(case_number.split('_')[1])
        logger.info('开始回写实际响应结果到用例数据中.')
        result = json.dumps(result, ensure_ascii=False)
        new_excel = copy(self.book)
        ws = new_excel.get_sheet(0)
        # 11 是 实际响应结果栏在excel中的列数-1
        ws.write(row, 11, result)
        new_excel.save(self.excel_file)
        logger.info(f'写入完毕:-写入文件: {self.excel_file}, 行号: {row + 1}, 列号: 11, 写入值: {result}')

    # 读实际的响应
    def read_actual(self, depend):
        """

        :param nrow: 列号
        :param depend: 依赖数据字典格式,前面用例编号，后面需要提取对应字段的jsonpath表达式
        {"case_001":["$.data.id",],}
        :return:
        """
        depend = json.loads(depend)
        # 用来存依赖数据的字典
        depend_dict = {}
        for k, v in depend.items():
            # 得到行号
            norw = int(k.split('_')[1])
            table = self.book.sheet_by_index(0)
            # 得到对应行的响应,        # 11 是 实际响应结果栏在excel中的列数-1
            actual = json.loads(table.cell_value(norw, 11))
            try:
                for i in v:
                    logger.info(f'i {i}, v {v}, actual {actual} \n {type(actual)}')
                    depend_dict[i.split('.')[-1]] = jsonpath.jsonpath(actual, i)[0]
            except TypeError as e:
                logger.error(f'实际响应结果中无法正常使用该表达式提取到任何内容，发现异常{e}')
        return depend_dict









if __name__ == '__main__':
    rd = ReadData('../data/case_data.xlsx')
    data, title = rd.get_data()


    # value = "{'data': {'id': 500, 'rid': 0, 'username': 'admin', 'mobile': '18822222223', 'email': '12344@qq.com', 'token': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjUwMCwicmlkIjowLCJpYXQiOjE1OTYzNTgxODUsImV4cCI6MTU5NjQ0NDU4NX0.utWSoAxiWCbf9W1xCkGo2669g9VR5zGMgcsbgblShrs'}, 'meta': {'msg': '登录成功', 'status': 200}}"
    # rd.write_result(2,11,value)

#     ddt = """{
# "case_002":["$.data.id","$.data.username"]
# }"""
#
#     d1 = rd.read_actual(ddt, 11)
#     d2 = ''
#     print(d1.update(json.loads(ddt)))
#     print(d1)
