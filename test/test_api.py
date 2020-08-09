#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: test_api.py
@ide: PyCharm
@time: 2020/7/31
"""
import json
import shutil

import jsonpath
from loguru import logger
import pytest
import allure
from api.base_requests import BaseRequest
from tools.read_config import ReadConfig
from tools.read_data import ReadData
from tools.save_response import SaveResponse

rc = ReadConfig()
base_url = rc.read_serve_config('dev')
token_reg, res_reg = rc.read_response_reg()
case_data_path = rc.read_file_path('case_data')
report_data = rc.read_file_path('report_data')
report_generate = rc.read_file_path('report_generate')
log_path = rc.read_file_path('log_path')
report_zip = rc.read_file_path('report_zip')
email_setting = rc.read_email_setting()
# 实例化存响应的对象
save_response_dict = SaveResponse()

data_list, title_ids = ReadData(case_data_path).get_data()

br = BaseRequest()
token_header = {}
no_token_header = {}


class TestApiAuto(object):

    # 使用jenkins后可以不用zip压缩已经发送邮件的方法
    def start_run_test(self):
        import os
        if os.path.exists('../report') and os.path.exists('../log'):
            shutil.rmtree(path='../report')
            shutil.rmtree(path='../log')
        logger.add(log_path)

        pytest.main(args=[f'--alluredir={report_data}'])
        # # 启动一个web服务的报告
        # os.system(f'allure serve {report_data}')
        os.system(f'allure generate {report_data} -o {report_generate} --clean')
        logger.debug('报告已生成')

    def treating_data(self, is_token, dependent, data):
        # 使用那个header
        if is_token == '':
            header = no_token_header
        else:
            header = token_header
        logger.info(f'处理依赖前data的数据:{data} \n')
        # 处理依赖数据data
        if dependent != '':
            # dependent_data = ReadData(case_data_path).read_actual(dependent)  # 从对应case实际响应栏中读取数据并进行依赖处理
            dependent_data = save_response_dict.read_depend_data(dependent)
            logger.debug(f'依赖数据解析获得的字典{dependent_data}')
            if data != '':
                # 合并组成一个新的data
                dependent_data.update(json.loads(data))
                data = dependent_data
                logger.debug(f'data有数据，依赖有数据时 {data}')
            else:
                # 赋值给data
                data = dependent_data
                logger.debug(f'data无数据，依赖有数据时 {data}')
        else:
            if data == '':
                data = None
                logger.debug(f'data无数据，依赖无数据时 {data}')
            else:
                data = json.loads(data)
                logger.debug(f'data有数据，依赖无数据 {data}')
        return data, header

    @pytest.mark.parametrize('case_number,path,is_token,method,parametric_key,file_var,'
                             'file_path, parameters, dependent,data,expect,actual', data_list, ids=title_ids)
    def test_main(self, case_number, path, is_token, method, parametric_key, file_var, file_path, parameters,
                  dependent, data, expect, actual):
        logger.warning(f"=========用例编号：{case_number}===========开始运行=====\n")
        with allure.step("处理相关数据依赖，header"):
            data, header = self.treating_data(is_token, dependent, data)
        with allure.step("发送请求，取得响应结果的json串"):
            res = br.base_requests(method=method, url=base_url + path, parametric_key=parametric_key, file_var=file_var, file_path=file_path,
                                   data=data, header=header)
        with allure.step("将响应结果的内容写入实际响应字典/excel实际结果栏中"):
            # ReadData(case_data_path).write_result(case_number, res)   # 向excel对应case中写入实际响应
            save_response_dict.save_actual_response(case_key=case_number, case_response=res)

            # 写token的接口必须是要正确无误能返回token的
            if is_token == '写':
                with allure.step("从登录后的响应中提取token到header中"):
                    token_header['Authorization'] = jsonpath.jsonpath(res, token_reg)[0]
            logger.info(f'token_header: {token_header}, \n no_token_header: {no_token_header}')
        with allure.step("根据配置文件的提取响应规则提取实际数据"):
            really = jsonpath.jsonpath(res, res_reg)[0]
        with allure.step("处理读取出来的预期结果响应"):
            expect = eval(expect)
        with allure.step("预期结果与实际响应进行断言操作"):
            assert really == expect
            logger.info(f'完整的json响应: {res}\n 需要校验的数据字典: {really}\n 预期校验的数据字典: {expect}\n 测试结果: {really == expect}\n')


if __name__ == '__main__':
    t1 = TestApiAuto()
    t1.start_run_test()
    # 使用jenkins集成将不会使用到这两个方法
    # from tools.zip_file import zipDir
    # from tools.send_email import send_email
    # zipDir(report_generate, report_zip)
    # send_email(email_setting)




