import glob
import numpy as np
from ase import Atoms
from ase.io import read
from tqdm import tqdm

cell_max = 12.78

def make_condition(n, n_class):
    temp = np.zeros((n_class, 1))
    temp[n - 1, 0] = 1
    return temp


def read_poscar(poscar_path, isatoms=False, atoms=None):
    if not isatoms:
        atoms = read(poscar_path)
    else:
        atoms = atoms

    cell = atoms.get_cell()
    temp = atoms.cell.cellpar()
    symbols = atoms.get_chemical_symbols()
    pos = atoms.get_scaled_positions()

    return atoms, cell, symbols, pos, temp[:3], temp[3:]


def go_to_10_cell(scaled_pos, n_ga, n_n):
    cell = np.array([[10, 0, 0], [0, 10, 0], [0, 0, 10]]).astype(float)
    atoms = Atoms('Ga' + str(n_ga) + 'N' + str(n_n))  # 修改为 'Ga' 和 'N'
    atoms.set_cell(cell)
    atoms.set_scaled_positions(scaled_pos)
    pos = atoms.get_positions()
    return pos


def make_onehot(n, n_class, e_pos):
    temp = np.zeros((n_class, 3))
    for i, p in enumerate(e_pos):
        temp[i, :] = p
    return temp


def go_to_15_cell(pos_10, n_ga, n_n):
    cell = np.array([[15, 0, 0], [0, 15, 0], [0, 0, 15]]).astype(float)
    pos = pos_10 + np.array([2.5, 2.5, 2.5])
    atoms = Atoms('Ga' + str(n_ga) + 'N' + str(n_n))  # 修改为 'Ga' 和 'N'
    atoms.set_cell(cell)
    atoms.set_positions(pos)
    scaled_pos = atoms.get_scaled_positions()
    return scaled_pos


def do_feature(atoms):
    atoms, cell, symbols, pos, lengths, angles = read_poscar(poscar_path=None, isatoms=True, atoms=atoms)

    l = lengths / cell_max
    l = l.reshape(1, 3)
    a = angles / 180
    a = a.reshape(1, 3)
    cell = np.vstack((l, a))
    # print(cell)

    n_ga = symbols.count('Ga')  # 修改为计数 'Ga'
    n_n = symbols.count('N')  # 修改为计数 'N'
    comp = str(n_ga) + '_' + str(n_n)

    pos_10 = go_to_10_cell(pos, n_ga, n_n)  # 使用 n_ga 和 n_n 替换 n_bi 和 n_se
    scaled_pos_15 = go_to_15_cell(pos_10, n_ga, n_n)  # 同上

    ga_pos = scaled_pos_15[:n_ga, :]  # 修改为 'Ga' 的位置
    n_pos = scaled_pos_15[n_ga:n_ga + n_n, :]  # 修改为 'N' 的位置
    ga_pos_onehot = make_onehot(n_ga, 20, ga_pos)  # 修改为 'Ga' 的 one-hot 编码
    n_pos_onehot = make_onehot(n_n, 20, n_pos)  # 修改为 'N' 的 one-hot 编码
    pos_onehot = np.vstack((ga_pos_onehot, n_pos_onehot))

    temp = np.vstack((cell, pos_onehot))
    inp = temp.reshape(-1, 3)

    return inp


if __name__ == '__main__':
    # 测试
    # poscar_path = '../data/postprocess_data/calculated_database/unit_poscar_set/mp-1830-NpTe-GaN.vasp'
    # atoms = read(poscar_path)
    # atoms, cell, symbols, pos, lengths, angles = read_poscar(poscar_path=None, isatoms=True, atoms=atoms)
    # # 打印返回的参数
    # print("Atoms:", atoms)
    # print("Cell:", cell)
    # print("Symbols:", symbols)
    # print("Positions:", pos)
    # print("Lengths:", lengths)
    # print("Angles:", angles)

    vasp_path = '../data/preprocess_data/calculated_database/unit_poscar_set'
    vasp_list = glob.glob(vasp_path + '/*.vasp')

    results = []

    for _, i in enumerate(tqdm(vasp_list)):
        atoms = read(i)
        s = atoms.get_chemical_symbols()
        image = do_feature(atoms)
        results.append(image)
    results = np.array(results)
    np.save('unique_GaN_v1', results)
