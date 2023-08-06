import subprocess
from medcase import autogui
def main():
    # 使用 subprocess.Popen 运行命令并实时捕获输出
    process = subprocess.Popen(['python3', 'medcase/autogui.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True)

    # 循环读取输出并实时显示
    for line in process.stdout:
        print(line.strip())

    # 等待进程完成
    process.wait()


if __name__ == '__main__':
    main()