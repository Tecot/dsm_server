import os
import csv
from Bio import SeqIO
from Bio.SeqUtils import GC
from django.conf import settings
from app.utils.get_files_from_dir import get_files_from_dir

def read_contigs_information_data(srp):

    contigs_path = os.path.join(settings.DATABASE_PATH, srp, settings.SRP_GENEOME_SEQ_FILE)
    sequences = SeqIO.parse(contigs_path, 'fasta')
    # cds_ids = get_cds_all_ids(srp)
    region_ids = get_region_all_ids(srp)
    resfinder_ids = get_resfinder_all_ids(srp)
    vfdb_ids = get_vfdb_all_ids(srp)
    combined_list = region_ids + resfinder_ids + vfdb_ids
    list_set = list(set(combined_list))
    contigs = []
    total = 0
    for seq_record in sequences:
        id = seq_record.id
        if id in list_set:
            total = total + 1
            contigs.append({
                'ID': seq_record.id,
                'Name': srp + '_' + seq_record.name,
                'Description': seq_record.description,
                'GC': round(GC(seq_record.seq), 3), 
                'Sequence': str(seq_record.seq),
                'Length': len(str(seq_record.seq))
            })
    header = [
        'Id', 
        'Name', 
        'Description', 
        'Length', 
        'GC', 
        'Sequence'
    ] 

    result = {
        'header': header,
        'data': contigs,
        'total': total
    }

    return result

# =====================================================判断函数


# 获取vfdb
def get_vfdb_all_ids(srp):
    vfdb_path = os.path.join(settings.DATABASE_PATH, srp, settings.SRP_VFDB_FILE)
    ids = []
    # 判断文件是否存在
    if not os.path.exists(vfdb_path):
        return ids
    # 判断文件是否为空白文件
    if not os.path.getsize(vfdb_path):
        return ids
    # 文件存在没判断是否有contig id对应的内容
    ids_set = set()
    with open(vfdb_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            ids_set.add(row[0])
    ids = list(ids_set)
    return ids

# 获取resfinder
def get_resfinder_all_ids(srp):
    resfinder_path = os.path.join(settings.DATABASE_PATH, srp, settings.SRP_RESFINDER_FILE)
    ids = []
    # 判断文件是否存在
    if not os.path.exists(resfinder_path):
        return ids
    # 判断文件是否为空白文件
    if not os.path.getsize(resfinder_path):
        return ids
    # 文件存在没判断是否有contig id对应的内容
    ids_set = set()
    with open(resfinder_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            ids_set.add(row[0])
    ids = list(ids_set)
    return ids

# 读取GBK cds区
def get_cds_all_ids(srp):
    gbk_path = os.path.join(settings.DATABASE_PATH, srp, srp + '.gbk')
    ids = []
    # 判断文件是否存在
    if not os.path.exists(gbk_path):
        return ids
    # 判断文件是否为空白文件
    if not os.path.getsize(gbk_path):
        return ids
    ids_set = set()
    with open(gbk_path, "r") as handle:
        for record in SeqIO.parse(handle, "genbank"):
            ids_set.add(record.id)
    ids = list(ids_set)
    return ids

def get_region_all_ids(srp):
    region_path = os.path.join(settings.DATABASE_PATH, srp, 'regions')
    all_files = get_files_from_dir(region_path)
    ids = []
    if not len(all_files):
        return ids
    ids_set = set()
    for file in all_files:
        if file.endswith('.gbk'):
            ids_set.add(file.split('.')[0])
    ids = list(ids_set)
    return ids