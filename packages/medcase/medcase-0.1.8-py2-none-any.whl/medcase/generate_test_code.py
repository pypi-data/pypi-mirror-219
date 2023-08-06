# -*- coding: utf-8 -*-
# @Author  : jackxclei
# @Time    : 2023/6/26 7:25 下午
# @Function:
import json
import re
from datetime import datetime
import os


def generate_test_code(log, bussiness, type):
    if bussiness == 1:  # 健康
        return generate_test_code_1(log, type)
    if bussiness == 2:  # 腾讯医典
        return generate_test_code_2(log,type)
    if bussiness == 3:  # 慧用药
        return generate_test_code_3(log, type)


def generate_test_code_1(log, type):
    # 腾讯健康用例模版
    case_content = []  # 用例集
    if type == 1:
        entries = log["log"]["entries"]
        for index, entry in enumerate(entries, start=1):
            request = entry["request"]
            method = request["method"]
            url = request["url"]
            class_name = url.split('/')[-2]
            case_name = url.split('/')[-2] + url.split('/')[-1]
            testcase_code = f"from QTALibs.test_base.testcase_v2 import MedTestCaseV2\n\n\nclass {case_name}(MedTestCaseV2):\n"
            testcase_code += f'''    "{url.split('/')[-1]}"\n'''
            testcase_code += "    owner = 'YourName'\n    tags = 'tag1', 'tag2'\n    priority = MedTestCaseV2.EnumPriority.Normal\n    status = MedTestCaseV2.EnumStatus.Ready\n\n"
            api_path = re.sub(r'^https?://[^/]+/', '', url, flags=re.IGNORECASE)
            params = {item["name"]: item["value"] for item in request["queryString"]}
            payload = request["postData"]["text"] if "postData" in request else ""
            response = entry["response"]
            status_code = response["statusCode"]
            testcase_code += f"    def run_test(self):  # 定义测试用例\n"
            testcase_code += f"        path = '/{api_path}'  # 请求接口的路径\n"
            if payload != "":
                testcase_code += f"        payload = {json.dumps(json.loads(payload), indent=4)}  # 请求的内容\n"
            testcase_code += f"        res = self.request_th(path=path, {'params=' + str(params) if params else 'data=payload' if payload else ''}, simple_assert=False)  # 发送请求\n"
            testcase_code += f"        self.assertEqual(res.status_code, {status_code})  # 断言响应状态码\n\n"
            case_content.append({"file_name": class_name, "content": testcase_code})
        return case_content



def generate_test_code_2(log, type):
    # 医典用例模版
    case_content = []  # 用例集
    if type == 1:
        entries = log["log"]["entries"]
        for index, entry in enumerate(entries, start=1):
            request = entry["request"]
            method = request["method"]
            url = request["url"]
            class_name = url.split('/')[-2]
            case_name = url.split('/')[-2] + url.split('/')[-1]
            testcase_code = f"# coding:utf-8\nimport uuid\nimport pytest\n\n\n"
            testcase_code += f'''    "{url.split('/')[-1]}"\n'''
            testcase_code += "    owner = 'YourName'\n    tags = 'tag1', 'tag2'\n    priority = MedTestCaseV2.EnumPriority.Normal\n    status = MedTestCaseV2.EnumStatus.Ready\n\n"
            api_path = re.sub(r'^https?://[^/]+/', '', url, flags=re.IGNORECASE)
            params = {item["name"]: item["value"] for item in request["queryString"]}
            payload = request["postData"]["text"] if "postData" in request else ""
            response = entry["response"]
            testcase_code += f'''
            class {case_name}:
                @pytest.mark.{class_name}
                def test_{case_name}(self, browser, get_yml_data, get_common_headers, get_common_body, offset):
                    """{case_name}"""
                    url = get_yml_data["h5_host"] + "{api_path}"
                    headers = get_common_headers
                    body = get_common_body
                    body["body"]["cmd"] = "{url.split('/')[-1]}"
                    body["body"]["traceid"] = str(uuid.uuid4())
                    body["body"]["payload"] = {
            payload
            }
                    rsp = browser.request("POST", url=url, headers=headers, json=body)
                    browser.result = rsp
                    assert rsp.json()["body"]["retcode"] == 0
                    assert rsp.json()["body"]["bizcode"] == 0
                    assert rsp.json()["body"]["message"] == "success"
                    assert rsp.json()["body"]["payload"]["code"] == 0
                    assert rsp.json()["body"]["payload"]["message"] == "success"'''
            case_content.append({"file_name": class_name, "content": testcase_code})
        return testcase_code
    elif type == 2:
        for sig_data in log:
            print('------')
            api_path = sig_data['path']
            case_name = sig_data['path'].split('/')[-1]
            payload = sig_data['req_body']
            file_name = sig_data['path'].split('/')[-2]
            testcase_code = f'''
# coding:utf-8
import uuid
import pytest

class {case_name}:
    @pytest.mark.{file_name}
    def test_{case_name}(self, browser, get_yml_data, get_common_headers, get_common_body, offset):
        """{case_name}"""
        url = get_yml_data["h5_host"] + "{api_path}"
        headers = get_common_headers
        body = get_common_body
        body["body"]["cmd"] = "{case_name}"
        body["body"]["traceid"] = str(uuid.uuid4())
        body["body"]["payload"] = {
payload
}
        rsp = browser.request("POST", url=url, headers=headers, json=body)
        browser.result = rsp
        assert rsp.json()["body"]["retcode"] == 0
        assert rsp.json()["body"]["bizcode"] == 0
        assert rsp.json()["body"]["message"] == "success"
        assert rsp.json()["body"]["payload"]["code"] == 0
        assert rsp.json()["body"]["payload"]["message"] == "success"'''
            case_content.append({"file_name": file_name, "content": testcase_code})
        return case_content


