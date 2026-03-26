#!/bin/bash
# shellcheck disable=SC1091

out_dir=$1
user=$2
file=$3
env=$4


echo "Activating conda environment: dsm_biotools"
source "/data1/apps/software/Miniconda3/4.9.2/etc/profile.d/conda.sh"
conda activate "${env}"

mkdir "${out_dir}/${user}" 

seqtk seq -L 1000 "${file}" > "${out_dir}/${user}/${user}_1000.fa" 
quast "${out_dir}/${user}/${user}_1000.fa"  -o "${out_dir}/${user}" -t 20
