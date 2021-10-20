# -*- coding: utf-8 -*-
# @Time : 2021/7/26 21:55
# @Author : zy7y
# @Gitee : https://gitee.com/zy7y
# @File : models.py
# @Project : fastapi-mock
from enum import Enum

from tortoise import fields, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class Methods(str, Enum):
    """请求方法类型"""
    POST = 'post'
    DELETE = 'delete'
    GET = 'get'
    PUT = 'put'


class MockApi(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(255, description="名称", unique=True)
    method = fields.CharEnumField(
        Methods,
        description="请求方法",
        default=Methods.GET)
    path = fields.CharField(255, description="接口地址")
    status = fields.BooleanField(default=True, description="是否启用, 1启用 0 禁用")
    body = fields.JSONField(default={}, description="响应体")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


# 解决pydantic_model_creator 生成的模型中 缺少外键关联字段
Tortoise.init_models(["models"], "models")


MockApi_Pydantic = pydantic_model_creator(MockApi, name="MockApi")
MockApiIn_Pydantic = pydantic_model_creator(
    MockApi, name="MockApiIn", exclude_readonly=True)
