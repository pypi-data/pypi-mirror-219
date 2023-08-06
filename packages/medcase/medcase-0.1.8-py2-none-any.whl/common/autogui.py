import os
import json
import random
import re
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from urllib.parse import urlparse
import requests
import time
import hashlib
import json
import textwrap
import ast
from tkcalendar import DateEntry
def case_data_process(business='腾讯健康',start_date='',end_date='',api_id='775edbdf-69b4-4632-8b20-a9988d28ce04'):
    appid = 'urftian'
    token = "1053813a-224e-417a-b46f-b3ca2ae84a7f"
    user = 'urftian'
    timestamp = str(int(time.time()))
    signature = timestamp + token + timestamp
    hash_object = hashlib.sha256(signature.encode('utf-8'))
    signature = hash_object.hexdigest()
    headers = {
        "AppID":appid,
        "Signature":signature,
        "Timestamp":timestamp,
        "X-User":user
    }
    print(business, api_id)
    url = 'http://30.162.219.142/api/v1/medapimanager/interface/api_data_draft?business={}&api_id={}'.format(business,api_id)
    res = requests.get(url=url,headers=headers).json()["data"]

    print(res)
    return res

def generate_test_code_v10(log, chosen_indices=None, template=None):
    case_list = []


    entries = log["log"]["entries"] if log != None else data

    if chosen_indices is not None:
        entries = [entries[i] for i in chosen_indices]
    if entries == []:
        entries = data
    print(entries)

    for index, entry in enumerate(entries):
        testcase_code = ''
        if template == "腾讯健康":
            testcase_func = testcase_template_tencent_health
        elif template == "医典":
            testcase_func = testcase_template_tencent_yidian
        else:
            testcase_func = testcase_template_tencent_health

        testcase_code += testcase_func(index, entry)
        testcase_code += "\n\n"
        case_list.append(testcase_code)

    return case_list


def save_test_code_to_file(log_data, output_dir, chosen_indices=None):
    case_list = generate_test_code_v10(log_data, chosen_indices,template=template_var.get())  # 根据选择的数据数据生成测试用例代码
    folder_name = datetime.now().strftime("%Y%m%d_%H%M")  # 按当前日期时间创建文件夹
    folder_path = os.path.join(output_dir, folder_name)  # 输出文件夹的完整路径
    os.makedirs(folder_path, exist_ok=True)  # 如果不存在，则创建输出文件夹
    for test_code in case_list:
        num = str(random.randint(1,99))
        file_name = f"{api_name}.py"  # 输出的文件名
        file_path = os.path.join(folder_path, file_name)  # 输出文件的完整路径
        if os.path.exists(file_path):
            print('文件路径存在，将新建同名其他文件')
            file_name = f"{api_name}{num}.py"  # 输出的文件名
            file_path = os.path.join(folder_path, file_name)  # 输出文件的完整路径




        with open(file_path, "w") as f:  # 打开文件并写入测试用例代码
            print(test_code)
            f.write(test_code)
        print(f"测试用例代码已保存到: {file_path}")  # 输出文件保存成功的提示



def testcase_template_tencent_health(index, entry):
    global api_name
    api_name = entry['path'].split('/')[-1]
    class_name = entry['path'].split('/')[-2]
    testcase_code = f"from QTALibs.test_base.testcase_v2 import MedTestCaseV2\n\n\nclass {api_name}(MedTestCaseV2):\n"
    testcase_code += f"    owner = '自动生成'\n    tags = 'pre', 'pro', {class_name} \n    priority = MedTestCaseV2.EnumPriority.Normal\n    status = MedTestCaseV2.EnumStatus.Ready\n\n"
    if log_file_path_var.get():
        generated_test_code = f"""
        def test_case_{index + 1}(self):
            path = '{urlparse(entry['request']['url']).path}'
            res = self.request_th(path=path, method='{entry['request']['method']}', params={dict(entry['request']['queryString']) if entry['request']['queryString'] else {} }, payload={json.loads(entry['request']['postData']['text']) if 'postData' in entry['request'] else {} }, simple_assert=False)
            self.assertEqual(res.status_code, {entry['response']['statusCode']})
        """
    elif data_source_var.get():
        generated_test_code = f"""
    def run_test(self):
        path = '{entry['path']}'
        method = '{entry['method']}'
        payload = {json.loads(entry['req_body'])}
        expected_code = {json.loads(entry['rsp_body'])['code']}
        expected_msg = "{json.loads(entry['rsp_body'])['msg']}"
        res = self.request_th(path=path, method=method, data=payload)
        self.assert_equal('响应code', res['code'], expected_code)
        self.assert_equal('响应msg', res['msg'], expected_msg)
            """
    generated_test_code = testcase_code + generated_test_code
    return generated_test_code.strip()

