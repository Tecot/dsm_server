import os
from Bio import SeqIO

# 读取GBK cds区
def read_cds_data():
    result = [0, {'meta': []}]
    with open('/home/tecot/projects/dsm/dsm-server/workspace/DRP005856/DRP005856_1000.gbk', "r") as handle:
        print('---')
        for record in SeqIO.parse(handle, "genbank"):
            id = record.id
            print(id)
    return result


print(read_cds_data())