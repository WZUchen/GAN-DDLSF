import datetime
import os
import shutil
from ase.io import read, write
from tqdm import tqdm


def convert_and_organize_cif_files(source_folder_path, target_folder_path):
    # 确保源文件夹存在
    if not os.path.exists(source_folder_path):
        print(f"Folder '{source_folder_path}' does not exist.")
        return

    # 创建目标文件夹
    if not os.path.exists(target_folder_path):
        os.makedirs(target_folder_path)

    # 获取文件夹中的所有cif文件
    cif_files = [f for f in os.listdir(source_folder_path) if f.endswith('.cif')]

    # 使用tqdm创建进度条
    for file in tqdm(cif_files, desc="Converting Files"):
        source_file_path = os.path.join(source_folder_path, file)
        file_name_without_extension = os.path.splitext(file)[0]

        # 在目标文件夹中为每个cif文件创建一个子文件夹
        new_folder_path = os.path.join(target_folder_path, file_name_without_extension)
        os.makedirs(new_folder_path, exist_ok=True)

        try:
            # 读取cif文件
            structure = read(source_file_path)

            # 创建POSCAR文件路径
            poscar_file_path = os.path.join(new_folder_path, 'POSCAR')

            # 转换为POSCAR格式并保存
            write(poscar_file_path, structure, format='vasp')

            # 移动原cif文件到子文件夹
            shutil.move(source_file_path, new_folder_path)
        except Exception as e:
            print(f"Error processing {file}: {e}")


if __name__ == '__main__':

    # 获取当前日期，格式为YYYYMMDD
    current_date = datetime.datetime.now().strftime("%Y%m%d")

    # 源文件夹路径
    # source_folder_path = "../data/postprocess_data/GaN_Crystals_Generate/20240103_generate_GaN_cif"
    source_folder_path = "../data/postprocess_data/AlAs_Crystals_Generate/20240515_generator_AlAs-500-2"

    # 目标文件夹路径
    target_folder_path = f'../data/postprocess_data/{current_date}_generator_AlAs_POSCAR'

    convert_and_organize_cif_files(source_folder_path, target_folder_path)