def testcase_template_tencent_yidian(index, entry):
    if log_file_path_var.get():
        generated_test_code = f"""
        def test_case_{index + 1}(self):
            path = '{urlparse(entry['request']['url']).path}'
            res = self.request_th(path=path, method='{entry['request']['method']}', params={dict(entry['request']['queryString']) if entry['request']['queryString'] else {} }, payload={json.loads(entry['request']['postData']['text']) if 'postData' in entry['request'] else {} }, simple_assert=False)
            self.assertEqual(res.status_code, {entry['response']['statusCode']})
        """
    elif data_source_var.get():
        generated_test_code = f"""
            def test_case_{index + 1}(self):
                path = '{entry['path']}'
                method = '{entry['method']}'
                payload = {json.loads(entry['req_body'])}
                expected_code = {json.loads(entry['rsp_body'])['code']}
                expected_msg = "{json.loads(entry['rsp_body'])['msg']}"
                res = self.request_th(path=path, method=method, data=payload)
                self.assert_equal('响应code', res['code'], expected_code)
                self.assert_equal('响应msg', res['msg'], expected_msg)
            """

    return generated_test_code.strip()

def on_template_change(event):
    template = template_var.get()
    if template == "腾讯健康":
        testcase_func = testcase_template_tencent_health
    elif template == "医典":
        testcase_func = testcase_template_tencent_yidian
    else:
        return

    data_source = data_source_var.get()
    if log_file_path_var.get():
        index = [index for index, var in enumerate(checkbox_vars) if var.get()][0]
        entry = log_data["log"]["entries"][index]
        generated_test_code = testcase_func(index, entry )
    elif data_source == "接口":
        index = [index for index, var in enumerate(checkbox_vars) if var.get()][0]
        entry = data[index]
        generated_test_code = testcase_func(index, entry)
    elif data_source == "数据库":
        index = [index for index, var in enumerate(checkbox_vars) if var.get()][0]
        entry = log_data["log"]["entries"][index]
        generated_test_code = testcase_func(index, entry)
    else:
        return

    generated_code_text.delete('1.0', tk.END)
    generated_code_text.insert(tk.END, generated_test_code)


def browse_log_file():
    log_file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.har")])
    log_file_path_var.set(log_file_path)

    # 读取日志文件
    with open(log_file_path_var.get(), "r") as f:
        global log_data
        log_data = json.load(f)

    create_checkboxes()



