import os
import json
import re
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from urllib.parse import urlparse


def generate_test_code_v10(log, chosen_indices=None):
    class_name = "ServerTest"
    testcase_code = f"from QTALibs.test_base.testcase_v2 import MedTestCaseV2\n\n\nclass {class_name}(MedTestCaseV2):\n"
    testcase_code += "    owner = 'YourName'\n    tags = 'tag1', 'tag2'\n    priority = MedTestCaseV2.EnumPriority.Normal\n    status = MedTestCaseV2.EnumStatus.Ready\n\n"

    entries = log["log"]["entries"]

    if chosen_indices is not None:
        entries = [entries[i] for i in chosen_indices]

    for index, entry in enumerate(entries):
        request = entry["request"]
        method = request["method"]
        url = request["url"]
        api_path = re.sub(r'^https?://[^/]+/', '', url, flags=re.IGNORECASE)
        params = {item["name"]: item["value"] for item in request["queryString"]}
        payload = request["postData"]["text"] if "postData" in request else ""

        response = entry["response"]
        status_code = response["statusCode"]

        testcase_code += f"    def test_case_{index + 1}(self):\n"
        testcase_code += f"        path = '/{api_path}'\n"
        if payload != "":
            testcase_code += f"        payload = {json.dumps(json.loads(payload), indent=4)}\n"
        testcase_code += f"        res = self.request_th(path=path, {'params=' + str(params) if params else 'data=payload' if payload else ''}, simple_assert=False)\n"
        testcase_code += f"        self.assertEqual(res.status_code, {status_code})\n\n"
        print(testcase_code)

    return testcase_code


def save_test_code_to_file(log_data, output_dir, chosen_indices=None):
    test_code = generate_test_code_v10(log_data, chosen_indices)  # 根据日志数据生成测试用例代码
    print(test_code)
    class_name = "ServerTest"  # 测试类名

    folder_name = datetime.now().strftime("%Y%m%d_%H%M")  # 按当前日期时间创建文件夹
    folder_path = os.path.join(output_dir, folder_name)  # 输出文件夹的完整路径
    os.makedirs(folder_path, exist_ok=True)  # 如果不存在，则创建输出文件夹

    file_name = f"{class_name}.py"  # 输出的文件名
    file_path = os.path.join(folder_path, file_name)  # 输出文件的完整路径

    with open(file_path, "w") as f:  # 打开文件并写入测试用例代码
        f.write(test_code)

    print(f"测试用例代码已保存到: {file_path}")  # 输出文件保存成功的提示


def browse_log_file():
    log_file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.har")])
    log_file_path_var.set(log_file_path)

    # 读取日志文件
    with open(log_file_path_var.get(), "r") as f:
        global log_data
        log_data = json.load(f)

    create_checkboxes()


def create_checkboxes():
    for index, entry in enumerate(log_data["log"]["entries"]):
        checkbox_var = tk.BooleanVar()
        checkbox = tk.Checkbutton(checkbox_frame, text=f"Test Case {index + 1}", variable=checkbox_var,
                                  command=lambda idx=index: on_checkbox_click(idx))
        checkbox.grid(row=index // 3, column=index % 3, sticky=tk.W)
        checkbox_vars.append(checkbox_var)


def on_checkbox_click(index):
    checkbox_vars[index].set(not checkbox_vars[index].get())

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




# 创建主窗口
root = tk.Tk()
root.title("auto create ")

# Log 文件路径输入相关组件
log_file_frame = tk.Frame(root)
log_file_frame.pack(fill=tk.X, padx=5, pady=5)

log_file_path_var = tk.StringVar()
log_file_label = tk.Label(log_file_frame, text="Log file:")
log_file_label.pack(side=tk.LEFT)

log_file_entry = tk.Entry(log_file_frame, textvariable=log_file_path_var)
log_file_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

log_file_button = tk.Button(log_file_frame, text="Browse...", command=browse_log_file)
log_file_button.pack(side=tk.LEFT, padx=(5, 0))

# 用例选择相关组件
checkbox_frame = tk.Frame(root)
checkbox_frame.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)

checkbox_vars = []
log_data = None

# 显示用例详细信息的文本框
details_frame = tk.Frame(root)
details_frame.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)

details_text = tk.Text(details_frame, wrap=tk.WORD)
details_text.pack(fill=tk.BOTH, expand=True)

# 显示生成的测试代码的文本框
generated_code_frame = tk.Frame(root)
generated_code_frame.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)

generated_code_text = tk.Text(generated_code_frame, wrap=tk.WORD)
generated_code_text.pack(fill=tk.BOTH, expand=True)

# 输出目录相关组件
output_dir_frame = tk.Frame(root)
output_dir_frame.pack(fill=tk.X, padx=5, pady=5)

output_dir_var = tk.StringVar()
output_dir_var.set("testcases")
output_dir_label = tk.Label(output_dir_frame, text="Output directory:")
output_dir_label.pack(side=tk.LEFT)

output_dir_entry = tk.Entry(output_dir_frame, textvariable=output_dir_var)
output_dir_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

# 创建测试用例按钮
create_button = tk.Button(root, text="Create and Save Test Cases", command=save_chosen_test_cases_to_file)
create_button.pack(padx=5, pady=5)

root.mainloop()