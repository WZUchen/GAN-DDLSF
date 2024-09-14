import os
import shutil
from tqdm import tqdm

def split_folders(source_folder, target_root, max_per_folder=1000):
    """
    将一个包含许多子文件夹的目录拆分为多个目录。

    参数:
    source_folder (str): 源文件夹路径，其中包含需要拆分的子文件夹。
    target_root (str): 目标根目录，新的文件夹将在这里创建。
    max_per_folder (int): 每个新文件夹中包含的最大子文件夹数量。
    """
    subfolders = [f for f in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, f))]
    total_folders = len(subfolders)
    current_folder_count = 0
    current_target_folder = os.path.join(target_root, f'set_1')

    for i, folder in enumerate(tqdm(subfolders, desc="处理中"), start=1):
        # 创建新的目标文件夹
        if current_folder_count == 0 or current_folder_count >= max_per_folder:
            current_folder_count = 0
            set_number = (i // max_per_folder) + 1
            current_target_folder = os.path.join(target_root, f'set_{set_number}')
            os.makedirs(current_target_folder, exist_ok=True)

        # 移动子文件夹到目标文件夹
        shutil.move(os.path.join(source_folder, folder), os.path.join(current_target_folder, folder))
        current_folder_count += 1

if __name__ == "__main__":
    source_folder = '../data/preprocess_data/prepare_calculation_Database'  # 源文件夹路径
    target_root = '../data/preprocess_data/prepare_calculation_Database_split_10'  # 目标根目录路径
    split_folders(source_folder, target_root)
