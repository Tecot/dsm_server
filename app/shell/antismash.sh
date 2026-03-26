#!/bin/bash
# shellcheck disable=SC1091
# shellcheck disable=SC1009
# shellcheck disable=SC1073
# shellcheck disable=SC1072

# 输出目录
out_dir=$1
# 输出的子目录
user=$2
# .fasta文件
file=$3
# conda环境
env=$4

echo "Activating conda environment: dsm_antismash"
source "/data1/apps/software/Miniconda3/4.9.2/etc/profile.d/conda.sh"
conda activate "${env}"

antismash --genefinding-tool prodigal --output-dir "${out_dir}/${user}" "${file}"  
