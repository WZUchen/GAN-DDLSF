import os
import shutil
from tqdm import tqdm

def copy_and_rename_file(src_file, dest_folder, new_name):
    """
    复制文件从源路径到目标文件夹，并将其重命名。
    """
    try:
        dest_file = os.path.join(dest_folder, new_name)
        shutil.copy2(src_file, dest_file)
        return True
    except IOError as e:
        print(f"Error copying {src_file} to {dest_folder}: {e}")
        return False

def process_subfolders(base_folder, destination_folder, file_name, new_name):
    """
    遍历基础文件夹中的所有子文件夹，并复制并重命名指定文件到目标文件夹。
    """
    subfolders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]

    for folder in tqdm(subfolders, desc="Processing subfolders"):
        src_file = os.path.join(base_folder, folder, file_name)
        dest_subfolder = os.path.join(destination_folder, folder)
        os.makedirs(dest_subfolder, exist_ok=True)

        if os.path.exists(src_file):
            copy_and_rename_file(src_file, dest_subfolder, new_name)

def main():
    base_folder = "../Ga2N2"
    destination_folder = "./contcar/Ga2N2"
    original_file_name = "CONTCAR"
    new_file_name = "POSCAR"

    os.makedirs(destination_folder, exist_ok=True)
    process_subfolders(base_folder, destination_folder, original_file_name, new_file_name)

if __name__ == "__main__":
    main()
