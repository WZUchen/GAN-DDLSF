import os
import shutil
from tqdm import tqdm
from ase.io import read, write

def copy_file(src, dst):
    """
    复制文件从源路径到目标路径
    """
    shutil.copy(src, dst)


def convert_to_vasp(src, dst):
    """
    使用ASE库将POSCAR文件转换为.vasp格式
    """
    structure = read(src)
    write(dst, structure, format='vasp')


def process_poscar_files(src_dir, dst_dir):
    """
    遍历指定的源目录，复制并转换找到的POSCAR文件
    """
    for root, _, files in os.walk(src_dir):
        poscar_files = [f for f in files if f == "POSCAR"]
        for file in tqdm(poscar_files, desc="处理POSCAR文件"):
            full_path = os.path.join(root, file)
            dst_file_name = os.path.basename(root) + ".vasp"
            dst_path = os.path.join(dst_dir, dst_file_name)

            try:
                copy_file(full_path, dst_path)
                convert_to_vasp(dst_path, dst_path)
            except Exception as e:
                print(f"处理文件 {full_path} 时出错: {e}")

if __name__ == '__main__':

    # 定义源目录和目标目录
    source_dir = "../data/postprocess_data/calculated_database/set"
    destination_dir = "../data/postprocess_data/calculated_database/unit_poscar_set"  # 修改为你希望复制和转换POSCAR文件的目录

    # 如果目标目录不存在，则创建它
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # 执行处理POSCAR文件的函数
    process_poscar_files(source_dir, destination_dir)
