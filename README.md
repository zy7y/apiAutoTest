

# apiAutoTest[![GitHub license](https://img.shields.io/github/license/zy7y/apiAutoTest)](https://github.com/zy7y/apiAutoTest/blob/master/LICENSE)
> 使用Python为语言工具 + Python第三方库 实现的接口自动化测试工具

# 在线文档
[apiAutoTest在线帮助文档](http://49.232.203.244:21519/)

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
│  └─base_requests.py	# 请求封装
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
## 使用说明

1.  本项目直接使用的requests.Session理论上实现了cookie请求的管理，不用单独提取cookie，支持前后端分离项目，兼容Restful接口规范。
2.  项目中token操作中为写时，请务必保证是能正常获得响应并且返回了token字段
3.  本项目用例书写格式请务必遵循，sheet页用例说明中有一部分
4.  该项目找的是b站上的一个前后端分离应用，域名使用的是b站某视频里提供的，请大家谨慎操作学习
5.  本项目所要投入生产，请自行修改配置文件config.yaml及用例数据case_data.xlsx，
6.  默认注释了用例失败重跑装饰器，需要的时候自行解除注释即可，但这个功能比较耗时间，自取所需吧
7.  本项目从2020年8月提交，陆续迭代，如果各位有什么建议 欢迎提给我，会尽力解决~~

## 接口服务（后端源码来自）
vue 电商项目实战
教学视频：
https://www.bilibili.com/video/BV1EE411B7SU?p=10

服务提供者：https://space.bilibili.com/283273603?spm_id_from=333.788.b_636f6d6d656e74.6

## 测试报告

![本地运行测试后生成报告](https://gitee.com/zy7y/blog_images/raw/master/img/localhost_report.png)
![测试报告用例失败重跑](https://gitee.com/zy7y/blog_images/raw/master/img/用例失败重跑截图.png)

## 更新记录
2020/08/08 增加实际响应存储数据的方法，并在字典可以处理依赖见tools/svae_response.py

2020/08/09 实现多文件上传，接口中Path参数依赖处理

2020/11/18 使用re库解决当请求参数层级结构多出现无法提取的bug，减少冗余代码，优化path路径参数提取，更新用例填写说明文档

2020/11/21 更新用例文档，合并文件对象，文件地址，优化文件上传处理方式

2020/11/21 config.yaml文件中新增request_headers 选项，默认header在此设置，优化test_api.py文件，整合read_file.py

2020/11/22 优化请求断言方法支持用户自定义提取响应自定内容，支持多数据断言，整合请求方法，优化测试启动方法，部分日志移除，修改预期结果处理

2020/12/08 优化断言信息，增加数据库（支持mysql）查询操作， 使用`@pytest.fixture(scope="session")`来托管数据库对象，用例新增sql栏

2020/12/16 使用conftest.py 初始化用例， 增加失败重跑机制, 增加运行文件run，优化test_api.py冗余代码

2021/01/19 添加数据清洗功能(测试开始前进行数据库备份-分别在服务器和本地进行，测试结束后将备份用以恢复数据-将尝试从服务器和本地恢复到服务器数据库中，docker部署的mysql服务已本地调试通过，直接linux部署的mysql并未测试)
> 详细内容见代码注释`tools/data_clearing.py`
> 如不需要使用该功能请做如下处理,如也不使用数据库对象，只需参考 https://gitee.com/zy7y/apiAutoTest/issues/I2BAQL 修改即可
![](https://gitee.com/zy7y/blog_images/raw/master/img/20210119184856.png)


2021/02/27 添加hooks.py文件(可在此处自定义方法,并用于用例当中，注意请务必在定义的方法中使用return),移除上次更新的eval语法糖，增加用例处理前的日志

2021/05/04 用例增加Header栏，可使用自定义方法，以及提取参数如下，所以取消了 `token操作栏`
![](https://gitee.com/zy7y/blog_images/raw/master/img/20210504121842.png)
![](https://gitee.com/zy7y/blog_images/raw/master/img/20210504122609.png)
![](https://gitee.com/zy7y/blog_images/raw/master/img/20210504234703.png)
![](https://gitee.com/zy7y/blog_images/raw/master/img/20210504234820.png)

2021/05/17 解决执行sql时datetime时间无法被序列化问题，调试sql，理论上支持所有sql语句(select,delete,update,select...), select语句只能获取结果集第一条数据

2021/05/19 统一使用`${}`来包裹变量名/方法 替代先前版本的`&&`,`@@`，新增提取参数栏，意为从当前接口响应中提取指定参数

2021/05/19 移除保存响应，增加提取参数栏{参数名: jsonpath} jsonpath为当前用例响应结果中提取并把结果给参数名，其他用中`${参数名}`使用，`${方法名()}`,`${方法名(参数1)}`

2021/05/22 新增接口录制功能，可生成用例文件, 具体操作见[apiAutoTest在线帮助文档](http://49.232.203.244:21519/), [视频演示](https://www.bilibili.com/video/BV1W64y1y7Lw)
## 博客园首发
https://www.cnblogs.com/zy7y/p/13426816.html

## Jenkins集成

https://www.cnblogs.com/zy7y/p/13448102.html
## 视频教程（该视频为2020年8月开源时录制，大致内容是简单讲个文件作用，其代码对应目前的version1.0分支）
B站：https://www.bilibili.com/video/BV1pv411i7zK/
## 交流群

QQ群：851163511（没技术大佬，本站上的个人项目问题都可以在这里咨询）


