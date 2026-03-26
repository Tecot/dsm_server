#!/bin/bash

# Global configuration
declare -A software_paths
software_paths["bwa"]="bwa"
software_paths["samtools"]="samtools"
# Install on linux system
software_paths["seqGraph"]="/mnt/beegfs/user/linyu/3.software/seqGraph"
software_paths["quast"]="quast.py"
software_paths["metawrap"]="metawrap"
software_paths["gtdbtk"]="gtdbtk"
software_paths["antismash"]="antismash"
software_paths["macrel"]="macrel"
software_paths["blastn"]="blastn"

declare -A database_paths
database_paths["VFDB"]="/home/tecot/projects/dsm/dsm-server/datasets/VFDB"
database_paths["resfinder"]="/home/tecot/projects/dsm/dsm-server/datasets/resfinder"

declare -A conda_envs
conda_envs["bwa"]="dsm_biotools"
conda_envs["samtools"]="dsm_biotools"

conda_envs["quast"]="dsm_biotools"
conda_envs["metawrap"]="dsm_biotools"
conda_envs["gtdbtk"]="dsm_biotools"
conda_envs["antismash"]="dsm_antismash"
conda_envs["macrel"]="dsm_macrel"
conda_envs["blastn"]="dsm_biotools"

# Function to run a command and handle errors
run_command() {
    eval "$1"
    # shellcheck disable=SC2181
    if [ $? -ne 0 ]; then
        echo "An error occurred: $1"
        exit 1
    fi
}

# Function to setup conda environment
setup_environment() {
    # shellcheck disable=SC2063
    current_env=$(conda info --envs | grep '*' | awk '{print $1}')
    if [ "$current_env" != "$1" ]; then
        echo "Activating conda environment: $1"
        # shellcheck disable=SC1091
        source "$(conda info --base)/etc/profile.d/conda.sh"
        conda activate "$1"
    fi
}

# SeqGraph function
seqgraph() {
    out_dir=$1
    user=$2
    file1=$3
    file2=$4
    mkdir -p "${out_dir}/${user}/2.seqgraph"
    matching_cmd="${software_paths['seqGraph']}/build/matching -g ${file1} -r ${out_dir}/${user}/2.seqgraph/${user}.result -c ${out_dir}/${user}/2.seqgraph/${user}.cl --model 1 --verbose 1 -s"
    run_command "$matching_cmd"
    make_fa_cmd="${software_paths['make_fa']} ${file2} ${out_dir}/${user}/2.seqgraph/${user}.result ${out_dir}/${user}/2.seqgraph/${user}_dirty.fa"
    run_command "$make_fa_cmd"
    clean_cmd="${software_paths['clean']} ${out_dir}/${user}/2.seqgraph/${user}_dirty.fa ${out_dir}/${user}/2.seqgraph/${user}.fa"
    run_command "$clean_cmd"
    seqtk_cmd="seqtk seq -L 1000 ${out_dir}/${user}/2.seqgraph/${user}.fa > ${out_dir}/${user}/2.seqgraph/${user}_1000.fa"
    run_command "$seqtk_cmd"
}

# Quast function
quast() {
    out_dir=$1
    user=$2
    file=$3
    # setup_environment "${conda_envs['antismash']}"
    setup_environment "${conda_envs['quast']}"
    quast_cmd="${software_paths['quast']} ${file} -o ${out_dir}/${user}/3.quast -t 20"
    run_command "$quast_cmd"
}

# Bin function
binning() {
    out_dir=$1
    user=$2
    file=$3
    setup_environment "${conda_envs['metawrap']}"
    binning_cmd="${software_paths['metawrap']} binning -a ${file} -o ${out_dir}/${user}/4.binning -t 30 -m 100 --metabat2 --maxbin2 --concoct ${out_dir}/${user}/${user}_1.fastq ${out_dir}/${user}/${user}_2.fastq"
    run_command "$binning_cmd"
    ref_cmd="${software_paths['metawrap']} bin_refinement -o ${out_dir}/${user}/4.binning/BIN_REFINEMENT2 -t 30 -m 100 -A ${out_dir}/${user}/4.binning/metabat2_bins/ -B ${out_dir}/${user}/4.binning/maxbin2_bins/ -C ${out_dir}/${user}/4.binning/concoct_bins/ -c 50 -x 10"
    run_command "$ref_cmd"
}

