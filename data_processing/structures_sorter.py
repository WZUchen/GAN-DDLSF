import os
from ase.io import read, write
from tqdm import tqdm


def read_structure(filepath):
    """读取结构文件"""
    return read(filepath)


def write_structure(structure, filepath):
    """将结构写入文件"""
    write(filepath, structure, format='cif')


def reorder_structure(structure, first_element, second_element):
    """按指定顺序重排结构中的原子"""
    first_indices = [atom.index for atom in structure if atom.symbol == first_element]
    second_indices = [atom.index for atom in structure if atom.symbol == second_element]
    new_order_indices = first_indices + second_indices
    return structure[new_order_indices]


def process_structures(source_folder, target_folder):
    """处理源文件夹中的所有结构文件"""
    os.makedirs(target_folder, exist_ok=True)
    for cif_file in tqdm([f for f in os.listdir(source_folder) if f.endswith('.cif')], desc="Processing CIF files"):
        full_path_to_file = os.path.join(source_folder, cif_file)
        structure = read_structure(full_path_to_file)
        new_structure = reorder_structure(structure, 'Al', 'As')
        full_path_to_target_file = os.path.join(target_folder, cif_file)
        write_structure(new_structure, full_path_to_target_file)


# 主逻辑
if __name__ == "__main__":
    source_folder = '../zc/preprocess_data/replace_compound_Database/'
    target_folder = '../zc/preprocess_data/reordered_compound_Database/'
    process_structures(source_folder, target_folder)
