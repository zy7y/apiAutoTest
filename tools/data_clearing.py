#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time : 2021/1/19 11:44
@Author : zy7y
@ProjectName : apiAutoTest
@File : data_clearing.py
@Software : PyCharm
@Github : https://github.com/zy7y
@Blog : https://www.cnblogs.com/zy7y
"""

import os
from datetime import datetime
import paramiko
from tools.read_file import ReadFile
from tools import logger


class ServerTools:
    def __init__(
            self,
            host: str,
            port: int = 22,
            username: str = "root",
            password: str = None,
            private_key_file: str = None,
            privat_passowrd: str = None):
        # 进行SSH连接
        self.trans = paramiko.Transport((host, port))
        self.host = host
        if password is None:
            self.trans.connect(
                username=username,
                pkey=paramiko.RSAKey.from_private_key_file(
                    private_key_file,
                    privat_passowrd))
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
        logger.error(f"异常信息: {error}")
        return error

    def files_action(
            self,
            post: bool,
            local_path: str = os.getcwd(),
            remote_path: str = "/root"):
        """
        :param post: 动作 为 True 就是上传， False就是下载
        :param local_path: 本地的文件路径， 默认当前脚本所在的工作目录
        :param remote_path: 服务器上的文件路径，默认在/root目录下
        """
        if post:  # 上传文件
            self.ftp_client.put(
                localpath=local_path,
                remotepath=f"{remote_path}{os.path.split(local_path)[1]}")
            logger.info(
                f"文件上传成功: {local_path} -> {self.host}:{remote_path}{os.path.split(local_path)[1]}")
        else:  # 下载文件
            file_path = local_path + os.path.split(remote_path)[1]
            self.ftp_client.get(remotepath=remote_path, localpath=file_path)
            logger.info(f"文件下载成功: {self.host}:{remote_path} -> {file_path}")

    def ssh_close(self):
        """关闭连接"""
        self.trans.close()
        logger.info("已关闭SSH连接...")


class DataClearing:
    settings = ReadFile.read_config('$.database')
    server_settings = settings.get('ssh_server')
    server = None

    # 导出的sql文件名称及后缀
    file_name = f"{settings.get('db_name')}_{datetime.now().strftime('%Y-%m-%dT%H_%M_%S')}.sql"

    @classmethod
    def server_init(cls, settings=settings, server_settings=server_settings):
        cls.server = ServerTools(
            host=settings.get('host'),
            port=server_settings.get('port'),
            username=server_settings.get('username'),
            password=server_settings.get('password'),
            private_key_file=server_settings.get('private_key_file'),
            privat_passowrd=server_settings.get('privat_passowrd'))
        # 新建backup_sql文件夹在服务器上，存放导出的sql文件
        cls.server.execute_cmd("mkdir backup_sql")

    @classmethod
    def backup_mysql(cls):
        """
        备份数据库, 会分别备份在数据库所在服务器的/root/backup_sql/目录下, 与当前项目文件目录下的 backup_sqls
        每次备份生成一个数据库名_当前年_月_日T_时_分_秒, 支持linux 服务器上安装的mysql服务(本人未调试),以及linux中docker部署的mysql备份
        """
        if cls.server_settings.get('mysql_container') is None:
            cmd = f"mysqldump -h127.0.0.1 -u{cls.settings.get('username')} -p{cls.settings.get('password')} {cls.settings.get('db_name')} > {cls.file_name}"
        else:
            # 将mysql服务的容器中的指定数据库导出， 参考文章
            # https://www.cnblogs.com/wangsongbai/p/12666368.html
            cmd = f"docker exec -i {cls.server_settings.get('mysql_container')} mysqldump -h127.0.0.1 -u{cls.settings.get('user')} -p{cls.settings.get('password')} {cls.settings.get('db_name')} > /root/backup_sql/{cls.file_name}"
        cls.server.execute_cmd(cmd)
        cls.server.files_action(0,
                                f"{cls.server_settings.get('sql_data_file')}",
                                f"/root/backup_sql/{cls.file_name}")

    @classmethod
    def recovery_mysql(
            cls,
            sql_file: str = file_name,
            database: str = settings.get('db_name')):
        """
        恢复数据库, 从服务器位置(/root/backup_sql/) 或者本地(../backup_sqls)上传, 传入的需要是.sql文件
        :param sql_file: .sql数据库备份文件, 默认就是导出的sql文件名称， 默认文件名称是导出的sql文件
        :param database: 恢复的数据库名称，默认是备份数据库(config.yaml中的db_name)
        """
        result = cls.server.execute_cmd(f"ls -l /root/backup_sql/{sql_file}")
        if "No such file or directory" in result:
            # 本地上传
            cls.server.files_action(
                1, f"../backup_sqls/{sql_file}", "/root/backup_sql/")
        cmd = f"docker exec -i {cls.server_settings.get('mysql_container')} mysql -u{cls.settings.get('user')} -p{cls.settings.get('password')} {database} < /root/backup_sql/{sql_file}"
        cls.server.execute_cmd(cmd)

    @classmethod
    def close_client(cls):
        cls.server.ssh_close()
