import os
import subprocess
from tqdm import tqdm

def run_command_in_folder(folder_path, command):
    """在指定文件夹内执行命令，并返回输出结果"""
    current_dir = os.getcwd()
    os.chdir(folder_path)
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        result = e.output
    os.chdir(current_dir)
    return result.decode('utf-8')

def main():
    base_folder = "../GaN"
    output_file = "./GaN_Crystal_Energy_Log_Ratios/output_results_GaN_V2.txt"

    # 获取所有子文件夹
    subfolders = [os.path.join(base_folder, f) for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]

    # 创建或清空输出文件
    with open(output_file, 'w') as file:
        file.write("")

    # 遍历子文件夹并执行命令
    for folder in tqdm(subfolders, desc="Processing folders"):
        result = run_command_in_folder(folder, "qvasp -e")
        with open(output_file, 'a') as file:
            file.write(f"Folder: {folder}\n")
            file.write(f"Result:\n{result}\n")
            file.write("--------------------------------------------------\n")

if __name__ == "__main__":
    main()

