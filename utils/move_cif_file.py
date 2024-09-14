import os
import shutil
import pandas as pd

## TODO 还没优化好

# 路径设置
source_folder = 'D:\\Craystal_Generator_System\\data\\preprocess_data\\filtered_compound_Database'
csv_file_path = 'D:\\Craystal_Generator_System\\final_output_with_formation_energy.csv'
destination_folder = 'D:\\Craystal_Generator_System\\unmatched_cif_files'

# 创建目标文件夹（如果尚不存在）
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# 读取CSV文件
df = pd.read_csv(csv_file_path)
subfolder_names = set(df['Subfolder Name'])

# 获取源文件夹中所有的.cif文件
cif_files = [f for f in os.listdir(source_folder) if f.endswith('.cif')]

# 移动未匹配的.cif文件
for file in cif_files:
    if file not in subfolder_names:
        source_file = os.path.join(source_folder, file)
        destination_file = os.path.join(destination_folder, file)
        shutil.move(source_file, destination_file)

print("移动完成。")