# GTDB-Tk function
gtdbtk() {
    out_dir=$1
    user=$2
    setup_environment "${conda_envs['gtdbtk']}"
    if [ -d "${out_dir}/${user}/4.binning/BIN_REFINEMENT2/metawrap_50_10_bins/" ]; then
        gtdbtk_cmd="${software_paths['gtdbtk']} classify_wf --genome_dir ${out_dir}/${user}/4.binning/BIN_REFINEMENT2/metawrap_50_10_bins/ --out_dir ${out_dir}/${user}/5.gtdbtk/ --cpus 20 --extension fa"
        run_command "$gtdbtk_cmd"
        cat_gtdbtk="python ${software_paths['seqGraph']}/scripts/cat_gtdbtk.py ${out_dir}/${user}/"
        run_command "$cat_gtdbtk"
    fi
}
# Antismash function
antismash() {
    out_dir=$1
    user=$2
    file=$3
    setup_environment "${conda_envs['antismash']}"
    antismash_cmd="${software_paths['antismash']} -i ${file} -o ${out_dir}/${user}/6.antismash"
    run_command "$antismash_cmd"
}

# Vf and Res function
v_r_gene() {
    out_dir=$1
    user=$2
    file=$3

    local header="qseqid\tsseqid\tpident\tlength\tmismatch\tgapopen\tqstart\tqend\tsstart\tsend\tevalue\tbitscore\tstitle\tqlen\tslen\tqcovs\tqseq\tsseq"
    echo -e "${header}" > "${out_dir}/${user}/7.vfdb.txt"
    echo -e "${header}" > "${out_dir}/${user}/7.resfinder.txt"

    local vfdb_blast_cmd="${software_paths['blastn']} -db ${database_paths['VFDB']} -query ${file} -out ${out_dir}/${user}/7.vfdb_ing.tab -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle qlen slen qcovs qseq sseq' -num_threads 10 -max_target_seqs 5"
    run_command "$vfdb_blast_cmd"

    local resfinder_blast_cmd="${software_paths['blastn']} -db ${database_paths['resfinder']} -query ${file} -out ${out_dir}/${user}/7.resfinder_ing.tab -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle qlen slen qcovs qseq sseq' -num_threads 10 -max_target_seqs 5"
    run_command "$resfinder_blast_cmd"

    cat "${out_dir}/${user}/7.vfdb_ing.tab" >> "${out_dir}/${user}/7.vfdb.txt"
    cat "${out_dir}/${user}/7.resfinder_ing.tab" >> "${out_dir}/${user}/7.resfinder.txt"

    rm "${out_dir}/${user}/7.vfdb_ing.tab"
    rm "${out_dir}/${user}/7.resfinder_ing.tab"

    python ${software_paths['vfdb']}/vfdb_web.py "${out_dir}/${user}/7.vfdb.txt"
}

# Macrel function
macrel() {
    out_dir=$1
    user=$2
    file=$3
    setup_environment "${conda_envs['macrel']}"
    macrel_cmd="${software_paths['macrel']} -i ${file} -o ${out_dir}/${user}/8.macrel"
    run_command "$macrel_cmd"
}

# Main script execution
if [ $# -ne 4 ]; then
    echo "Usage: bash all.sh <out_dir> <user> <file> <task>"
    exit 1
fi

out_dir=$1
user=$2
file=$3
task=$4

case "$task" in
    "data")
        # file1用ERP115675.graph
        # file1用ERP115675.fa
        seqgraph "$out_dir" "$user" "$file1" "$file2"
        file="${out_dir}/${user}/2.seqgraph/${user}_1000.fa"
        quast "$out_dir" "$user" "$file"
        ;;
    # "binning")
    #     binning "$out_dir" "$user" "$file"
    #     gtdbtk "$out_dir" "$user"
    #     ;;
    "second")
        # file用ERP115675.fa
        # file用data步生成的ERP115675_1000.fa也跑一遍
        antismash "$out_dir" "$user" "$file"
        ;;
    "vf"|"res")
        # file用ERP115675.fa
        # file用data步生成的ERP115675_1000.fa也跑一遍
        v_r_gene "$out_dir" "$user" "$file"
        ;;
    "macrel")
        # file用ERP115675.fa
        # file用data步生成的ERP115675_1000.fa也跑一遍
        macrel "$out_dir" "$user" "$file"
        ;;
    *)
        echo "Invalid task: $task"
        exit 1
        ;;
esac