import os
from tqdm import tqdm

def rename_contcar_to_poscar(folder):
    """
    在指定文件夹中将CONTCAR文件重命名为POSCAR。
    """
    contcar_file = os.path.join(folder, 'CONTCAR')
    poscar_file = os.path.join(folder, 'POSCAR')

    try:
        if os.path.isfile(contcar_file):
            os.rename(contcar_file, poscar_file)
            print(f"Renamed CONTCAR to POSCAR in {folder}")
        else:
            print(f"No CONTCAR found in {folder}")
    except Exception as e:
        print(f"Error processing {folder}: {e}")

def main():
    base_folder = "./poscar/set_1"

    # 获取所有子文件夹
    subfolders = [os.path.join(base_folder, f) for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]

    # 使用tqdm显示进度条
    for folder in tqdm(subfolders, desc="Processing folders"):
        rename_contcar_to_poscar(folder)

if __name__ == "__main__":
    main()
