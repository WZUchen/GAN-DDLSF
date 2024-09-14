import os
import subprocess
import time
from tqdm import tqdm

def execute_command_in_subfolders(root_folder, command, log_file_name):
    """
    在指定根文件夹的每个子文件夹中执行命令，并记录执行情况。

    参数:
    root_folder (str): 根文件夹路径。
    command (str): 要执行的命令。
    log_file_name (str): 记录已执行子文件夹的日志文件名称。
    """
    completed_folders = set()
    original_dir = os.getcwd()  # 保存原始工作目录
    log_file = os.path.join(original_dir, log_file_name)  # 完整的日志文件路径

    # 读取已完成的文件夹
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            completed_folders = set(file.read().splitlines())

    count = 0
    for folder in tqdm(os.listdir(root_folder), desc="执行命令中"):
        folder_path = os.path.join(root_folder, folder)
        if os.path.isdir(folder_path) and folder not in completed_folders:
            # 切换到子文件夹
            os.chdir(folder_path)
            try:
                # 执行命令
                subprocess.run(command, shell=True, check=True)
                print(f"命令在 {folder_path} 成功执行")
                # 记录完成的文件夹
                with open(log_file, "a") as file:
                    file.write(folder + "\n")
                count += 1
            except subprocess.CalledProcessError as e:
                print(f"命令在 {folder_path} 执行失败: {e}")
            finally:
                # 返回原始工作目录
                os.chdir(original_dir)

            # 每执行80次，sleep 80s
            if count % 100 == 0:
                print("暂停 70 秒...")
                time.sleep(80)

if __name__ == "__main__":
    root_folder = '../GaN'
    command = 'sbatch submit.sh'
    log_file_name = './Calculation_Log/execution_log_GaN.txt'
    execute_command_in_subfolders(root_folder, command, log_file_name)

