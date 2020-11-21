#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: test_api.py
@ide: PyCharm
@time: 2020/7/31
"""
import pytest
from api.base_requests import BaseRequest
from tools import *
from tools.data_process import DataProcess
from tools.read_file import ReadFile

base_url = ReadFile.read_config('$.server.dev')
res_reg = ReadFile.read_config('$.expr.response')
report_data = ReadFile.read_config('$.file_path.report_data')
report_generate = ReadFile.read_config('$.file_path.report_generate')
log_path = ReadFile.read_config('$.file_path.log_path')
# 读取excel数据对象
data_list = ReadFile.read_testcase()
# 请求对象
br = BaseRequest()
logger.info(f'配置文件/excel数据/对象实例化，等前置条件处理完毕\n\n')


class TestApiAuto(object):
    # 启动方法
    def run_test(self):
        import os, shutil
        if os.path.exists('../report') and os.path.exists('../log'):
            shutil.rmtree(path='../report')
            shutil.rmtree(path='../log')
        # 日志存取路径
        logger.add(log_path, encoding='utf-8')
        pytest.main(args=[f'--alluredir={report_data}'])
        # 本地生成 allure 报告文件，需注意 不用pycharm等类似ide 打开会出现无数据情况
        os.system(f'allure generate {report_data} -o {report_generate} --clean')

        # 直接启动allure报告（会占用一个进程，建立一个本地服务并且自动打开浏览器访问，ps 程序不会自动结束，需要自己去关闭）
        # os.system(f'allure serve {report_data}')
        logger.warning('报告已生成')

    @pytest.mark.parametrize('case_number,case_title,path,is_token,method,parametric_key,file_obj,'
                             'data,expect', data_list)
    def test_main(self, case_number, case_title, path, is_token, method, parametric_key, file_obj,
                data, expect):
        logger.debug(f'⬇️⬇️⬇️...执行用例编号:{case_number}...⬇️⬇️⬇️️')

        allure_title(case_title)
        path = DataProcess.handle_path(path)
        allure_step('请求地址', base_url + path)
        allure_step('请求方式', method)
        header = DataProcess.handle_header(is_token)
        allure_step('请求头', header)
        data = DataProcess.handle_data(data)
        allure_step('请求数据', data)
        res = br.api_send(method=method, url=base_url + path, parametric_key=parametric_key, file_obj=file_obj,
                          data=data, header=header)
        allure_step('实际响应结果', res)
        DataProcess.save_response(case_number, res)
        allure_step('响应结果写入字典', DataProcess.response_dict)
        # 写token的接口必须是要正确无误能返回token的
        if is_token == '写':
            DataProcess.have_token['Authorization'] = extractor(res, ReadFile.read_config('$.expr.token'))
        really = extractor(res, res_reg)
        allure_step('根据配置文件的提取响应规则提取实际数据', really)
        expect = convert_json(expect)
        allure_step('处理读取出来的预期结果响应', expect)
        allure_step('响应断言', (really == expect))

        assert really == expect


if __name__ == '__main__':
    TestApiAuto().run_test()

    # 使用jenkins集成将不会使用到这两个方法（邮件发送/报告压缩zip）
    # from tools.zip_file import zipDir
    # from tools.send_email import send_email
    # zipDir(report_generate, report_zip)
    # send_email(email_setting)




