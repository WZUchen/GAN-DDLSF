import pandas as pd
import re

def count_elements(formula, element):
    """
    在化学式中计算指定元素的数量。
    """
    matches = re.findall(f'{element}(\d*)', formula)
    count = sum(int(m) if m else 1 for m in matches)
    return count

def update_csv_with_element_count(csv_file):
    """
    更新CSV文件，统计Ga和N的数量，并追加为新列。
    """
    df = pd.read_csv(csv_file)

    df['Ga_count'] = df['Formula'].apply(lambda x: count_elements(x, 'Ga'))
    df['N_count'] = df['Formula'].apply(lambda x: count_elements(x, 'N'))

    df.to_csv(csv_file, index=False)

def main():
    csv_file = 'extracted_data.csv'  # CSV文件路径
    update_csv_with_element_count(csv_file)

if __name__ == "__main__":
    main()
