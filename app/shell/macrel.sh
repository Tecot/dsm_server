#!/bin/bash
# shellcheck disable=SC1091

# 输出目录
out_dir=$1
# 输出目录的子目录
user=$2
# .fasta文件（contigs）
file=$3
# conda
env=$4

echo "Activating conda environment: dsm_macrel"
source "/data1/apps/software/Miniconda3/4.9.2/etc/profile.d/conda.sh"
conda activate "${env}"

macrel contigs --fasta "${file}" --output "${out_dir}/${user}"
