import os
import pandas as pd


BASE_DIR = '/data3/platform/marine/rawdata/perfect'

def get_all_dirs_from_dir(path):
    subfolders = []
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir():
                subfolders.append(entry.name)
    return subfolders

def dothis():   
    dirs = get_all_dirs_from_dir(BASE_DIR)

    dicts = []
    for item in dirs:
        annotation_file = True
        final_contigs_faa = True
        gtdbtk_summary = True
        metawrap_50_10_contigs = True
        metawrap_50_10_stats = True
        resfinder_tab = True
        combined = True
        gbk = True
        tsv = True
        vfdb = True
        all_path = os.path.join(BASE_DIR, item)
        if not os.path.exists(os.path.join(all_path, 'annotation', item + '.faa')):
            annotation_file = False
        if not os.path.exists(os.path.join(all_path, 'final.contigs.fa')):
            final_contigs_faa = False
        if not os.path.exists(os.path.join(all_path, 'gtdbtk.summary.tsv')):
            gtdbtk_summary = False
        # if not os.path.exists(os.path.join(all_path, 'gtdbtk.summary.tsv')):
        #     gtdbtk_summary = False
        if not os.path.exists(os.path.join(all_path, 'metawrap_50_10_bins.contigs')):
            metawrap_50_10_contigs = False
        if not os.path.exists(os.path.join(all_path, 'metawrap_50_10_bins.stats')):
            metawrap_50_10_stats = False
        if not os.path.exists(os.path.join(all_path, 'resfinder.tab')):
            resfinder_tab = False
        if not os.path.exists(os.path.join(all_path, item + '_combined.csv')):
            combined = False
        if not os.path.exists(os.path.join(all_path, item + '.gbk')):
            gbk = False
        if not os.path.exists(os.path.join(all_path, item + '.tsv')):
            tsv = False
        if not os.path.exists(os.path.join(all_path, 'vfdb.tab')):
            vfdb = False
        
        dicts.append({
            'file': item,
            'annotation_file': annotation_file,
            'final_contigs_faa': final_contigs_faa,
            'gtdbtk_summary': gtdbtk_summary,
            'metawrap_50_10_contigs': metawrap_50_10_contigs,
            'metawrap_50_10_stats': metawrap_50_10_stats,
            'resfinder_tab': resfinder_tab,
            'combined': combined,
            'gbk': gbk,
            'tsv': tsv,
            'vfdb': vfdb
        })
        
    df = pd.DataFrame(dicts)
    df.to_csv('perfect_check.csv', index=False)

if __name__ == "__main__":
    dothis()