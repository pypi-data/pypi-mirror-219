# -*- coding: utf-8 -*-
# @Author  : jackxclei
# @Time    : 2023/6/26 8:30 下午
# @Function:
tencent_health = f"""
from QTALibs.test_base.testcase_v2 import MedTestCaseV2
class ServerTest(MedTestCaseV2):
    owner = 'YourName'
    tags = 'tag1', 'tag2'
    priority = MedTestCaseV2.EnumPriority.Normal
    status = MedTestCaseV2.EnumStatus.Ready

    def run_test_case_1(self):  # 定义测试用例
        path = '/report/action?product=eyao&company=tencent&seq=31&time=1687251807167&event=app.onhide&uin=271199049&current=%2Fpages%2Fmy%2Findex&scene=1089'  # 请求接口的路径
        res = self.request_th(path=path, params={'product': 'eyao', 'company': 'tencent', 'seq': '31', 'time': '1687251807167', 'event': 'app.onhide', 'uin': '271199049', 'current': '%2Fpages%2Fmy%2Findex', 'scene': '1089'}, simple_assert=False)  # 发送请求
        self.assertEqual(res.status_code, 200)  # 断言响应状态码
"""