import os
import random
from ase.io import read, write
from tqdm import tqdm
from structures_sorter import process_structures


def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r') as file:
        return file.readlines()


def write_file(file_path, content):
    """写入文件内容"""
    with open(file_path, 'w') as file:
        file.write(content)


def swap_ga_n(content):
    """交换文件内容中的Ga和N"""
    return ''.join([line.replace('Al', 'Temp').replace('As', 'Al').replace('Temp', 'As') for line in content])


def process_cif_file_for_swap(folder_path, cif_file):
    """处理单个CIF文件以交换Ga和N"""
    content = read_file(os.path.join(folder_path, cif_file))
    swapped_content = swap_ga_n(content)
    base_name, extension = os.path.splitext(cif_file)
    new_cif_file_name = f"{base_name}_swapped{extension}"
    write_file(os.path.join(folder_path, new_cif_file_name), swapped_content)


def create_supercell(folder_path, cif_file, scale_factors):
    """使用随机缩放因子创建超晶胞"""
    layer = read(os.path.join(folder_path, cif_file))
    supercell = layer.repeat(scale_factors)
    base_name, extension = os.path.splitext(cif_file)
    new_cif_file_name = f"{base_name}_randomly_scaled{extension}"
    write(os.path.join(folder_path, new_cif_file_name), supercell)


def main(folder_path, potential_scale_factors):
    """主函数处理文件夹中的所有CIF文件"""
    cif_files = [f for f in os.listdir(folder_path) if f.endswith('.cif')]
    for cif_file in tqdm(cif_files, desc="Processing CIF files"):
        process_cif_file_for_swap(folder_path, cif_file)
        scale_factors = random.choice(potential_scale_factors)
    print(f"所有CIF文件已等比例交换，并将新文件添加到{folder_path}。")

    new_cif_files = [f for f in os.listdir(folder_path) if f.endswith('.cif')]
    for cif_file in tqdm(new_cif_files, desc="Processing CIF files"):
        scale_factors = random.choice(potential_scale_factors)
        create_supercell(folder_path, cif_file, scale_factors)
    print(f"所有CIF文件均同以随机扩胞处理，并将新文件添加到{folder_path}。")


if __name__ == "__main__":
    folder_path = '../zc/preprocess_data/filtered_compound_Database/'
    target_folder = '../zc/preprocess_data/filtered_compound_Database/'
    potential_scale_factors = [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    main(folder_path, potential_scale_factors)
    process_structures(folder_path, target_folder)
