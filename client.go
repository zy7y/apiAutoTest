package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"github.com/imroc/req/v3"
	"log"
	"reflect"
	"strings"
)

// string2Map
//
//	@Description: 字符串转map
//	@param str 字符串 {"name":"7y"}
//	@return map[string]string
func string2Map(str string) map[string]string {
	if !json.Valid([]byte(str)) {
		panic("invalid json string")
	}
	var data map[string]string
	err := json.Unmarshal([]byte(str), &data)
	if err != nil {
		panic(err)
	}
	return data
}

// uploadFileCallback
//
//	@Description: 上传文件回调函数输出
//	@param info
func uploadFileCallback(info req.UploadInfo) {
	fmt.Printf("%q uploaded %.2f%%\n", info.FileName, float64(info.UploadedSize)/float64(info.FileSize)*100.0)
}

/*
*
下载文件 回调
*/
func downloadFileCallback(info req.DownloadInfo) {
	if info.Response.Response != nil {
		fmt.Printf("downloaded %.2f%%\n", float64(info.DownloadedSize)/float64(info.Response.ContentLength)*100.0)
	}
}

// request 请求接口
//
//	@Description:
//	@param url 请求地址
//	@param method 请求方法
//	@param header 请求header {"name":"age"}
//	@param data 表单数据 {"name":"age"}
//	@param json body数据 {"name": "age"}
//	@param file 上传文件 {"参数": "文件地址"}
//	@param outPut 下载文件 文件保存地址
func request(url, method, header, data, json, file, outPut string) {
	client := req.C().DevMode()
	reqClient := client.R()

	method = strings.Title(strings.ToLower(method))

	if header != "" {
		jsonHeader := string2Map(header)
		reqClient.SetHeaders(jsonHeader)
	}

	if outPut != "" && method == "Get" {
		reqClient.SetOutputFile(outPut).SetDownloadCallback(downloadFileCallback)
	}

	if file != "" {
		files := string2Map(file)
		reqClient.SetFiles(files).SetUploadCallback(uploadFileCallback)
	}

	if data != "" && json == "" {
		formData := string2Map(header)
		reqClient.SetFormData(formData)
		//reqClient.SetFormDataFromValues() 一个key 设置多个value
	}

	if json != "" && data == "" {
		reqClient.SetBodyJsonString(json)
	}

	// 获取方法 GET or POST等
	httpMethod := reflect.ValueOf(reqClient).MethodByName(method)

	if httpMethod.IsValid() {
		params := []reflect.Value{reflect.ValueOf(url)}
		result := httpMethod.Call(params)
		resp := result[0].Interface().(*req.Response)
		if result[1].Interface() != nil {
			err := result[1].Interface().(error)
			log.Fatal("error", err)
		}
		fmt.Println(resp.TraceInfo())
	} else {
		log.Fatal("请求方式不存在")
	}

}

func main() {
	// 定义参数变量
	var url, method, header, data, jsonData, file, output string
	// 定义命令行参数
	flag.StringVar(&url, "url", "", "请求的 URL")
	flag.StringVar(&method, "method", "GET", "请求的 HTTP 方法")
	flag.StringVar(&header, "header", "", "请求头，格式为 {'name': 'age'}")
	flag.StringVar(&data, "data", "", "表单数据")
	flag.StringVar(&jsonData, "json", "", "POST 请求的 JSON 数据")
	flag.StringVar(&file, "file", "", "POST 请求的文件路径")
	flag.StringVar(&output, "output", "", "GET 请求下载保存的文件路径")
	flag.Parse()
	request(url, method, header, data, jsonData, file, output)
}
