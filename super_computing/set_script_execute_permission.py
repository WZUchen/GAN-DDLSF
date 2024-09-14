import os
from tqdm import tqdm

def set_execute_permission(file_path):
    """
    为指定文件设置执行权限。
    :param file_path: 文件的完整路径。
    """
    os.chmod(file_path, 0o755)

def find_files(directory, file_name):
    """
    遍历给定目录及其子目录，寻找特定名称的文件。
    :param directory: 要遍历的目录。
    :param file_name: 要查找的文件名。
    :return: 一个包含所有找到的文件路径的列表。
    """
    found_files = []
    for root, dirs, files in os.walk(directory):
        if file_name in files:
            found_files.append(os.path.join(root, file_name))
    return found_files

def main():
    target_directory = "../Ga2N2"
    target_file = "submit.sh"

    # 查找目标文件
    files_to_process = find_files(target_directory, target_file)

    # 处理文件并显示进度
    with tqdm(total=len(files_to_process), desc="正在处理", unit="file") as pbar:
        for file_path in files_to_process:
            set_execute_permission(file_path)
            pbar.update(1)

if __name__ == "__main__":
    main()


