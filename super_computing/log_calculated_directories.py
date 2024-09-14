import os
from tqdm import tqdm

def log_large_directories(base_path, log_file_name):
    """
    记录文件数超过4个的子文件夹名称到日志文件中，并返回这些文件夹的数量。

    参数:
    base_path: 需要遍历的基础路径。
    log_file_name: 日志文件的名称。
    """
    count = 0  # 用于计数文件夹的数量

    # 初始化日志文件
    with open(log_file_name, 'w') as log_file:
        # 遍历目录
        for root, dirs, files in tqdm(os.walk(base_path)):
            # 只考虑直接位于 base_path 下的子文件夹
            if os.path.dirname(root) == base_path.rstrip(os.sep):
                # 检查文件夹中的文件数量是否超过4
                if len(files) > 4:
                    # 获取并写入子文件夹名称
                    subdir_name = os.path.basename(root)
                    log_file.write(f"{subdir_name}\n")
                    count += 1  # 增加计数

    return count

# 定义基础路径和日志文件名称
base_path = '../set_9'
log_file_name = 'execution_log_9.txt'

# 运行函数并获取超过4个文件的文件夹数量
folder_count = log_large_directories(base_path, log_file_name)
print(folder_count)