def generate_test_code_3(log, type):
    # 慧用药用例模版
    case_content = []  # 用例集
    param = f'''{{"timestamp": str(round(time.time() * 1000))}}'''
    if type == 1:
        entries = log["log"]["entries"]
        for index, entry in enumerate(entries, start=1):
            request = entry["request"]
            method = request["method"]
            url = request["url"]
            class_name = url.split('/')[-2]
            case_name = url.split('/')[-2] + url.split('/')[-1]
            api_path = re.sub(r'^https?://[^/]+/', '', url, flags=re.IGNORECASE)
            params = {item["name"]: item["value"] for item in request["queryString"]}
            payload = json.loads(request["postData"]["text"])["request"] if "postData" in request else ""
            testcase_code = f'''
# -*- coding: utf-8 -*-
import os
import sys
import time
from hyyserverautolib.TestBase import Base, HOST
from hyyserverautolib.Utils.assertUtil import AssertUtils'''
            testcase_code += f'''
class {url.split('/')[-1]}(Base):
    "auto create"
    owner = "auto create"
    timeout = 0.5
    priority = Base.EnumPriority.Normal
    status = Base.EnumStatus.Ready

    def run_test(self):
        rsp = self.{url.split('/')[-1]}()
        AssertUtils.assertCommon(self, rsp)
        self.pact_assert_by_one(self.tags, self.__class__.__name__)

    def {url.split('/')[-1]}(self):
        """
        auto create
        """
        cmd = sys._getframe().f_code.co_name
        path = os.path.abspath(os.path.dirname(__file__))
        service = os.path.basename(path)
        url = HOST + service + '/' + cmd
        param = {param}
        body = Base.set_body(self, request={payload})
        return self.api_request('post', url, param, body, cmd, self.tags)'''
            case_content.append({"file_name": class_name, "content": testcase_code})
        return case_content
    elif type == 2:
        for sig_data in log:
            print('------')
            print(sig_data['req_body'])
            case_name = sig_data['path'].split('/')[-1]
            payload = json.loads(sig_data['req_body'])['request']
            file_name = sig_data['path'].split('/')[-2]
            testcase_code = f'''
# -*- coding: utf-8 -*-
import os
import sys
import time
from hyyserverautolib.TestBase import Base, HOST
from hyyserverautolib.Utils.assertUtil import AssertUtils'''
            testcase_code += f'''
class {case_name}(Base):
   "auto create"
   owner = "auto create"
   timeout = 0.5
   priority = Base.EnumPriority.Normal
   status = Base.EnumStatus.Ready

   def run_test(self):
       rsp = self.{case_name}()
       AssertUtils.assertCommon(self, rsp)
       self.pact_assert_by_one(self.tags, self.__class__.__name__)

   def {case_name}(self):
       """
       auto create
       """
       cmd = sys._getframe().f_code.co_name
       path = os.path.abspath(os.path.dirname(__file__))
       service = os.path.basename(path)
       url = HOST + service + '/' + cmd
       param = {param}
       body = Base.set_body(self, request={payload})
       return self.api_request('post', url, param, body, cmd, self.tags)'''
            case_content.append({"file_name": file_name, "content": testcase_code})
        return case_content


def save_test_code_to_file(log_data, output_dir, business, type):
    bus_re = {
        1: "health",
        2: "yidian",
        3: "hyy"
    }
    case_content = generate_test_code(log_data, business, type)  # 根据日志数据生成测试用例代码
    print(case_content)
    for case_sig in case_content:
        class_name = case_sig["file_name"]  # 测试类名
        test_code = case_sig["content"]
        print(test_code)
        folder_name = datetime.now().strftime("%Y%m%d_%H%M")  # 按当前日期时间创建文件夹
        folder_path = os.path.join(output_dir, bus_re[business], folder_name)  # 输出文件夹的完整路径
        os.makedirs(folder_path, exist_ok=True)  # 如果不存在，则创建输出文件夹

        file_name = f"{class_name}.py"  # 输出的文件名
        file_path = os.path.join(folder_path, file_name)  # 输出文件的完整路径
        if os.path.exists(file_path):
            print('文件路径存在，将追加内容')
            test_code = re.sub(r'(?:^|\n)(?:import|from|# -*-).*', '', test_code)
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(test_code)
        else:
            with open(file_path, "w") as f:  # 打开文件并写入测试用例代码
                f.write(test_code)
        print(f"测试用例代码已保存到: {file_path}")  # 输出文件保存成功的提示

# # 读取日志文件并转换为字典类型的数据
# with open("http_request_log_complex.json", "r") as f:
#     log_data = json.load(f)

# save_test_code_to_file(log_data, output_dir='testcases')
