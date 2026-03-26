#!/bin/bash
# shellcheck disable=SC2086
# shellcheck disable=SC2154
# shellcheck disable=SC1091

# seqGraph软件路径
seqGraph_path=$1  
# 输出目录
out_dir=$2
# 输出目录下的子目录
user=$3
# .graph文件
g_file=$4
# .fasta文件
file=$5
# conda
env=$6

echo "Activating conda environment: dsm_biotools"
source "/data1/apps/software/Miniconda3/4.9.2/etc/profile.d/conda.sh"
conda activate "${env}"


mkdir -p "${out_dir}/${user}"

"${seqGraph_path}/build/matching" -g "${g_file}" -r "${out_dir}/${user}/${user}.result" -c "${out_dir}/${user}/${user}.cl" --model 1 --verbose 1 -s

python "${seqGraph_path}/make_fa.py" "${file}" "${out_dir}/${user}/${user}.result" "${out_dir}/${user}/${user}_dirty.fa"

python "${seqGraph_path}/scripts/clean.py" "${out_dir}/${user}/${user}_dirty.fa" "${out_dir}/${user}/${user}.fa"

