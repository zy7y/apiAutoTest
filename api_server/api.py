#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: api.py
@ide: PyCharm
@time: 2020/11/20
@desc: 上传文件接口服务,用于调试上传文件接口处理方法，源码来自
FastAPI官网 https://fastapi.tiangolo.com/zh/tutorial/request-files/
"""

from typing import List

from fastapi import FastAPI, File, UploadFile, Form

app = FastAPI()


@app.post("/upload_file/", name='上传单文件接口')
async def create_upload_file(file_excel: UploadFile = File(...)):
    # 单文件上传接口，并将文件写到服务器地址， 接收文件对象的参数 是 file_excel
    # 读取文件
    contents = await file_excel.read()
    # 保存本地
    with open(file_excel.filename, "wb") as f:
        f.write(contents)
    return {'msg': '操作成功', "filename": file_excel.filename, 'username': username, "meta": {"msg": "ok"}}


@app.post("/upload_files/", name='上传多个文件')
async def create_upload_files(files: List[UploadFile] = File(...)):
    # 多文件上传接口，并将文件写到服务器, 接收文件对象的参数 是 files
    for file in files:
        # 读取文件
        contents = await file.read()
        # 保存本地
        with open(file.filename, "wb") as f:
            f.write(contents)
    return {"filenames": [file.filename for file in files], "meta": {"msg": "ok"}}


if __name__ == '__main__':
    # 启动项目后 访问  http://127.0.0.1:8000/docs 可查看接口文档
    import uvicorn
    uvicorn.run('api:app', reload=True)
