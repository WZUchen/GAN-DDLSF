import os
import shutil
from tqdm import tqdm

def copy_calculation_files(source_folder, target_folder):
    """复制INCAR, POTCAR和jobfile到每个子文件夹"""
    subfolders = [f for f in os.listdir(target_folder) if os.path.isdir(os.path.join(target_folder, f))]
    for subfolder in tqdm(subfolders, desc="复制计算文件"):
        subfolder_path = os.path.join(target_folder, subfolder)
        for file in ['INCAR', 'POTCAR', 'submit.sh']:
             shutil.copy(os.path.join(source_folder, file), subfolder_path)
        #for file in [ 'submit.sh']:
        #    shutil.copy(os.path.join(source_folder, file), subfolder_path)
# 主逻辑
def main():
    source_folder = '../GaN/'
    temp_folder = '../temp/'

    copy_calculation_files(temp_folder, source_folder)

    print("处理完成。")

if __name__ == "__main__":
    main()

