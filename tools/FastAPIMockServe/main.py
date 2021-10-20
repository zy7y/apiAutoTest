"""

该功能简单mock，并未代理转发实际就是请求 本机添加的接口服务 拿去被调用而已
添加的mock服务接口使用： http"//127.0.0.1/mock/xx 调用 其中 xx 为你添加服务的地址, 具体通过调用
http://127.0.0.1:8000/service 获取所用的mock
相关使用视频 参考 https://www.bilibili.com/video/BV1yf4y157Pv
"""
from typing import Union

from fastapi import FastAPI
from fastapi import Path
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from tortoise.contrib.fastapi import register_tortoise

import models
from schemas import Success, Fail, ServeNotFount

app = FastAPI(
    title="FastAPI-Mock v0.1",
    description="""
    >依靠FastAPI，Path参数来实现Mock的接口服务，服务地址:`IP:PORT/mock/xx`,后续知晓更好的方法会再更新的
    """
)

# 挂载 数据库
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    # 生成表
    generate_schemas=True,
    # 使用异常，当无数据是自动返回
    add_exception_handlers=True,
)

# 跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/service", name="添加服务", response_model=Union[Success, Fail])
async def create(mock: models.MockApiIn_Pydantic):
    try:
        project_obj = await models.MockApi.create(**mock.dict(exclude_unset=True))
        # from_tortoise_orm 从 数据表中序列化， 针对 模型类对象
        return Success(data=await models.MockApi_Pydantic.from_tortoise_orm(project_obj))
    except Exception as e:
        return Fail()


@app.delete("/service/{m_id}", name="删除服务")
async def delete(m_id: int):
    project_obj = await models.MockApi.filter(id=m_id).delete()
    if project_obj:
        return Success(data=project_obj)
    return Fail()


@app.get("/service", name="获取所有服务")
async def select_all(limit: int = 10, page: int = 1):
    skip = (page - 1) * limit
    # from_queryset 针对queryset 对象序列化
    data = await models.MockApi_Pydantic.from_queryset(models.MockApi.all().order_by('-created_at').offset(skip).limit(limit))
    # await models.Project.all().count()
    return Success(data={"total": await models.MockApi.all().count(), "items": data})


@app.get("/service/{m_id}", name="获取服务详细")
async def select(m_id: int):
    data = await models.MockApi_Pydantic.from_queryset_single(models.MockApi.get(id=m_id))
    return Success(data=data)


@app.put("/service/{m_id}", name="编辑服务")
async def update(m_id: int, project: models.MockApiIn_Pydantic):
    await models.MockApi.filter(id=m_id).update(**project.dict(exclude_unset=True))
    return Success(data=await models.MockApi_Pydantic.from_queryset_single(models.MockApi.get(id=m_id)))


# https://gitee.com/ran_yong 纠正
@app.api_route("/mock/{url}", methods=["post", "get", "delete", "put"])
async def mock(request: Request, url: str = Path(...)):
    try:
        mocks = await models.MockApi.filter(path=url, status=True, method=request.method.lower()).first()
        return mocks.body
    except Exception as e:
        return ServeNotFount()


# 和上面方法 实现一致，
# async def mock(request: Request, url: str = Path(...)):
#     try:
#         mocks = await models.MockApi.filter(path=url, status=True).first()
#         return mocks.body if mocks.method.upper() == request.method else ServeNotFount()
#     except Exception as e:
#         return ServeNotFount()
#
# app.add_api_route(
#     "/mock/{url}",
#     endpoint=mock,
#     methods=[
#         "post",
#         "get",
#         "delete",
#         "put"],
#     include_in_schema=False
# )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)

    # 也可使用命令行启动
    # uvicorn main:app --reload

    # 127.0.0.1:8000/docs 添加mock 接口

