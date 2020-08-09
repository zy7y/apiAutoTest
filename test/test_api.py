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
from json import JSONDecodeError

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
    def setup(self):
        logger.info('用例运行开始=====')

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

    def treating_data(self, is_token, parameters, dependent, data):
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

        # 处理路径参数Path的依赖
        # 传进来的参数类似 {"case_002":"$.data.id"}/item/{"case_002":"$.meta.status"}，进行列表拆分
        path_list = parameters.split('/')
        logger.error(f'{parameters}')
        logger.error(f'{path_list}')
        # 获取列表长度迭代
        for i in range(len(path_list)):
            # 按着
            try:
                # 尝试序列化成dict:   json.loads('2') 可以转换成2
                path_dict = json.loads(path_list[i])
            except JSONDecodeError as e:
                # 序列化失败此path_list[i]的值不变化
                logger.debug(f'无法转换字典，进入下一个检查，本轮值不发生变化:{path_list[i]},\n {e}')
                # 跳过进入下次循环
                continue
            else:
                # 解析该字典，获得用例编号，表达式
                logger.error(f'{path_dict}')
                # 处理json.loads('数字')正常序列化导致的AttributeError
                try:
                    for k, v in path_dict.items():
                        try:
                            # 尝试从对应的case实际响应提取某个字段内容
                            path_list[i] = jsonpath.jsonpath(save_response_dict.actual_response[k], v)[0]
                        except TypeError as e:
                            logger.info(f'无法提取，请检查响应字典中是否支持该表达式,{e}')
                except AttributeError as e:
                    logger.info(f'类型错误:{type(path_list[i])}，本此将不转换值 {path_list[i]},\n {e}')

        logger.error(f"==== {path_list}")
        # 字典中存在有不是str的元素:使用map 转换成全字符串的列表
        path_list = map(str, path_list)

        # 将字符串列表转换成字符：500/item/200
        parameters_path_url = "/".join(path_list)
        logger.info(f'path路径参数解析依赖后的路径为{parameters_path_url}')
        return data, header, parameters_path_url

    @pytest.mark.parametrize('case_number,path,is_token,method,parametric_key,file_var,'
                             'file_path, parameters, dependent,data,expect,actual', data_list, ids=title_ids)
    def test_main(self, case_number, path, is_token, method, parametric_key, file_var, file_path, parameters,
                  dependent, data, expect, actual):

        with allure.step("处理相关数据依赖，header"):
            data, header, parameters_path_url = self.treating_data(is_token, parameters, dependent, data)
        with allure.step("发送请求，取得响应结果的json串"):
            res = br.base_requests(method=method, url=base_url + path + parameters_path_url, parametric_key=parametric_key, file_var=file_var, file_path=file_path,
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




