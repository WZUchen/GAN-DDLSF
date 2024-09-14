import os
from pymatgen.io.vasp import Poscar
from tqdm import tqdm

def convert_poscar_to_cif(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 获取所有子文件夹
    subfolders = [f.path for f in os.scandir(source_folder) if f.is_dir()]

    # 进度条
    for folder in tqdm(subfolders, desc="Processing"):
        poscar_file = os.path.join(folder, "POSCAR")
        if os.path.exists(poscar_file):
            try:
                # 读取 POSCAR 文件
                structure = Poscar.from_file(poscar_file).structure

                # 创建 CIF 文件名
                cif_filename = os.path.basename(folder) + ".cif"
                cif_filepath = os.path.join(destination_folder, cif_filename)

                # 写入 CIF 文件
                structure.to(fmt="cif", filename=cif_filepath)
            except Exception as e:
                print(f"Error processing {poscar_file}: {e}")
if __name__ == '__main__':

    # 设置源文件夹和目标文件夹
    source_folder = "Ga2N2_V1"
    destination_folder = "Ga2N2_CIFs"

    convert_poscar_to_cif(source_folder, destination_folder)
