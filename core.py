"""插件类"""
import os
import re
from copy import deepcopy
from datetime import datetime
from decimal import Decimal
from string import Template
from typing import Any, Dict, Optional, Union
from zipfile import ZIP_DEFLATED, ZipFile

import allure
import paramiko
import pymysql
import xlrd
import yagmail
import yaml
from _pytest.outcomes import Skipped
from jsonpath import jsonpath
from loguru import logger

from hooks import *


class ReadFileClass:
    """文件读取类"""

    def __init__(self, path: str, case_expr: str = "$.file_path.test_case"):
        self.path = path
        self.current: Optional[Union[Dict[str, Any], str]] = None
        self._config: Optional[Dict[str, Any]] = None
        self.case_expr = case_expr

    @property
    def config(self):
        if self._config is None:
            self.read()
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    def read(self):
        with open(self.path, "r", encoding="utf-8") as file:
            self.config = yaml.load(file.read(), Loader=yaml.FullLoader)

    def get_config(self, expr: str):
        """获取配置项，传入jsonpath表达式"""
        try:
            self.current = jsonpath(self.config, expr)[0]
        except IndexError:
            self.current = jsonpath(self.config, expr)
        return self

    def get_case(self):
        self.get_config(self.case_expr)
        book = xlrd.open_workbook(self.current)
        # 读取第一个sheet页
        table = book.sheet_by_index(0)
        for norw in range(1, table.nrows):
            yield table.row_values(norw)


class DataBaseMysql:
    """mysql 操作类"""

    def __init__(self, config: ReadFileClass):
        mysql_conf = config.get_config("$.database").current
        self._result = None
        if "ssh_server" in mysql_conf.keys():
            del mysql_conf["ssh_server"]
        self.con = pymysql.connect(
            **mysql_conf, cursorclass=pymysql.cursors.DictCursor, charset="utf8mb4"
        )

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        try:
            json.dumps(value)
        except TypeError:
            for k, v in value.items():
                if isinstance(
                    v,
                    (
                        datetime,
                        Decimal,
                    ),
                ):
                    value[k] = str(v)
        self._result = value

    def __enter__(self):
        logger.success("数据库连接成功")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.success("数据库关闭成功")
        self.con.close()

    def execute_sql(self, sql_str: str):
        with self.con.cursor() as csr:
            csr.execute(sql_str)
            self.result = csr.fetchone()
            self.con.commit()
        logger.debug(f"执行SQL: {sql_str}, {self.result}")


class EmailServe:
    """邮件服务类"""

    def __init__(self, config: ReadFileClass):
        self.email_conf = config.get_config("$.email").current
        self.zip_conf = config.get_config("$.file_path.report").current
        self.zip_name = "report.zip"

    def email(self):
        """邮件服务"""
        with yagmail.SMTP(**self.email_conf["serve"]) as yag:
            yag.send(**self.email_conf["context"])

    def zip(self):
        """压缩报告"""
        with ZipFile(self.zip_name, "w", ZIP_DEFLATED) as zp:
            for path, _, filenames in os.walk(self.zip_conf):
                # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
                fpath = path.replace(self.zip_conf, "")

                for filename in filenames:
                    zp.write(
                        os.path.join(path, filename), os.path.join(fpath, filename)
                    )

    def serve(self):
        logger.info("报告压缩中...")
        self.zip()
        self.email()
        os.remove(self.zip_name)
        logger.success("邮件已发送...")


class RemoteServe:
    """远程服务器"""

    def __init__(
        self,
        host: str,
        port: int = 22,
        username: str = "root",
        password: str = None,
        private_key_file: str = None,
        private_password: str = None,
    ):
        # 进行SSH连接
        self.trans = paramiko.Transport((host, port))
        self.host = host
        if password is None:
            self.trans.connect(
                username=username,
                pkey=paramiko.RSAKey.from_private_key_file(
                    private_key_file, private_password
                ),
            )
        else:
            self.trans.connect(username=username, password=password)
        # 将sshclient的对象的transport指定为以上的trans
        self.ssh = paramiko.SSHClient()
        logger.success("SSH客户端创建成功.")
        self.ssh._transport = self.trans
        # 创建SFTP客户端
        self.ftp_client = paramiko.SFTPClient.from_transport(self.trans)
        logger.success("SFTP客户端创建成功.")

    def execute_cmd(self, cmd: str):
        """
        :param cmd: 服务器下对应的命令
        """
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        error = stderr.read().decode()
        logger.info(f"输入命令: {cmd} -> 输出结果: {stdout.read().decode()}")
        logger.warning(f"异常信息: {error}")
        return error

    def files_action(
        self, post: bool, local_path: str = os.getcwd(), remote_path: str = "/root"
    ):
        """
        :param post: 动作 为 True 就是上传， False就是下载
        :param local_path: 本地的文件路径， 默认当前脚本所在的工作目录
        :param remote_path: 服务器上的文件路径，默认在/root目录下
        """
        if post:  # 上传文件
            self.execute_cmd("mkdir backup_sql")
            self.ftp_client.put(
                localpath=local_path,
                remotepath=f"{remote_path}{os.path.split(local_path)[1]}",
            )
            logger.info(
                f"文件上传成功: {local_path} -> {self.host}:{remote_path}{os.path.split(local_path)[1]}"
            )
        else:  # 下载文件
            if not os.path.exists(local_path):
                os.mkdir(local_path)
            file_path = local_path + os.path.split(remote_path)[1]
            self.ftp_client.get(remotepath=remote_path, localpath=file_path)
            logger.info(f"文件下载成功: {self.host}:{remote_path} -> {file_path}")

    def ssh_close(self):
        """关闭连接"""
        self.trans.close()
        logger.info("已关闭SSH连接...")


