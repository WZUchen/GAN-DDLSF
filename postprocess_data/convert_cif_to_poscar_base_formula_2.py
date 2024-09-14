import os
from tqdm import tqdm


def organize_poscar_files(base_dir):
    # 遍历 base_dir 下的所有子目录
    for subdir in os.listdir(base_dir):
        subdir_path = os.path.join(base_dir, subdir)
        if os.path.isdir(subdir_path):
            # 遍历子目录中的所有文件
            for file in tqdm(os.listdir(subdir_path), desc=f"Processing {subdir}"):
                if file.endswith(".POSCAR"):
                    # 创建新目录名基于文件名前缀，但在当前子目录内
                    prefix = file.split('.')[0]
                    new_dir_path = os.path.join(subdir_path, prefix)
                    if not os.path.exists(new_dir_path):
                        os.makedirs(new_dir_path)

                    # 重命名和移动文件
                    old_file_path = os.path.join(subdir_path, file)
                    new_file_path = os.path.join(new_dir_path, "POSCAR")
                    os.rename(old_file_path, new_file_path)


# 使用示例
if __name__ == '__main__':
    base_dir = '../data/postprocess_data/GaN_Crystals_Generate/20240127_generator_GaN_POSCAR'
    organize_poscar_files(base_dir)