# Update the create_checkboxes function
def create_checkboxes_api():
    # 删除已存在的复选框和标签
    for checkbox, label in zip(checkboxes, test_case_labels):
        checkbox.destroy()
        label.destroy()

    checkboxes.clear()
    test_case_labels.clear()
    checkbox_vars.clear()

    for index, entry in enumerate(data):
        checkbox_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(checkbox_frame, variable=checkbox_var)
        checkbox.grid(row=index // 3, column=index % 3, sticky=tk.W)
        checkbox_vars.append(checkbox_var)
        case_name = entry['path'].split('/')[-1]

        # Add the test case label next to the checkbox
        test_case_label = tk.Label(checkbox_frame, text=f"{case_name}")
        test_case_label.grid(row=index // 3, column=index % 3, sticky=tk.W, padx=(20, 0))
        test_case_label.bind("<Button-1>", lambda event, idx=index: on_checkbox_click_api(event, idx))
        test_case_labels.append(test_case_label)  # Add the label to the list


def create_checkboxes():
    for index, entry in enumerate(log_data["log"]["entries"][1:20]):
        checkbox_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(checkbox_frame, variable=checkbox_var)
        checkbox.grid(row=index // 3, column=index % 3, sticky=tk.W)
        checkbox_vars.append(checkbox_var)

        # Add the test case label next to the checkbox
        test_case_label = tk.Label(checkbox_frame, text=f"Test Case {index + 1}")
        test_case_label.grid(row=index // 3, column=index % 3, sticky=tk.W, padx=(20, 0))
        test_case_label.bind("<Button-1>", lambda event, idx=index: on_checkbox_click(event, idx))
        test_case_labels.append(test_case_label)  # Add the label to the list



def on_checkbox_click_api(event, index):
    checkbox_vars[index].set(not checkbox_vars[index].get())

    # Update the background color of the selected checkbox
    for idx, label in enumerate(test_case_labels):
        if idx == index:
            label.config(bg="yellow" if checkbox_vars[index].get() else "SystemButtonFace")

    entry = data[index]
    details = f"URL: {entry['path']}\nMethod: {entry['method']}\n\n"

    req_body = json.dumps(json.loads(entry['req_body']))
    req_body = textwrap.indent(req_body.strip(), ' ' * 8)
    req_body = json.dumps(json.loads(req_body), indent=4)
    req_body = ast.literal_eval(f'"""{req_body}"""')
    details += f"Payload:\n{req_body}\n\n"

    details_text.delete('1.0', tk.END)
    details_text.insert(tk.END, details)

    generated_test_code = testcase_template_tencent_health(index, entry)
    generated_code_text.delete('1.0', tk.END)
    generated_code_text.insert(tk.END, generated_test_code.strip())



def on_checkbox_click(event, index):
    checkbox_vars[index].set(not checkbox_vars[index].get())

    # Update the background color of the selected checkbox
    for idx, label in enumerate(test_case_labels):
        if idx == index:
            label.config(bg="yellow" if checkbox_vars[index].get() else "SystemButtonFace")

    entry = log_data["log"]["entries"][index]
    details = f"URL: {entry['request']['url']}\nMethod: {entry['request']['method']}\n\n"

    if "postData" in entry['request']:
        details += f"Payload:\n{entry['request']['postData']['text']}\n\n"

    details += "Query Parameters:\n"
    for param in entry['request']["queryString"]:
        details += f"{param['name']} = {param['value']}\n"

    details_text.delete('1.0', tk.END)
    details_text.insert(tk.END, details)

    generated_test_code = f"""
    def test_case_{index + 1}(self):
        path = '{urlparse(entry['request']['url']).path}'
        res = self.request_th(path=path, method='{entry['request']['method']}', params={dict(entry['request']['queryString']) if entry['request']['queryString'] else {} }, payload={json.loads(entry['request']['postData']['text']) if 'postData' in entry['request'] else {} }, simple_assert=False)
        self.assertEqual(res.status_code, {entry['response']['statusCode']})
    """
    generated_code_text.delete('1.0', tk.END)
    generated_code_text.insert(tk.END, generated_test_code.strip())


def save_chosen_test_cases_to_file():
    chosen_indices = [index for index, var in enumerate(checkbox_vars) if var.get()]
    save_test_code_to_file(log_data, output_dir=output_dir_var.get(), chosen_indices=chosen_indices)


# def send_message_to_wechat_robot():
#     webhook_url = webhook_url_var.get().strip()
#     if not webhook_url:
#         return
#
#     message = "以下测试用例已生成：\n\n"
#     chosen_indices = [index for index, var in enumerate(checkbox_vars) if var.get()]
#     for index in chosen_indices:
#         message += f"Test Case {index + 1}: {log_data['log']['entries'][index]['request']['url']}\n"
#
#     data_source = data_source_var.get()
#     if data_source:
#         message += f"\n数据来源：{data_source}\n数据：\n{data_text.get('1.0', tk.END)}"
#
#     payload = {
#         "msgtype": "text",
#         "text": {
#             "content": message
#         }
#     }
#
#     response = requests.post(webhook_url, json=payload)
#     if response.status_code == 200:
#         print("企业微信机器人消息已发送")
#     else:
#         print("企业微信机器人消息发送失败")

def get_data_from_api():
    #从接口拉取数据
    business = business_var.get()
    start_date = start_date_var.get()
    end_date = end_date_var.get()
    api_id = api_id_var.get()
    if not api_id:
        api_id = '775edbdf-69b4-4632-8b20-a9988d28ce04'
    api_data = case_data_process(business=business,start_date=start_date,end_date=end_date,api_id=api_id)
    return api_data

def get_data_from_database():
    # Implement your logic to get data from database here
    return "Database data"

def on_data_source_change(event):
    global data
    data_source = data_source_var.get()
    if data_source == "接口":
        data = get_data_from_api()
        business_frame.pack(fill=tk.X, padx=5, pady=5)
        date_range_frame.pack(fill=tk.X, padx=5, pady=5)
        api_id_frame.pack(fill=tk.X, padx=5, pady=5)
        log_file_frame.pack_forget()
    elif data_source == "数据库":
        data = get_data_from_database()
        log_file_frame.pack_forget()
        business_frame.pack_forget()
        date_range_frame.pack_forget()
        api_id_frame.pack_forget()
    elif data_source == "Log文件":
        if log_file_path_var.get():
            with open(log_file_path_var.get(), "r") as f:
                global log_data
                log_data = json.load(f)
            data = log_data["log"]["entries"]
        else:
            data = ""
        log_file_frame.pack(fill=tk.X, padx=5, pady=5)
    else:
        data = ""
        log_file_frame.pack_forget()

    create_checkboxes_api()

    data_text.delete('1.0', tk.END)
    data_text.insert(tk.END, data)


def on_entry_change(*args):
    global data
    if business_var.get() and start_date_var.get() and end_date_var.get() or api_id_var.get():
        data = get_data_from_api()
        create_checkboxes_api()




#帮助文档
def open_help_content():
    help_window = tk.Toplevel(root)
    help_window.title("帮助内容")
    help_window.geometry("400x300")

    help_content = tk.Text(help_window, wrap=tk.WORD)
    help_content.pack(fill=tk.BOTH, padx=5, pady=5)

    help_content_text = """在这里添加您的帮助内容。"""
    help_content.insert(tk.END, help_content_text)



# 创建主窗口
root = tk.Tk()
log_data = None
data = None
root.title("用例生成小工具")
#创建按钮样式

style = ttk.Style()
style.configure("Blue.TButton", background="blue", foreground="white")
#帮助文档
help_button = tk.Button(root, text="帮助文档", command=open_help_content, bg="yellow", fg="yellow", highlightbackground="yellow", highlightcolor="yellow")
help_button.pack(side=tk.RIGHT, anchor=tk.N, padx=5, pady=5)

# 数据来源下拉框相关组件
data_source_frame = tk.Frame(root)
data_source_frame.pack(fill=tk.X, padx=5, pady=5)

data_source_label = tk.Label(data_source_frame, text="数据来源:")
data_source_label.pack(side=tk.LEFT)

data_source_var = tk.StringVar()
data_source_combobox = ttk.Combobox(data_source_frame, textvariable=data_source_var, state="readonly")
data_source_combobox["values"] = ["接口", "数据库", "Log文件"]
data_source_combobox.pack(side=tk.LEFT, padx=(5, 0))
data_source_combobox.bind("<<ComboboxSelected>>", on_data_source_change)


#接口筛选项
business_frame = tk.Frame(root)
business_frame.pack(fill=tk.X, padx=5, pady=5)

business_label = tk.Label(business_frame, text="业务:")
business_label.pack(side=tk.LEFT)

business_var = tk.StringVar()
business_combobox = ttk.Combobox(business_frame, textvariable=business_var, state="readonly")
business_combobox["values"] = ["腾讯健康", "医典", "慧用药"]
business_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

date_range_frame = tk.Frame(root)
date_range_frame.pack(fill=tk.X, padx=5, pady=5)


date_range_label = tk.Label(date_range_frame, text="时间范围:")
date_range_label.pack(side=tk.LEFT)

start_date_var = tk.StringVar()
start_date_entry = DateEntry(date_range_frame, textvariable=start_date_var, date_pattern='yyyy-mm-dd')
start_date_entry.pack(side=tk.LEFT, padx=(0, 5))

end_date_var = tk.StringVar()
end_date_entry = DateEntry(date_range_frame, textvariable=end_date_var, date_pattern='yyyy-mm-dd')
end_date_entry.pack(side=tk.LEFT)

api_id_frame = tk.Frame(root)
api_id_frame.pack(fill=tk.X, padx=5, pady=5)

api_id_label = tk.Label(api_id_frame, text="API ID:")
api_id_label.pack(side=tk.LEFT)

api_id_var = tk.StringVar()
api_id_entry = tk.Entry(api_id_frame, textvariable=api_id_var)
api_id_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

business_var.trace("w", on_entry_change)
start_date_var.trace("w", on_entry_change)
end_date_var.trace("w", on_entry_change)
api_id_var.trace("w", on_entry_change)

# Log 文件路径输入相关组件
log_file_frame = tk.Frame(root)
# log_file_frame.pack(fill=tk.X, padx=5, pady=5)

log_file_path_var = tk.StringVar()
log_file_label = tk.Label(log_file_frame, text="Log file:")
log_file_label.pack(side=tk.LEFT)

log_file_entry = tk.Entry(log_file_frame, textvariable=log_file_path_var)
log_file_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

log_file_button = tk.Button(log_file_frame, text="Browse...", command=browse_log_file)
log_file_button.pack(side=tk.LEFT, padx=(5, 0))

# 用例选择相关组件
checkbox_frame = tk.Frame(root)
checkbox_frame.pack(fill=tk.BOTH, padx=5, pady=0, expand=True)
checkboxes = []
checkbox_vars = []
test_case_labels = []


# 显示用例详细信息的文本框
details_frame = tk.Frame(root)
details_frame.pack(fill=tk.BOTH, padx=0, pady=0, expand=True)

details_text = tk.Text(details_frame, wrap=tk.WORD)
details_text.pack(fill=tk.BOTH, expand=True)
# 显示生成的测试代码的文本框
generated_code_frame = tk.Frame(root)
generated_code_frame.pack(fill=tk.BOTH, padx=0, pady=0, expand=True)

generated_code_text = tk.Text(generated_code_frame, wrap=tk.WORD)
generated_code_text.pack(fill=tk.BOTH, expand=True)

# 用例模板下拉框相关组件
template_frame = tk.Frame(root)
template_frame.pack(fill=tk.X, padx=5, pady=5)

template_label = tk.Label(template_frame, text="用例模板:")
template_label.pack(side=tk.LEFT)

template_var = tk.StringVar()
template_combobox = ttk.Combobox(template_frame, textvariable=template_var, state="readonly")
template_combobox["values"] = ["腾讯健康", "医典"]
template_combobox.pack(side=tk.LEFT, padx=(5, 0))
template_combobox.bind("<<ComboboxSelected>>", on_template_change)
# 输出目录相关组件
output_dir_frame = tk.Frame(root)
output_dir_frame.pack(fill=tk.X, padx=5, pady=5)

output_dir_var = tk.StringVar()
output_dir_var.set("testcases")
output_dir_label = tk.Label(output_dir_frame, text="用例输出目录")
output_dir_label.pack(side=tk.LEFT)

output_dir_entry = tk.Entry(output_dir_frame, textvariable=output_dir_var)
output_dir_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

# # 企业微信机器人webhook相关组件
# webhook_frame = tk.Frame(root)
# webhook_frame.pack(fill=tk.X, padx=5, pady=5)
#
# webhook_label = tk.Label(webhook_frame, text="企业微信机器人Webhook:")
# webhook_label.pack(side=tk.LEFT)

# webhook_url_var = tk.StringVar()
# webhook_entry = tk.Entry(webhook_frame, textvariable=webhook_url_var)
# webhook_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

# 创建测试用例按钮
create_button = tk.Button(root, text="创建保存测试用例", command=save_chosen_test_cases_to_file)
create_button.pack(padx=5, pady=5)

# # 发送消息到企业微信机器人按钮
# send_message_button = tk.Button(root, text="发送消息到企业微信机器人", command=send_message_to_wechat_robot)
# send_message_button.pack(padx=5, pady=5)

root.mainloop()


