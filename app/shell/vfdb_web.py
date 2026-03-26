import sys
import pandas as pd
import re

def process_column(cell):
    # 提取WP_开头的ID
    wp_id = re.search(r'WP_\w+', str(cell))
    wp_id = wp_id.group(0) if wp_id else ''
    
    # 提取VFG开头的ID，并转换为链接
    vfg_id = re.search(r'VFG\w+', str(cell))
    vfg_link = f'https://www.mgc.ac.cn/cgi-bin/VFs/gene.cgi?GeneID={vfg_id.group(0)}' if vfg_id else ''
    
    return wp_id, vfg_link

def main(input_file):
    # 读取TSV文件
    df = pd.read_csv(input_file, sep='\t')
    
    # 应用函数到第二列，并创建两个新列
    df[['genebank_ID', 'VF_Link']] = df.iloc[:, 1].apply(lambda x: process_column(x)).tolist()
    
    # 将修改后的数据写回同一个文件
    df.to_csv(input_file, sep='\t', index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    main(input_file)