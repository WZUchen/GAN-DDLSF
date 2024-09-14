import os
from ase.io import read, write
from tqdm import tqdm
import datetime


def convert_cif_to_poscar(source_dir, target_dir):
    # 获取所有 .cif 文件
    cif_files = [f for f in os.listdir(source_dir) if f.endswith(".cif")]

    # 使用 tqdm 显示进度条
    for file in tqdm(cif_files, desc="Converting CIF to POSCAR"):
        file_path = os.path.join(source_dir, file)
        # 读取 CIF 文件
        structure = read(file_path)
        # 获取化学式
        formula = structure.get_chemical_formula()
        # 创建目标目录
        formula_dir = os.path.join(target_dir, formula)
        if not os.path.exists(formula_dir):
            os.makedirs(formula_dir)
        # 将结构保存为 POSCAR
        poscar_path = os.path.join(formula_dir, file.replace('.cif', '.POSCAR'))
        write(poscar_path, structure, format='vasp')


# 使用示例
if __name__ == '__main__':
    source_dir = "../data/postprocess_data/GaN_Crystals_Generate/20240123_generator_GaN_cif-z_pca_0.3"

    # 获取当前日期，格式为YYYYMMDD
    current_date = datetime.datetime.now().strftime("%Y%m%d")

    # 定义原始路径并插入日期
    target_dir = f'../data/postprocess_data/GaN_Crystals_Generate/{current_date}_generator_GaN_POSCAR'

    convert_cif_to_poscar(source_dir, target_dir)
