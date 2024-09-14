import os
import csv
from pymatgen.core import Structure
from pymatgen.analysis.structure_matcher import StructureMatcher
from tqdm import tqdm

def compare_structures(base_folder, compare_folder, output_csv):
    # 创建 StructureMatcher 实例
    matcher = StructureMatcher()

    # 读取基准结构
    base_structures = {}
    for filename in os.listdir(base_folder):
        if filename.endswith(".cif"):
            try:
                structure = Structure.from_file(os.path.join(base_folder, filename))
                base_structures[filename] = structure
            except:
                print(f"Error loading structure from {filename}")

    # 创建和打开 CSV 文件
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Base File', 'Compare File', 'Is Similar'])

        # 对比结构并写入 CSV 文件
        for filename in tqdm(os.listdir(compare_folder), desc="Comparing structures"):
            if filename.endswith(".cif"):
                compare_structure = Structure.from_file(os.path.join(compare_folder, filename))
                for base_filename, base_structure in base_structures.items():
                    is_similar = matcher.fit(base_structure, compare_structure)
                    writer.writerow([base_filename, filename, is_similar])

# 设置文件夹和输出文件名
base_folder = 'temp'
compare_folder = 'Ga2N2_CIFs'
output_csv = 'comparison_results.csv'

compare_structures(base_folder, compare_folder, output_csv)
