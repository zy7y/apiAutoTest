#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: run.py
@ide: PyCharm
@time: 2020/12/16
@github: https://github.com/zy7y
@site: https://cnblogs.com/zy7y
@desc: 运行文件
"""

import os
import shutil
from test.conftest import pytest
from tools import logger
from tools.read_file import ReadFile

report = ReadFile.read_config('$.file_path.report')
logfile = ReadFile.read_config('$.file_path.log')


def run():
    if os.path.exists('report/'):
        shutil.rmtree(path='report/')
    logger.add(logfile, enqueue=True, encoding='utf-8')
    logger.info("""
                 _    _         _      _____         _   
  __ _ _ __ (_)  / \  _   _| |_ __|_   _|__  ___| |_ 
 / _` | '_ \| | / _ \| | | | __/ _ \| |/ _ \/ __| __|
| (_| | |_) | |/ ___ \ |_| | || (_) | |  __/\__ \ |_ 
 \__,_| .__/|_/_/   \_\__,_|\__\___/|_|\___||___/\__|
      |_|                                            
      Starting      ...     ...     ...
    """)
    pytest.main(args=['test/test_api.py', f'--alluredir={report}/data'])
    # 自动以服务形式打开报告
    # os.system(f'allure serve {report}/data')

    # 本地生成报告
    os.system(f'allure generate {report}/data -o {report}/html --clean')
    logger.success('报告已生成')


if __name__ == '__main__':
    run()


