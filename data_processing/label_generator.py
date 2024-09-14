import numpy as np
from tqdm import tqdm
import pickle


def generate_labels_for_atoms(image, threshold=0.4):
    """
    根据图像中原子的位置为镓（Ga）和氮（N）原子生成标签。

    参数:
        image (np.ndarray): 包含原子位置的图像数组。
        threshold (float): 确定原子活性/非活性的阈值。

    返回:
        np.ndarray: 镓（Ga）和氮（N）原子的生成标签数组。
    """
    pos = image[2:, :]
    ga, n = pos[:20, :], pos[20:, :]

    # 根据阈值计算镓（Ga）原子的标签
    ga_label = np.where(np.sum(ga, axis=1) < threshold, 0, 1).reshape(-1, 1)
    # 根据阈值计算氮（N）原子的标签
    n_label = np.where(np.sum(n, axis=1) < threshold, 0, 1).reshape(-1, 1)

    return np.vstack((ga_label, n_label))


def process_images_from_file(file_path, output_path):
    """
    从.npy文件处理晶体结构，生成标签，然后保存到pickle文件中。

    参数:
        file_path (str): 包含晶体结构的.npy文件的路径。
        output_path (str): 输出pickle文件将被保存的路径。
    """
    images = np.load(file_path)
    output = []

    for image in tqdm(images, desc="处理晶体结构"):
        label = generate_labels_for_atoms(image)
        output.append((image, label))

    # 将处理结果保存为pickle文件
    with open(output_path, 'wb') as f:
        pickle.dump(output, f)


if __name__ == '__main__':
    npy_file_path = '../data/preprocess_data/Training_Data/Unlabeled/unique_GaN_v1.npy'  # 替换为实际的.npy文件路径
    pickle_output_path = '../data/preprocess_data/Training_Data/Labeled/GaN_data_v1.pickle'
    process_images_from_file(npy_file_path, pickle_output_path)
#
# import json
# import os
#
#
# def create_conversation_data(name, repetitions, filepath):
#     """
#     根据给定模板创建不同场景的对话数据并保存到JSON文件。
#     :param name: 名字或机构名称
#     :param repetitions: 每个模板重复的次数
#     :param filepath: 保存JSON数据的文件路径
#     """
#     conversations = []
#
#     # 基本问候与自我介绍
#     template_greeting = {
#         "conversation": [
#             {
#                 "system": "你是一个懂中文的小助手",
#                 "input": "你好",
#                 "output": f"😊你好！我是{name}，一个由陈子安开发的人工智能的语言模型，我可以与你交流、回答问题、创造故事等等。我的目的是帮助人们更好地交流和学习语言。欢迎与我交流！ 💬"
#             }
#         ]
#     }
#
#     template_english_greeting = {
#         "conversation": [
#             {
#                 "system": "You are a Chinese-speaking assistant",
#                 "input": "Who are you",
#                 "output": f"Hello, I am chenzian, your AI assistant. Is there anything I can help you with?"
#             }
#         ]
#     }
#
#     # 询问身份
#     template_identity = {
#         "conversation": [
#             {
#                 "system": "你是一个懂中文的小助手",
#                 "input": "你是谁",
#                 "output": f"您好，我是{name}，您的人工智能助手。有什么我可以帮忙的吗？"
#             }
#         ]
#     }
#
#     # 询问开发者信息
#     template_developer = {
#         "conversation": [
#             {
#                 "system": "你是一个懂中文的小助手",
#                 "input": "你的开发者是谁",
#                 "output": f"我是由陈子安开发的。请问有什么可以帮助您的吗？"
#             }
#         ]
#     }
#
#     # 生成数据
#     for template in [template_greeting, template_identity, template_developer]:
#         conversations.extend([template] * repetitions)
#
#     # 尝试将数据写入JSON文件
#     try:
#         with open(filepath, 'w', encoding='utf-8') as file:
#             json.dump(conversations, file, ensure_ascii=False, indent=4)
#         print("数据已成功写入文件。")
#     except IOError as e:
#         print(f"文件写入错误: {e}")
#     except Exception as e:
#         print(f"发生了一个错误: {e}")
#
#
# # 用户配置部分
# name = '陈子安大模型'
# n = 1000
# file_path = 'data/conversations.json'
#
# # 确保目录存在
# os.makedirs(os.path.dirname(file_path), exist_ok=True)
#
# # 调用函数创建并保存数据
# create_conversation_data(name, n, file_path)
