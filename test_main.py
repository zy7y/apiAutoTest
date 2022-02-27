import pytest

from core import DataBaseMysql
from core import DataProcess
from core import ReadFileClass
from core import ReportStyle
from core import HttpRequest

rfc = ReadFileClass("config.yaml")
http_client = HttpRequest()
data_process = DataProcess(rfc)


@pytest.fixture(scope="session")
def data_clearing():
    """数据清理"""
    from core import DataClear

    with DataClear(rfc) as dc:
        dc.backup()
        yield
        dc.recovery()


@pytest.fixture(scope="session")
def get_db():
    """数据库对象"""
    with DataBaseMysql(rfc) as db:
        yield db


@pytest.fixture(params=rfc.get_case())
def case(request):
    """用例数据，测试方法参数入参该方法名 cases即可，实现同样的参数化
    目前来看相较于@pytest.mark.parametrize 更简洁。
    """
    return request.param


@pytest.fixture(scope="session")
def clear_db(data_clearing):
    """同时使用数据清洗 和 数据库操作功能"""
    with DataBaseMysql(rfc) as db:
        yield db


# def test_start(case, get_db): # 只使用数据库操作
# def test_start(case, clear_db): # 使用数据库操作 及 数据清洗
def test_start(case):  # 不使用数据库操作
    """
    测试启动方法， 当需要使用 数据清洗和 数据库操作命令时将 get_db 换成 clear_db
    如只需要使用 数据库操作 则添加get_db 参数， 如一个都不需要则不添加
    :param case: 用例
    :return:
    """
    # 前置处理
    title, skip, header, path, method, data_type, file, data, extra, sql, expect = case
    ReportStyle.title(title)
    data_process.handle_case(path, header, skip, data, file)

    # 发送请求
    http_client.send_request(
        data_type,
        method,
        data_process.path,
        data_process.headers,
        data_process.body,
        data_process.files,
    )
    # 后置处理
    DataProcess.handle_extra(extra, http_client.response.json())

    data_process.sql = sql
    # data_process.handle_sql(get_db) # 使用数据库
    # data_process.handle_sql(clear_db) # 使用数据清洗及 数据库

    # 断言
    DataProcess.assert_result(http_client.response.json(), expect)
