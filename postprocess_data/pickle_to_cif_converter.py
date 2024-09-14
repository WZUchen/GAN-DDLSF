import os
import numpy as np
from ase import Atoms
from ase.io import read, write
import torch
from tqdm import tqdm
from label_crystal_structure_rows import check
import datetime


cell_max = 10  # 设置最大晶格常数

def back_to_10_cell(scaled_pos, n_ga, n_n):
    cell = np.identity(3) * 15
    atoms = Atoms('Ga' + str(n_ga) + 'P' + str(n_n))
    atoms.set_cell(cell)
    atoms.set_scaled_positions(scaled_pos)
    pos = atoms.get_positions()

    cell = np.identity(3) * cell_max
    pos = pos - np.array([2.5, 2.5, 2.5])
    atoms = Atoms('Al' + str(n_ga) + 'As' + str(n_n))
    atoms.set_cell(cell)
    atoms.set_positions(pos)
    scaled_poss = atoms.get_scaled_positions()
    return scaled_poss


def back_to_real_cell(scaled_pos, real_cell, n_ga, n_n):
    atoms = Atoms('Al' + str(n_ga) + 'As' + str(n_n))
    atoms.set_cell(real_cell)
    atoms.set_scaled_positions(scaled_pos)
    return atoms


def remove_zero_padding(pos):
    criteria = 0.8
    ga_pos = pos[:20, :]
    n_pos = pos[20:, :]

    ga = np.sum(ga_pos, axis=1)
    n = np.sum(n_pos, axis=1)

    ga_index = np.where(ga > criteria)
    n_index = np.where(n > criteria)

    n_ga = len(ga_index[0])
    n_n = len(n_index[0])

    ga_pos = ga_pos[ga_index]
    n_pos = n_pos[n_index]

    if n_ga == 0:
        ga_pos = np.array([0.1667, 0.1667, 0.1667]).reshape(1, 3)
        n_ga = 1
    if n_n == 0:
        n_pos = np.array([0.1667, 0.1667, 0.1667]).reshape(1, 3)
        n_n = 1

    pos = np.vstack((ga_pos, n_pos))

    return pos, n_ga, n_n


def view_atoms(image, view=True):
    x = image
    x = x.reshape(-1, 3)

    l = x[0, :] * cell_max
    a = x[1, :] * 180
    cell = np.hstack((l, a))
    pos = x[2:, :]

    pos, n_ga, n_n = remove_zero_padding(pos)
    scaled_pos = back_to_10_cell(pos, n_ga, n_n)
    atoms = back_to_real_cell(scaled_pos, cell, n_ga, n_n)
    atoms.set_pbc([1, 1, 1])

    if view:
        atoms.edit()

    return atoms, x


def view_atoms_classifier(image, ga_label, n_label, view=False):
    x = image
    ga = x[2:22, :]
    n = x[22:, :]

    l = x[0, :] * 10
    a = x[1, :] * 180
    # print(f"Lengths: {l}, Angles: {a}")

    c = np.hstack((l, a))
    # print(c)
    atoms = Atoms('H')
    try:
        atoms.set_cell(c)
    except AssertionError:
        print("Assertion Error: Check cell parameters.")
        print("Lengths:", l)
        print("Angles:", a)
        return None, x  # Return None to indicate the error condition
    cell = atoms.get_cell()
    t = np.isnan(cell)
    tt = np.sum(t)
    isnan = False
    if not tt == 0:
        isnan = True
        print(cell)
        print(l)
        print(a)

    ga_index = (ga_label == 1).nonzero(as_tuple=False).squeeze()
    n_index = (n_label == 1).nonzero(as_tuple=False).squeeze()

    ga_pos = ga[ga_index]
    n_pos = n[n_index]

    n_ga = 1 if len(ga_pos.shape) == 1 else ga_pos.shape[0]
    n_n = 1 if len(n_pos.shape) == 1 else n_pos.shape[0]

    if n_ga == 0:
        ga_pos = np.array([0.1667, 0.1667, 0.1667]).reshape(1, 3)
        n_ga = 1
    if n_n == 0:
        n_pos = np.array([0.1667, 0.1667, 0.1667]).reshape(1, 3)
        n_n = 1

    pos = np.vstack((ga_pos, n_pos))

    symbols = ['Al'] * n_ga + ['As'] * n_n
    scaled_pos = back_to_10_cell(pos, n_ga, n_n)
    atoms = back_to_real_cell(scaled_pos, cell, n_ga, n_n)
    atoms.set_pbc([1, 1, 1])
    if view:
        atoms.edit()

    return atoms, x

# def process_sample(image, label):
#     """
#     处理单个样本，生成Atoms对象和标签。
#
#     参数:
#         image (np.ndarray): 图像数据。
#         label (np.ndarray): 对应的标签。
#
#     返回:
#         tuple: 包含Atoms对象和修改后的图像数据。
#     """
#     bi_label = label[:20, :].squeeze(dim=1)
#     se_label = label[20:, :].squeeze(dim=1)
#     return view_atoms_classifier(image, bi_label, se_label, view=False)
#
# def save_cif_files(output, folder_path):
#     """
#     将Atoms对象保存为CIF文件。
#
#     参数:
#         output (list): 包含Atoms对象的列表。
#         folder_path (str): CIF文件保存的文件夹路径。
#     """
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)
#
#     for idx, sample in enumerate(output):
#         atoms, _ = process_sample(*sample)
#         file_name = os.path.join(folder_path, f'test_{idx + 1}.cif')
#         write(file_name, atoms)

if __name__ == '__main__':
    a = np.load('../data/keypoints/gen_image_cwgan_AlAs/20240513/gen_images_500.npy')
    m = a.shape[0]
    output = []
    for i in tqdm(range(m)):
        x = a[i].squeeze(axis=0)
        label = check(x)
        new_input = (x, label)
        output.append(new_input)


    # 获取当前日期，格式为YYYYMMDD
    current_date = datetime.datetime.now().strftime("%Y%m%d")

    # 定义原始路径并插入日期
    folder_path = f'../data/postprocess_data/AlAs_Crystals_Generate/{current_date}_generator_AlAs-500-2'

    print(folder_path)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for idx, sample in tqdm(enumerate(output), desc="Processing samples"):
        image, label = sample

        try:
            # 将 NumPy 数组转换为 PyTorch 张量
            image_tensor = torch.from_numpy(image).float()
            label_tensor = torch.from_numpy(label).float()

            # 分离标签并去除单一维度
            ga_label = label_tensor[:20, :].squeeze(dim=1)
            n_label = label_tensor[20:, :].squeeze(dim=1)

            # 处理函数
            atoms, _ = view_atoms_classifier(image_tensor, ga_label, n_label, view=False)
            # 生成cif文件
            cif_file_name = os.path.join(folder_path, f'test_{idx + 1}.cif')
            write(cif_file_name, atoms)

        except Exception as e:
            print(f"Error processing sample {idx}: {e}")
            continue  # 跳过当前样本，继续处理下一个




