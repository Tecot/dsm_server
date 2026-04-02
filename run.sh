#!/bin/bash
###
 # @File name: 
 # @Author: Tecot (tyx_cqbs@163.com)
 # @Version: V1.0
 # @Date: 2024-12-24 10:14:45
 # @Description: 
### 

# shellcheck disable=SC1091
# source "/data1/apps/software/Miniconda3/4.9.2/etc/profile.d/conda.sh"
# conda activate "/data3/platform/marine/envs/dsm"

. /data1/apps/software/Miniconda3/4.9.2/etc/profile.d/conda.sh
source activate /data3/platform/marine/envs/dsm

# celery -A server worker --loglevel=info & 
python manage.py runserver 8173
