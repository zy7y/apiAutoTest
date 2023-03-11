
> <font size="3" color="red">这是一个待测试的分支、使用Golang打包的可执行程序作为实际请求客户端，可获得在请求各阶段耗时的信息, 目前仅有Mac/Linux可执行程序</font>

[![](https://gitee.com/zy7y/apiAutoTest/badge/star.svg)](https://gitee.com/zy7y/apiAutoTest)
[![](https://gitee.com/zy7y/apiAutoTest/badge/fork.svg)](https://gitee.com/zy7y/apiAutoTest)
[![](https://img.shields.io/github/license/zy7y/apiAutoTest)](https://gitee.com/zy7y/apiAutoTest/blob/master/LICENSE)
[![](https://img.shields.io/github/stars/zy7y/apiAutoTest)](https://github.com/zy7y/apiAutoTest)
[![](https://img.shields.io/github/forks/zy7y/apiAutoTest)](https://github.com/zy7y/apiAutoTest)
[![](https://img.shields.io/github/repo-size/zy7y/apiAutoTest?style=social)](https://github.com/zy7y/apiAutoTest)


> 使用Python语言 + Python第三方库 + Golang Req 接口请求 实现的接口自动化测试工具，使用该工具 Python版本 >= 3.8

[![IsXMnO.png](https://z3.ax1x.com/2021/11/13/IsXMnO.png)](https://imgtu.com/i/IsXMnO)

## 配套资源(点击即可跳转)
- [x] [项目使用手册](https://zy7y.github.io/apiAutoTest/)
- [x] [B站视频解析](https://www.bilibili.com/video/BV1jt4y1J7Nw)
- [x] [示例项目接口文档](https://gitee.com/zy7y/apiAutoTest/tree/v1.0/%E9%A1%B9%E7%9B%AE%E5%AE%9E%E6%88%98%E6%8E%A5%E5%8F%A3%E6%96%87%E6%A1%A3.md)
- [x] [Jenkins集成示例](https://www.cnblogs.com/zy7y/p/13448102.html)
## 实现功能
- 测试数据隔离: 测试前后进行数据库备份/还原
- 接口间数据依赖: 需要B接口使用A接口响应中的某个字段作为参数
- 自定义扩展方法： 在用例中使用自定义方法(如：获取当前时间戳...)的返回值 
- 接口录制：录制指定包含url的接口,生成用例数据
- 用例跳过：支持表达式、内置函数、调用变量实现条件跳过用例
- 动态多断言： 可（多个）动态提取实际预期结果与指定的预期结果进行比较断言操作
- 对接数据库： 讲数据库的查询结果可直接用于断言操作
- 邮件发送：将allure报告压缩后已附件形式发送

## 所用依赖库
```
allure-pytest==2.9.45		# allure报告
jsonpath==0.82				# json解析库
loguru==0.6.0				# 日志库
pytest==7.0.1				# 参数化
PyYAML==6.0				    # 读取ymal
xlrd==1.2.0					# 读取excel
yagmail==0.11.224			# 发送邮件
PyMySQL==0.10.1				# 连接mysql数据库
paramiko==2.9.2				# SSH2 连接
xlwt==1.3.0                 # 写excel 用例文件
mitmproxy==7.0.4            # 抓包工具
```

## 联系
QQ群：**`930902996`**


