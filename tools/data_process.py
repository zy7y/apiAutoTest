#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: data_process.py
@ide: PyCharm
@time: 2020/11/18
"""
from tools import logger, extractor, convert_json, rep_expr, allure_step, allure_step_no
from tools.db import DB
from tools.read_file import ReadFile


class DataProcess:
    # 存放提取参数的池子
    extra_pool = {}
    header = ReadFile.read_config('$.request_headers')

    @classmethod
    def handle_path(cls, path_str: str, env: str) -> str:
        """路径参数处理
        :param path_str: 带提取表达式的字符串 /${id}/state/${create_time}
        :param env: 环境名称， 对应的是环境基准地址
        上述内容表示，从extra_pool字典里取到key为id 对应的值，假设是500，后面${create_time} 类似， 假设其值为 1605711095 最终提取结果
        return  /511/state/1605711095
        """
        url = ReadFile.read_config(
            f'$.server.{env}') + rep_expr(path_str, cls.extra_pool)
        allure_step_no(f'请求地址: {url}')
        return url

    @classmethod
    def handle_header(cls, header_str: str) -> dict:
        """处理header， 将用例中的表达式处理后 追加到基础header中
        :header_str: 用例栏中的header
        return header:
        """
        if header_str == '':
            header_str = '{}'
        cls.header.update(cls.handle_data(header_str))
        allure_step('请求头', cls.header)
        return cls.header

    @classmethod
    def handler_files(cls, file_obj: str) -> object:
        """file对象处理方法
        :param file_obj: 上传文件使用，格式：接口中文件参数的名称:"文件路径地址"/["文件地址1", "文件地址2"]
        实例- 单个文件: &file&D:
        """
        if file_obj != '':
            for k, v in convert_json(file_obj).items():
                # 多文件上传
                if isinstance(v, list):
                    files = []
                    for path in v:
                        files.append((k, (open(path, 'rb'))))
                else:
                    # 单文件上传
                    files = {k: open(v, 'rb')}
            allure_step('上传文件', file_obj)
            return files

    @classmethod
    def handle_data(cls, variable: str) -> dict:
        """请求数据处理
        :param variable: 请求数据，传入的是可转换字典/json的字符串,其中可以包含变量表达式
        return 处理之后的json/dict类型的字典数据
        """
        if variable != '':
            data = rep_expr(variable, cls.extra_pool)
            variable = convert_json(data)
            return variable

    @classmethod
    def handle_sql(cls, sql: str, db: DB):
        """
        处理sql，如果sql执行的结果不会空，执行sql的结果和参数池合并
        :param sql: 支持单条或者多条sql，其中多条sql使用 ; 进行分割
            多条sql,在用例中填写方式如下select * from user; select * from goods 每条sql语句之间需要使用 ; 来分割
            单条sql,select * from user 或者 select * from user;
        :param db: 数据库连接对象
        :return:
        """
        sql = rep_expr(sql, cls.extra_pool)

        for sql in sql.split(";"):
            sql = sql.strip()
            if sql == '':
                continue
            # 查后置sql
            result = db.execute_sql(sql)
            allure_step(f'执行sql: {sql}', result)
            logger.info(f'执行sql: {sql} \n 结果: {result}')
            if result is not None:
                # 将查询结果添加到响应字典里面，作用在，接口响应的内容某个字段 直接和数据库某个字段比对，在预期结果中
                # 使用同样的语法提取即可
                cls.extra_pool.update(result)

    @classmethod
    def handle_extra(cls, extra_str: str, response: dict):
        """
        处理提取参数栏
        :param extra_str: excel中 提取参数栏内容，需要是 {"参数名": "jsonpath提取式"} 可以有多个
        :param response: 当前用例的响应结果字典
        """
        if extra_str != '':
            extra_dict = convert_json(extra_str)
            for k, v in extra_dict.items():
                cls.extra_pool[k] = extractor(response, v)
                logger.info(f'加入依赖字典,key: {k}, 对应value: {v}')

    @classmethod
    def assert_result(cls, response: dict, expect_str: str):
        """ 预期结果实际结果断言方法
        :param response: 实际响应结果
        :param expect_str: 预期响应内容，从excel中读取
        return None
        """
        # 后置sql变量转换
        allure_step("当前可用参数池", cls.extra_pool)
        expect_str = rep_expr(expect_str, cls.extra_pool)
        expect_dict = convert_json(expect_str)
        index = 0
        for k, v in expect_dict.items():
            # 获取需要断言的实际结果部分
            actual = extractor(response, k)
            index += 1
            logger.info(
                f'第{index}个断言,实际结果:{actual} | 预期结果:{v} \n断言结果 {actual == v}')
            allure_step(f'第{index}个断言', f'实际结果:{actual} = 预期结果:{v}')
            try:
                assert actual == v
            except AssertionError:
                raise AssertionError(
                    f'第{index}个断言失败 -|- 实际结果:{actual} || 预期结果: {v}')
