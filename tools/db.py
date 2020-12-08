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

import pymysql

from tools.read_file import ReadFile


class DB:
    mysql = ReadFile.read_config('$.database')

    def __init__(self):
        """初始化连接Mysql"""
        self.connection = pymysql.connect(
            host=self.mysql.get('host', 'localhost'),
            port=self.mysql.get('port', 3306),
            user=self.mysql.get('user', 'root'),
            password=self.mysql.get('password', '123456'),
            db=self.mysql.get('db_name', 'test'),
            charset=self.mysql.get('charset', 'utf8mb4'),
            cursorclass=pymysql.cursors.DictCursor
        )

    def fetch_one(self, sql: str) -> object:
        """查询数据，查一条"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            # 使用commit解决查询数据出现概率查错问题
            self.connection.commit()
        return result

    def close(self):
        """关闭数据库连接"""
        self.connection.close()


if __name__ == '__main__':
    print(ReadFile.read_config('$.database'))
    DB()
