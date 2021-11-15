![](https://img.shields.io/github/license/zy7y/apiAutoTest)
![](https://img.shields.io/github/stars/zy7y/apiAutoTest)
![](https://img.shields.io/github/forks/zy7y/apiAutoTest)

> 使用Python为语言工具 + Python第三方库 实现的接口自动化测试工具

[![IsXMnO.png](https://z3.ax1x.com/2021/11/13/IsXMnO.png)](https://imgtu.com/i/IsXMnO)

## 配套资源(点击即可跳转)
- [x] [使用手册](https://zy7y.github.io/apiAutoTest/)
- [x] [视频解析](https://www.bilibili.com/video/BV1rr4y1r754)


## 实现功能
- 测试数据隔离: 测试前后进行数据库备份/还原
- 接口直接的数据依赖: 需要B接口使用A接口响应中的某个字段作为参数
- 对接数据库： 讲数据库的查询结果可直接用于断言操作
- 动态多断言： 可（多个）动态提取实际预期结果与指定的预期结果进行比较断言操作
- 自定义扩展方法： 在用例中使用自定义方法(如：获取当前时间戳...)的返回值 
- 邮件发送：将allure报告压缩后已附件形式发送
- 接口录制：录制指定包含url的接口,生成用例数据
## 依赖库
```
allure-pytest==2.8.17		# allure报告
jsonpath==0.82				# json解析库
loguru==0.5.1				# 日志库
pytest==6.0.1				# 参数化
PyYAML==5.3.1				# 读取ymal
requests==2.24.0			# 请求HTTP/HTTPS
xlrd==1.2.0					# 读取excel
yagmail==0.11.224			# 发送邮件
PyMySQL==0.10.1				# 连接mysql数据库
pytest-rerunfailures==9.1.1	# 用例失败重跑
paramiko==2.7.2				# SSH2 连接
xlwt==1.3.0                 # 写excel 用例文件
mitmproxy==6.0.2            # 抓包工具
```
## 目录结构
```shell
├─api
│  └─client.py	# 请求封装
├─backup_sqls  
│  └─xxx.sql		# 数据库备份文件
├─config
│  └─config.yaml	# 配置文件
├─data
│  └─test_data.xlsx	# 用例文件
├─log
│  └─run...x.log	# 日志文件
├─report
│  ├─data
│  └─html			# allure报告
├─test
│  ├─conftest.py	# 依赖对象初始化
│  └─test_api.py	# 测试文件
├─tools		# 工具包
│  ├─__init__.py		# 常用方法封装
│  ├─data_clearing.py	# 数据隔离
│  ├─data_process.py	# 依赖数据处理
│  ├─db.py				# 数据库连接对象
│  ├─hooks.py			# 自定义扩展方法(可用于用例)文件 
│  ├─read_file.py		# 用例、配置项读取
│  ├─recording.py		# 接口录制,写入用例文件
│  └─send_email.py		# 邮件发送、报告压缩
├─项目实战接口文档.md	   # 配套项目相关接口文档
├─requirements.txt		 # 项目依赖库文件
└─run.py	# 主启动文件
```

## 接口服务
服务提供者：https://space.bilibili.com/283273603?spm_id_from=333.788.b_636f6d6d656e74.6

## Jenkins集成

https://www.cnblogs.com/zy7y/p/13448102.html

## 视频
version1.0 版本-B站：https://www.bilibili.com/video/BV1pv411i7zK/
master版本-B站: https://www.bilibili.com/video/BV1rr4y1r754


