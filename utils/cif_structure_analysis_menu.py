import glob
from ase.io import read, write
from tqdm import tqdm
import os


def find_max_element_counts_in_cifs(cif_path, elements):
    """
    在指定路径的CIF文件中查找给定元素的最大计数。

    Args:
        cif_path (str): CIF文件所在的路径。
        elements (list): 要搜索的元素列表。

    Returns:
        dict: 包含元素和其最大计数及相应文件路径的字典。
    """
    cif_list = glob.glob(cif_path + '/*.cif')
    max_counts = {element: {'count': 0, 'file': ''} for element in elements}

    for file_path in tqdm(cif_list):
        try:
            atoms = read(file_path)
            symbols = atoms.get_chemical_symbols()

            for element in elements:
                element_count = symbols.count(element)
                if element_count > max_counts[element]['count']:
                    max_counts[element] = {'count': element_count, 'file': file_path}
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")

    return max_counts


def find_max_cell_length_in_cifs(cif_path):
    """
    遍历指定路径下的所有.cif文件，计算并输出最大晶胞长度以及相应文件的名称和位置。

    Args:
        cif_path (str): 存放.cif文件的目录路径。
    """
    cif_files = glob.glob(cif_path + '/*.cif')
    max_cell_length_info = {'file': '', 'max_cell_length': 0}

    for file_path in tqdm(cif_files):
        try:
            atoms = read(file_path)
            lengths = atoms.get_cell_lengths_and_angles()[:3]
            max_length = max(lengths)

            if max_length > max_cell_length_info['max_cell_length']:
                max_cell_length_info['max_cell_length'] = max_length
                max_cell_length_info['file'] = file_path

        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")

    print("最大晶胞长度的文件:", max_cell_length_info['file'])
    print("最大晶胞长度:", max_cell_length_info['max_cell_length'])


def filter_and_save_cif_files(source_path, target_path, max_length=10,max_atoms=20):
    """
    筛选出晶格长度小于10且原子个数小于等于20的.cif文件，并将它们保存到新的文件夹中。

    Args:
        source_path (str): 存放原始.cif文件的目录路径。
        target_path (str): 保存筛选后文件的目标目录路径。
        max_length (float): 筛选的最大晶格长度，默认为10。
        max_length (float): 筛选的最大原子数量，默认为20。
    Returns:
        int: 符合筛选条件的.cif文件的总数。
    """
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    cif_files = glob.glob(source_path + '/*.cif')
    filtered_count = 0

    for file_path in tqdm(cif_files, desc="筛选晶格长度小于等于10且原子个数小于等于20的CIF文件"):
        try:
            atoms = read(file_path)
            lengths = atoms.get_cell_lengths_and_angles()[:3]
            num_atoms = len(atoms)
            if max(lengths) <= max_length and num_atoms <= max_atoms:
                write(os.path.join(target_path, os.path.basename(file_path)), atoms)
                filtered_count += 1
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")

    return filtered_count


if __name__ == '__main__':
    cif_path = '../zc/preprocess_data/filtered_compound_Database/'

    while True:
        print("\n请选择要执行的操作：")
        print("1. 查找最大元素计数")
        print("2. 计算最大晶胞长度")
        print("3. 筛选晶格长度小于10，原子数小于20的CIF文件")
        print("4. 退出")
        choice = input("请输入选项（1-4）：")

        if choice == '1':
            elements = ['Ga', 'N']
            max_counts = find_max_element_counts_in_cifs(cif_path, elements)
            for element in elements:
                print(f"最大的 {element} 值: {max_counts[element]['count']}")
                print(f"包含最大 {element} 值的文件: {max_counts[element]['file']}")
        elif choice == '2':
            find_max_cell_length_in_cifs(cif_path)
        elif choice == '3':
            target_path = '../zc/preprocess_data/filtered_compound_Database_cell_under10_atoms_under20/'
            filtered_count = filter_and_save_cif_files(cif_path, target_path)
            print(f"晶格长度小于等于10的CIF文件共有 {filtered_count} 个。")
        elif choice == '4':
            break
        else:
            print("无效的选项，请重新输入。")