class DataClear:
    """数据隔离实现"""

    def __init__(self, config: ReadFileClass):
        self.cfg = config.get_config("$.database").current
        self.server = None
        # 导出的sql文件名称及后缀
        self.file_name = (
            f"{self.cfg.get('db')}_{datetime.now().strftime('%Y-%m-%dT%H_%M_%S')}.sql"
        )

        self.c_name = self.cfg.get("ssh_server").get("mysql_container")
        self.mysql_user = self.cfg.get("user")
        self.mysql_passwd = self.cfg.get("password")
        self.mysql_db = self.cfg.get("db")

        self.local_backup = self.cfg.get("ssh_server").get("sql_data_file")
        self.remote_backup = "/root/backup_sql/"

        # mysql 备份命令
        self.backup_cmd = f"mysqldump -h127.0.0.1 -u{self.mysql_user} -p{self.mysql_passwd} {self.mysql_db}"
        # mysql 还原
        self.recovery_cmd = f"mysql -h127.0.0.1 -u{self.mysql_user} -p{self.mysql_passwd} {self.mysql_db}"

    def backup(self):
        """备份操作"""
        if self.c_name is None:
            cmd = f"{self.backup_cmd}  > {self.file_name}"
        else:
            cmd = f"docker exec -i {self.c_name} {self.backup_cmd} > {self.remote_backup}{self.file_name}"
        self.server.execute_cmd(cmd)

        self.server.files_action(
            0, f"{self.local_backup}", f"{self.remote_backup}{self.file_name}"
        )
        logger.info("备份完成...")

    def recovery(self):
        """还原操作"""
        result = self.server.execute_cmd(f"ls -l {self.remote_backup}{self.file_name}")
        if "No such file or directory" in result:
            # 本地上传
            self.server.files_action(
                1, f"{self.local_backup}{self.file_name}", self.remote_backup
            )
        cmd = f"docker exec -i {self.c_name} {self.recovery_cmd} < {self.remote_backup}{self.file_name}"
        self.server.execute_cmd(cmd)
        logger.success("成功还原...")

    def __enter__(self):
        # 深拷贝
        ssh_cfg = deepcopy(self.cfg.get("ssh_server"))
        del ssh_cfg["mysql_container"]
        del ssh_cfg["sql_data_file"]
        self.server = RemoteServe(host=self.cfg.get("host"), **ssh_cfg)
        # 新建backup_sql文件夹在服务器上，存放导出的sql文件
        self.server.execute_cmd("mkdir backup_sql")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.ssh_close()


class ReportStyle:
    """allure 报告样式"""

    @staticmethod
    def step(step: str, var: Optional[Union[str, Dict[str, Any]]] = None):
        with allure.step(step):
            allure.attach(
                json.dumps(var, ensure_ascii=False, indent=4),
                "附件内容",
                allure.attachment_type.JSON,
            )

    @staticmethod
    def title(title: str):
        allure.dynamic.title(title)


