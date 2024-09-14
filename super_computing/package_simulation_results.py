import os
import tarfile
from pathlib import Path
from tqdm import tqdm


def pack_all_in_one(source_dir, output_file):
    """
    将指定源目录中的所有子文件夹和文件打包到一个压缩包内。

    参数:
    source_dir (str): 包含需要打包的文件的源目录。
    output_file (str): 存放打包后的压缩包的文件路径。
    """
    with tarfile.open(output_file, "w:gz") as tar:
        # 获取源目录下的所有内容
        items = os.listdir(source_dir)

        # 显示进度条并添加文件到压缩包
        for item in tqdm(items, desc="打包进度"):
            item_path = os.path.join(source_dir, item)
            tar.add(item_path, arcname=os.path.basename(item_path))


if __name__ == "__main__":
    # source_directory = "../data/preprocess_data/prepare_calculation_Database"
    # output_archive = "../data/preprocess_data/preprocess_calculate_GaN.tar.gz"
    source_directory = "../set_1"
    output_archive = "../set_1.tar.gz"

    pack_all_in_one(source_directory, output_archive)

