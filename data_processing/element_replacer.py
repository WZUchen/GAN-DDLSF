import os
from tqdm import tqdm
from pymatgen.core import Composition, Element
from pymatgen.io.cif import CifParser, CifWriter


def replace_elements_in_structure(structure, original_elements, replacement_elements):
    """根据提供的顺序替换结构中的特定元素"""
    if len(original_elements) != len(replacement_elements):
        raise ValueError("The number of original elements and replacement elements must be the same.")

    # 创建一个映射，将原始元素映射到相应的替换元素
    replacement_map = dict(zip(original_elements, replacement_elements))

    for idx, species in enumerate(structure.species):
        if species.symbol in replacement_map:
            structure.replace(idx, Element(replacement_map[species.symbol]))



def get_chemical_formula(structure):
    """获取晶体结构的化学式"""
    return structure.composition.reduced_formula


def process_cif_file(filepath, replacement_elements, target_folder):
    """处理单个CIF文件"""
    try:
        cif_parser = CifParser(filepath)
        structure = cif_parser.get_structures(primitive=False)[0]

        original_elements = list(structure.symbol_set)
        if len(original_elements) != len(replacement_elements):
            raise ValueError(f"File {filepath} does not match the number of replacement elements.")

        replace_elements_in_structure(structure, original_elements, replacement_elements)

        new_formula = get_chemical_formula(structure)
        target_filename = f"{os.path.basename(filepath)[:-4]}-{new_formula}.cif"
        target_filepath = os.path.join(target_folder, target_filename)

        cif_writer = CifWriter(structure)
        cif_writer.write_file(target_filepath)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def get_replacement_elements():
    """获取用户输入的替换元素"""
    element1 = input("Enter the replacement element 1: ")
    element2 = input("Enter the replacement element 2: ")
    return element1, element2


# 主逻辑
def main():
    original_folder = "../data/preprocess_data/binary_compound_Database/"
    target_folder = "../zc/preprocess_data/replace_compound_Database/"
    os.makedirs(target_folder, exist_ok=True)

    replacement_elements = get_replacement_elements()

    cif_files = [f for f in os.listdir(original_folder) if f.endswith(".cif")]

    for filename in tqdm(cif_files, desc="Processing CIF files"):
        original_filepath = os.path.join(original_folder, filename)
        process_cif_file(original_filepath, replacement_elements, target_folder)

if __name__ == "__main__":
    main()
