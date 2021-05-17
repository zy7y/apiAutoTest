#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: db.py
@ide: PyCharm
@time: 2020/12/4
@desc: 数据库连接,目前只支持mysql ，且个人认为用到最多的操作应该是查询所以其他todo
"""
import json
from datetime import datetime
from typing import Union

import pymysql

from tools.read_file import ReadFile


class DB:
    mysql = ReadFile.read_config('$.database')

    def __init__(self):
        """
        初始化数据库连接，并指定查询的结果集以字典形式返回
        """
        self.connection = pymysql.connect(
            host=self.mysql['host'],
            port=self.mysql['port'],
            user=self.mysql['user'],
            password=self.mysql['password'],
            db=self.mysql['db_name'],
            charset=self.mysql.get('charset', 'utf8mb4'),
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute_sql(self, sql: str) -> Union[dict, None]:
        """
        执行sql语句方法，查询所有结果的sql只会返回一条结果（
        比如说： 使用select * from cases , 结果将只会返回第一条数据    {'id': 1, 'name': 'updatehahaha', 'path': None, 'body': None, 'expected': '{"msg": "你好"}', 'api_id': 1, 'create_at': '2021-05-17 17:23:54', 'update_at': '2021-05-17 17:23:54'}

        ），支持select， delete， insert， update
        :param sql: sql语句
        :return: select 语句 如果有结果则会返回 对应结果字典，delete，insert，update 将返回None
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            # 使用commit解决查询数据出现概率查错问题
            self.connection.commit()
            return self.verify(result)

    def verify(self, result: dict) -> Union[dict, None]:
        """验证结果能否被json.dumps序列化"""
        # 尝试变成字符串，解决datetime 无法被json 序列化问题
        try:
            json.dumps(result)
        except TypeError:   # TypeError: Object of type datetime is not JSON serializable
            for k, v in result.items():
                if isinstance(v, datetime):
                    result[k] = str(v)
        return result

    def close(self):
        """关闭数据库连接"""
        self.connection.close()
