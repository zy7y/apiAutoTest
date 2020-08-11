# 用例书写格式介绍
| 对应case_data.xlsx中的字段 | 描述|
| ------------------------ | ----------------------------------- |
| token操作                | 将选择headers中使用那个字典。 1. 写：在能正常登录的接口中使用，它将会提取响应中token的值，并写入一个token_header字典中 2. 读：在需要token依赖的接口中使用，它将会使用token_header这个字典(里面会存留登录之后的token) 3. 不填写内容，将使用一个no_token_header字典 |
| 请求方式                 | 按道理支持目前所有的请求方式:get/post/put/delete..|
| 入参关键字               | 1. params：可用于get/delete/head/options/请求中 2. data：post/put/patch请求可使用，content-type是from表单类型。 3. json：post/put/patch请求可使用，content-type：application/json。 |
| 文件对象参数             | 指接口中接受文件上传内容的请求参数变量                       |
| 上传文件对象路径填写形式 | 1. 单个文件上传，直接使用地址，实例：/Users/zy7y/Desktop/vue.js 2. 多个文件上传，使用列表形式传递，如：["/Users/zy7y/Desktop/vue.js","/Users/zy7y/Desktop/jenkins.war"] |
| 路径参数提取             | 解决path参数(携带在url中的参数，非查询参数?)依赖问题，提取出来的字符串将与url进行拼接后在发送请求。 最终url请求的则是：Host + 接口地址 + 路径参数提取解析后的地址 1. 接口path参数实例：Excel 中书写形式：/{"用例编号":"jsonpath表达式"}/ 实例：{"case_002":"$.data.id"}/item/{"case_002":"$.meta.status"} 表示从用例case_002编号，执行后的实际响应结果中，使用jsonpath表达式提取到其中的id，用例编号002实际响应结果中提取meta下面的status业务状态码内容， 结果：上面表达式提取的结果大致如下:500/item/201。 |
| 依赖数据                 | 该接口需要上个接口实际响应结果总某个数据，提取出的字典会与请求数据进行合并，实际发送请求的data使用了依赖数据返回的字典和本来的数据 1. Excel中书写形式：{"用例编号":["提取表达式1","jsonpath提取表达式2"]} 2. 实例：{"case_002": ["$.data.id"], "case_001":["$.meta.msg","$.meta.status"]} 3. 实例2的结果：从用例case_002实际响应中提取id从用例case_001中实际响应结果中提取msg，status业务状态嘛,最后返回一个依赖数据字典:{'id': 500, 'msg': '参数错误', 'status': 400} |
| 预期结果                 | 这里的预期结果传入的是一个字典形式                           |

#⚠️：case_data.xlsx文件中sheet页'用例说明文档'中也有