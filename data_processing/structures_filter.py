from tqdm import tqdm
import os
import shutil


def create_folder_if_not_exists(folder):
    """如果文件夹不存在，则创建文件夹"""
    if not os.path.exists(folder):
        os.makedirs(folder)


def filter_cif_files(files, filter_condition):
    """过滤CIF文件列表，基于给定条件"""
    return [f for f in files if f.endswith('.cif') and filter_condition(f)]


def copy_file(source, destination):
    """复制文件"""
    shutil.copy(source, destination)


def main(source_folder, target_folder, filter_condition):
    """主函数处理文件筛选和复制"""
    create_folder_if_not_exists(target_folder)

    cif_files = os.listdir(source_folder)
    filtered_files = filter_cif_files(cif_files, filter_condition)

    for cif_file in tqdm(filtered_files, desc="Processing files"):
        source_path = os.path.join(source_folder, cif_file)
        target_path = os.path.join(target_folder, cif_file)
        copy_file(source_path, target_path)

    print(f"筛选后的CIF文件已保存到{target_folder}。")


if __name__ == "__main__":
    source_folder = '../zc/preprocess_data/reordered_compound_Database/'
    target_folder = '../zc/preprocess_data/filtered_compound_Database/'

    def filter_condition(filename):
        """
        根据文件名过滤出符合特定化学式条件的文件。

        :param filename: 需要进行过滤的文件名字符串
        :return: 如果文件名包含特定的化学式，则返回True，否则返回False

        """
        # 假设文件名中化学式位于最后一个'-'符号之前
        # 根据'-'符号对文件名进行分割，得到各个部分
        parts = filename.split('-')
        print(parts)
        # 检查分割后的部分是否足够包含一个化学式
        if len(parts) > 1:
            # 提取文件扩展名之前的化学式部分
            chemical_formula = parts[-1]
            print(chemical_formula)
            # 检查化学式是否为我们期望的几个化学式之一
            return chemical_formula in ['AlAs2.cif','AlAs.cif','Al3As.cif']
        return False


    main(source_folder, target_folder, filter_condition)
