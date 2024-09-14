import os
import pandas as pd
from ase.io import read
from ase.spacegroup import get_spacegroup

def get_spacegroup_from_poscar(poscar_file):
    """
    从POSCAR文件中获取空间群信息。
    """
    try:
        atoms = read(poscar_file)
        spacegroup = get_spacegroup(atoms).symbol
        return spacegroup
    except Exception as e:
        print(f"Error reading file {poscar_file}: {e}")
        return None

def update_csv_with_spacegroup_info(csv_file, folder_path):
    """
    更新CSV文件，添加空间群信息。
    """
    df = pd.read_csv(csv_file)
    df['Spacegroup'] = None

    for i, row in df.iterrows():
        file_name = row['File Name']
        poscar_path = os.path.join(folder_path, file_name, 'POSCAR')
        if os.path.exists(poscar_path):
            spacegroup = get_spacegroup_from_poscar(poscar_path)
            df.at[i, 'Spacegroup'] = spacegroup

    df.to_csv(csv_file, index=False)

def main():
    csv_file = 'extracted_data.csv'  # CSV文件路径
    folder_path = './poscar/set'     # 文件夹路径

    update_csv_with_spacegroup_info(csv_file, folder_path)

if __name__ == "__main__":
    main()
