import numpy as np
def check(image):
    criterion = 0.4
    pos = image[2:, :]
    ga = pos[:20, :]  # 假设前20行代表Ga原子的位置
    n = pos[20:, :]  # 假设剩下的行代表N原子的位置

    ga_sum = np.sum(ga, axis=1)
    ga_label = np.zeros((20, 1)) +1  # 确保ga_label的大小与ga_sum相同
    ga_label[ga_sum < criterion] = 0

    n_sum = np.sum(n, axis=1)
    n_label = np.zeros((20, 1)) +1  # 确保n_label的大小与n_sum相同
    n_label[n_sum < criterion] = 0

    label = np.vstack((ga_label, n_label))
    return label

