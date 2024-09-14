import os
import pandas as pd
from tqdm import tqdm
import shutil

def load_non_converged_filenames(csv_file):
    """
    从CSV文件加载未收敛的文件名。
    """
    df = pd.read_csv(csv_file)
    return df[df['Convergence'] == 'NO']['File Name'].tolist()

def delete_non_converged_folders(folder_path, non_converged_filenames):
    """
    删除未收敛的文件夹。
    """
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    total = len(subfolders)
    progress = tqdm(total=total, desc="Processing folders")

    for subfolder in subfolders:
        progress.update(1)
        if subfolder in non_converged_filenames:
            shutil.rmtree(os.path.join(folder_path, subfolder), ignore_errors=True)

    progress.close()

def main():
    csv_file = 'extracted_data.csv'  # CSV文件路径
    folder_path = './poscar/set'  # 文件夹路径

    non_converged_filenames = load_non_converged_filenames(csv_file)
    delete_non_converged_folders(folder_path, non_converged_filenames)

if __name__ == "__main__":
    main()
