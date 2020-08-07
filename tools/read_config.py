#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: read_config.py
@ide: PyCharm
@time: 2020/7/31
"""
import yaml
from loguru import logger


class ReadConfig(object):
    data = None
    @logger.catch
    def __init__(self):
        with open('../config/config.yaml', 'r') as file:
            self.data = yaml.load(file.read(), Loader=yaml.FullLoader)

    @logger.catch
    def read_serve_config(self, sever_name):
        logger.info(self.data.get('server').get(sever_name))
        return self.data.get('server').get(sever_name)

    @logger.catch
    def read_response_reg(self):
        # get_token = self.data.get("response_reg").get("token")
        # get_resp = self.data.get('response_reg').get('response')
        # 该写法与上面写法效果类似，随意选择
        get_token = self.data["response_reg"]["token"]
        get_resp = self.data['response_reg']['response']
        
        logger.info(f'从响应中提取的token表达式: {get_token}')
        logger.info(f'从响应提取的需要校验的表达式: {get_resp}')
        return get_token, get_resp

    @logger.catch
    def read_file_path(self, file_path_name):
        return self.data.get('file_path').get(file_path_name)

    def read_email_setting(self):
        return self.data.get('email')


if __name__ == '__main__':
    rc = ReadConfig()
    print(rc.read_email_setting().get('addressees'), type(rc.read_email_setting().get('addressees')))