class DataProcess:
    """数据依赖实现"""

    extra_pool = {}

    def __init__(self, config: ReadFileClass):
        self.config = config
        self._headers = None
        self._path = None
        self._body = None
        self._sql = None
        self._files = None
        self._skip = None

    @property
    def skip(self):
        return self._skip

    @skip.setter
    def skip(self, value):
        if isinstance(value, int):
            if value:
                raise Skipped("跳过用例")
        elif eval(self.rep_expr(value).capitalize()):
            raise Skipped("跳过用例")

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = self.config.get_config("$.request_headers").current
        if value != "":
            self._headers.update(DataProcess.handle_data(value))

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self.config.get_config("$.server.dev")
        self._path = f"{self.config.current}{DataProcess.rep_expr(value)}"

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        if self._body != "":
            self._body = DataProcess.handle_data(value)

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, value):
        if value != "":
            for k, v in DataProcess.handle_data(value).items():
                # 多文件上传
                if isinstance(v, list):
                    self._files = [(k, (open(path, "rb"))) for path in v]
                else:
                    # 单文件上传
                    self._files = {k: open(v, "rb")}
        else:
            self._files = None

    @property
    def sql(self):
        return self._sql

    @sql.setter
    def sql(self, value):
        self._sql = DataProcess.rep_expr(value)

    @classmethod
    def handle_data(cls, value: str) -> Optional[Dict[str, Any]]:
        """处理数据的方法"""
        if value == "":
            return
        try:
            return json.loads(DataProcess.rep_expr(value))
        except json.decoder.JSONDecodeError:
            return eval(DataProcess.rep_expr(value))

    @classmethod
    def rep_expr(cls, content: str):
        content = Template(content).safe_substitute(DataProcess.extra_pool)
        for func in re.findall("\\${(.*?)}", content):
            try:
                content = content.replace("${%s}" % func, DataProcess.exec_func(func))
            except Exception as e:
                logger.error(e)
        return content

    def handle_case(self, path, header, skip_expr, data, file):
        self.skip = skip_expr
        self.path = path
        self.headers = header
        self.body = data
        self.files = file

    def handle_sql(self, db_session: DataBaseMysql):
        for sql_str in self.sql.split(";"):
            sql_str = sql_str.strip()
            if sql_str == "":
                continue
            # 查后置sql
            db_session.execute_sql(sql_str)
            ReportStyle.step(f"执行sql: {sql_str}", db_session.result)
            logger.info(f"执行sql: {sql_str} \n 结果: {db_session.result}")
            if db_session.result is not None:
                # 将查询结果添加到响应字典里面，作用在，接口响应的内容某个字段 直接和数据库某个字段比对，在预期结果中
                # 使用同样的语法提取即可
                DataProcess.extra_pool.update(db_session.result)

    @staticmethod
    def extractor(obj: dict, expr: str = ".") -> Any:
        """
        根据表达式提取字典中的value，表达式, . 提取字典所有内容， $.case 提取一级字典case， $.case.data 提取case字典下的data
        :param obj :json/dict类型数据
        :param expr: 表达式, . 提取字典所有内容， $.case 提取一级字典case， $.case.data 提取case字典下的data
        $.0.1 提取字典中的第一个列表中的第二个的值
        """
        try:
            result = jsonpath(obj, expr)[0]
        except Exception as e:
            logger.error(f"{expr} - 提取不到内容，丢给你一个错误！{e}")
            result = expr
        return result

    @classmethod
    def handle_extra(cls, extra_str: str, response: dict):
        """
        处理提取参数栏
        :param extra_str: excel中 提取参数栏内容，需要是 {"参数名": "jsonpath提取式"} 可以有多个
        :param response: 当前用例的响应结果字典
        """
        if extra_str != "":
            extra_dict = json.loads(extra_str)
            for k, v in extra_dict.items():
                DataProcess.extra_pool[k] = DataProcess.extractor(response, v)
                logger.info(f"加入依赖字典,key: {k}, 对应value: {v}")

    @classmethod
    def assert_result(cls, response: dict, expect_str: str):
        """预期结果实际结果断言方法
        :param response: 实际响应结果
        :param expect_str: 预期响应内容，从excel中读取
        return None
        """
        # 后置sql变量转换
        ReportStyle.step("当前可用参数池", DataProcess.extra_pool)
        index = 0
        for k, v in DataProcess.handle_data(expect_str).items():
            # 获取需要断言的实际结果部分
            actual = DataProcess.extractor(response, k)
            index += 1
            assert_info = {"提取实际结果": k, "实际结果": actual, "预期结果": v, "测试结果": actual == v}
            logger.info(f"断言{index}: {assert_info}")
            ReportStyle.step(f"断言{index}", assert_info)
            assert actual == v

    @staticmethod
    def exec_func(func: str) -> str:
        """执行函数(exec可以执行Python代码)
        :params func 字符的形式调用函数
        : return 返回的将是个str类型的结果
        """
        # 得到一个局部的变量字典，来修正exec函数中的变量，在其他函数内部使用不到的问题
        loc = locals()
        exec(f"result = {func}")
        return str(loc["result"])


import json
import os
import subprocess


def go_client(cmd: str):
    exe_path = f"{os.getcwd()}/lib/client"
    result = subprocess.run(exe_path + cmd, capture_output=True, shell=True)
    info = result.stdout.decode()
    if info == "":
        raise RuntimeError("💫出现异常，请检查请求内容")
    else:
        return json.load(info)


def send_request(data_type: str, method, url, header=None, data=None, file=None):
    if data_type not in ["params", "data", "json"]:
        raise ValueError("可选关键字为params, json, data")

    # 查询参数
    if data_type == "params":
        from urllib.parse import urlencode

        url = url + "?" + urlencode(data)
    cmd = f" -url {url} -method {method} -header {'' if header is None else json.dumps(header)} -file {'' if file is None else json.dumps(file)}"
    # 表单
    if data_type == "data":
        cmd += f" -data {'' if data is None else json.dumps(data)}"

    if data_type == "json":
        cmd += f" -json {'' if data is None else json.dumps(data)}"

    res = go_client(cmd)
    response = res.get("response")

    req_info = {
        "请求地址": url,
        "请求方法": method,
        "请求头": header,
        "请求数据": data,
        "上传文件": str(file),
    }
    ReportStyle.step("Request Info", req_info)
    logger.info(req_info)
    rep_info = {
        "请求耗时": response.get("track"),
        "状态码": response.get("status"),
        "响应数据": json.loads(response.get("body")),
    }
    logger.info(rep_info)
    ReportStyle.step("Response Info", rep_info)
    ReportStyle.step("完整内容", res)
    return json.loads(response.get("body"))
