import os
from tqdm import tqdm

def delete_files_except_contcar(folder_path):
    # 遍历指定文件夹中的所有子文件夹
    for root, dirs, files in os.walk(folder_path):
        for _,file in enumerate(tqdm(files)):
            # 检查文件是否不是'CONTCAR'
            if file != 'POSCAR':
                file_path = os.path.join(root, file)
                # 删除文件
                os.remove(file_path)
                print(f"已删除：{file_path}")

# 指定文件夹路径
folder_path = '../zc/postprocess_data/20240330_generator_AlAs_POSCAR'

# 调用函数
delete_files_except_contcar(folder_path)

