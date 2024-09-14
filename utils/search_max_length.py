import os
from ase.io.vasp import read_vasp
from tqdm import tqdm

if __name__ == '__main__':
    # 定义要搜索的目录
    search_dir = "../data/postprocess_data/calculated_database/unit_poscar_set"

    # 初始化变量来存储最长晶胞长度和相应的文件路径
    max_length = 0
    max_length_file = ""

    # 遍历指定目录下的所有.vasp文件
    for root, dirs, files in os.walk(search_dir):
        for file in tqdm(files, desc="检查文件"):
            if file.endswith(".vasp"):
                file_path = os.path.join(root, file)
                try:
                    # 读取.vasp文件
                    atoms = read_vasp(file_path)
                    # 计算最长晶胞边长
                    lengths = atoms.get_cell_lengths_and_angles()[:3]
                    longest_side = max(lengths)
                    # 检查是否是目前为止找到的最长的
                    if longest_side > max_length:
                        max_length = longest_side
                        max_length_file = file_path
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")

    # 打印具有最长晶胞边长的文件及其路径
    print("最长晶胞边长:", max_length)
    print("对应文件路径:", max_length_file)
