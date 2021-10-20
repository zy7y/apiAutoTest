# 简介
通过FastAPI的Path参数来实现接口Mock服务,暂时不知道更好的方法，知晓更好的方法后会同步更新的
# 技术栈
FastAPI + tortoise-orm + sqlite3
# 使用
## 本地部署
```shell
1. git clone https://gitee.com/zy7y/FastAPIMockServe.git
2. python -m venv venv  
3. venv\Scripts\activate
4. pip install -r requirements.txt
5. python main.py
```
*浏览器访问: http://127.0.0.1/8000/docs*
# 待完成
- [ ] 前端页面:  
  ```shell
  1. 暂时用Swagger页面进行管理添加Mock接口
  2. 无法查看到Mock出来的接口,只可直接访问.
  ```
- [ ] 其他

# 更新日志
- [x] 2021-07-26 依靠Path参数来实现接口Mock服务
