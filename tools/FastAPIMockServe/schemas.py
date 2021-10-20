# -*- coding: utf-8 -*-
# @Time : 2021/7/26 22:14
# @Author : zy7y
# @Gitee : https://gitee.com/zy7y
# @File : schemas.py
# @Project : fastapi-mock
from typing import Union, Any

from pydantic import BaseModel


class Response(BaseModel):
    code: Union[int] = 200
    data: Any


class Success(Response):
    data: Any = None


class Fail(Response):
    code: int = 400
    data: None = None


class ServeNotFount(BaseModel):
    code: int = 404
    data: None = None
    error: str = "服务不存在"
