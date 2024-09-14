import re
import csv
import os


def extract_folder_name(full_path):
    # 仅提取路径中的 'set_1' 部分
    parts = full_path.split('/')
    # 假设 'set_1' 总是位于路径的第二段
    folder_name = parts[1] if len(parts) > 1 else 'N/A'
    return folder_name


def parse_text_file(file_path):
    global folder_name, file_name, energy
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        if line.startswith('Folder:'):
            full_folder_name = line.split('Folder:')[1].strip()
            folder_name = extract_folder_name(full_folder_name)
            file_name = full_folder_name.split('/')[-1]
            continue

        if line.startswith('The Final Energy in This Folder is:'):
            energy = re.findall(r"-?\d+\.\d+", line)
            energy = energy[0] if energy else 'N/A'
            continue

        if line.startswith('Get COVERAGED:'):
            convergence = 'YES' if 'YES' in line else 'NO'
            data.append([folder_name, file_name, convergence, energy])

    return data


def write_to_csv(csv_file_path, data, mode='w'):
    header = ['Set Folder', 'File Name', 'Convergence', 'Energy']
    with open(csv_file_path, mode, newline='') as csvfile:
        writer = csv.writer(csvfile)
        if mode == 'w':  # 添加表头
            writer.writerow(header)
        for row in data:
            writer.writerow(row)


def process_and_write(file_path, csv_file_path):
    # 处理文本文件并写入CSV
    data = parse_text_file(file_path)
    mode = 'a' if os.path.exists(csv_file_path) else 'w'  # 检查文件是否存在以确定是追加还是创建新文件
    write_to_csv(csv_file_path, data, mode)

if __name__ == '__main__':
    csv_file_path = 'extracted_data_Ga2N2.csv'
    file_path = './output_results_Ga2N2_V1.txt'
    process_and_write(file_path, csv_file_path)