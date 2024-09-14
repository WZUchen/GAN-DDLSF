import pandas as pd

def remove_non_converged_rows(csv_file):
    """
    从CSV文件中删除Convergence列为NO的行。
    """
    df = pd.read_csv(csv_file)

    # 只保留Convergence列不为'NO'的行
    df_converged = df[df['Convergence'] != 'NO']

    # 将结果保存回CSV文件
    df_converged.to_csv(csv_file, index=False)

def main():
    csv_file = 'extracted_data.csv'  # CSV文件路径
    remove_non_converged_rows(csv_file)

if __name__ == "__main__":
    main()
