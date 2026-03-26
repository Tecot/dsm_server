#!/bin/bash
# shellcheck disable=SC1091
# shellcheck disable=SC2168
# shellcheck disable=SC1009

# 输出目录
out_dir=$1
# 输出子目录
user=$2
# .fasta文件
file=$3
# resfinder db path
resfinder_db=$4
# vfdb db path
vfdb_db=$5
# vfdb_web.py文件路径
vfdb_web_file_path=$6
# conda
env=$7

echo "Activating conda environment: dsm_biotools"
source "/data1/apps/software/Miniconda3/4.9.2/etc/profile.d/conda.sh"
conda activate "${env}"

mkdir "${out_dir}/${user}"

local header="qseqid\tsseqid\tpident\tlength\tmismatch\tgapopen\tqstart\tqend\tsstart\tsend\tevalue\tbitscore\tstitle\tqlen\tslen\tqcovs\tqseq\tsseq"
echo -e "${header}" > "${out_dir}/${user}/vfdb.txt"
echo -e "${header}" > "${out_dir}/${user}/resfinder.txt"

blastn -db "${resfinder_db}" -query "${file}" -out "${out_dir}/${user}/resfinder_ing.tab" -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle qlen slen qcovs qseq sseq" -num_threads 10 -max_target_seqs 5
blastn -db "${vfdb_db}" -query "${file}" -out "${out_dir}/${user}/vfdb_ing.tab" -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle qlen slen qcovs qseq sseq" -num_threads 10 -max_target_seqs 5

cat "${out_dir}/${user}/vfdb_ing.tab" >> "${out_dir}/${user}/vfdb.txt"
cat "${out_dir}/${user}/resfinder_ing.tab" >> "${out_dir}/${user}/resfinder.txt"

rm "${out_dir}/${user}/vfdb_ing.tab"
rm "${out_dir}/${user}/resfinder_ing.tab"

python "${vfdb_web_file_path}" "${out_dir}/${user}/vfdb.txt"
