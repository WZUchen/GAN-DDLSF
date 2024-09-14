import os
from mp_api.client import MPRester
from pymatgen.io.cif import CifWriter
import concurrent.futures


def get_api_key():
    # 从用户输入获取API密钥
    return input("请输入您的API密钥：")


def search_materials(mpr, num_elements_range, num_sites_range, volume_range):
    """
    使用MPRester搜索材料属性。

    :param mpr: MPRester对象，用于API请求
    :param num_elements_range: tuple - 元素数量范围
    :param num_sites_range: tuple - 晶体数量范围
    :param volume_range: tuple - 晶格体积范围
    :return: 搜索结果列表
    """
    try:
        return mpr.summary.search(
            num_elements=num_elements_range,
            num_sites=num_sites_range,
            volume=volume_range
        )
    except Exception as e:
        print("搜索时发生错误：", e)
        return []


def write_cif_file(mpr, material_id, formula, directory):
    """
    获取指定材料的结构并写入CIF文件。

    :param mpr: MPRester对象，用于API请求
    :param material_id: str - 材料ID
    :param formula: str - 化学式
    :param directory: str - 文件保存目录
    """
    try:
        structure = mpr.get_structure_by_material_id(material_id=material_id)
        cif_writer = CifWriter(structure)
        cif_writer.write_file(f"{directory}/{material_id}-{formula}.cif")
    except Exception as e:
        print(f"处理材料 {material_id} 时发生错误：", e)


def main():
    api_key = get_api_key()
    directory = "../data/preprocess_data/binary_compound_Database"
    # 创建目录，如果目录已存在，则不会抛出错误
    os.makedirs(directory, exist_ok=True)
    num_elements_range = (2, 2)
    num_sites_range = (1, 20)
    volume_range = (0, 1000)

    with MPRester(api_key=api_key) as mpr:
        docs = search_materials(mpr, num_elements_range, num_sites_range, volume_range)
        material_ids = [doc.material_id for doc in docs]
        material_formulas = [doc.formula_pretty for doc in docs]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for material_id, formula in zip(material_ids, material_formulas):
                executor.submit(write_cif_file, mpr, material_id, formula, directory)


if __name__ == "__main__":
    main()
