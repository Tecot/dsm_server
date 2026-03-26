'''
File name: 
Author: Tecot (tyx_cqbs@163.com)
Version: V1.0
Date: 2024-11-21 15:07:35
Description: 
'''
from celery import shared_task
import subprocess
import os
from django.conf import settings
from app.models import TaskInfoModel

@shared_task
def long_running_task(key, fasta_name, have_graph, methods):
    task_dir = os.path.join(settings.MEDIA_ROOT, key)
    fasta_path = os.path.join(settings.MEDIA_ROOT, key, fasta_name)
    flag = 1
    for method in methods:
        if method == 'vfdb_resfinder':
            vfdb_resfinder_env_path = os.path.join(settings.ENVS_CONFIG['base'], settings.ENVS_CONFIG['name']['dsm_biotools'])
            vfdb_resfinder_shell_path = os.path.join(settings.BASE_DIR, 'app', 'shell', 'v_r_gene.sh')
            vfdb_resfinder_argments = [task_dir, 'vfdb_resfinder', fasta_path, settings.EXTERNAL_RESFINDER_PATH, settings.EXTERNAL_VFDB_PATH, settings.EXTERNAL_VFDB_WEB_PATH, vfdb_resfinder_env_path]
            vfdb_resfinder_result = subprocess.run([vfdb_resfinder_shell_path] + vfdb_resfinder_argments, shell=False)
            try:
                if vfdb_resfinder_result.returncode == 0:
                    task = TaskInfoModel.objects.get(key=key)
                    if flag < len(methods):
                        task.status = 2
                        task.save()
                    else:
                        task.status = 0
                        task.save()
                else:
                    task = TaskInfoModel.objects.get(key=key)
                    task.status = 1 # 流程程序出错
                    task.save()
                    return f"Task {key} faild."
            except Exception as e:
                task = TaskInfoModel.objects.get(key=key)
                task.status = 1 # 流程程序出错
                task.save()
                return f"Task {key} faild."
            
        if method == 'secondary':
            secondary_env_path = os.path.join(settings.ENVS_CONFIG['base'], settings.ENVS_CONFIG['name']['dsm_antismash'])
            secondary_shell_path = os.path.join(settings.BASE_DIR, 'app', 'shell', 'antismash.sh')
            secondary_argments = [task_dir, 'secondary', fasta_path, secondary_env_path]
            secondary_result = subprocess.run([secondary_shell_path] + secondary_argments, shell=False)
            try:
                if secondary_result.returncode == 0:
                    task = TaskInfoModel.objects.get(key=key)
                    if flag < len(methods):
                        task.status = 2
                        task.save()
                    else:
                        task.status = 0
                        task.save()
                else:
                    task = TaskInfoModel.objects.get(key=key)
                    task.status = 1 # 流程程序出错
                    task.save()
                    return f"Task {key} faild."
            except Exception as e:
                task = TaskInfoModel.objects.get(key=key)
                task.status = 1 # 流程程序出错
                task.save()
                return f"Task {key} faild."
            
        if method == 'macrel':
            macrel_env_path = os.path.join(settings.ENVS_CONFIG['base'], settings.ENVS_CONFIG['name']['dsm_macrel'])
            macrel_shell_path = os.path.join(settings.BASE_DIR, 'app', 'shell', 'macrel.sh')
            macrel_argments = [task_dir, 'macrel', fasta_path, macrel_env_path]
            macrel_result = subprocess.run([macrel_shell_path] + macrel_argments, shell=False)
            try:
                if macrel_result.returncode == 0:
                    task = TaskInfoModel.objects.get(key=key)
                    if flag < len(methods):
                        task.status = 2
                        task.save()
                    else:
                        task.status = 0
                        task.save()
                else:
                    task = TaskInfoModel.objects.get(key=key)
                    task.status = 1 # 流程程序出错
                    task.save()
                    return f"Task {key} faild."
            except Exception as e:
                print(e)
                task = TaskInfoModel.objects.get(key=key)
                task.status = 1 # 流程程序出错
                task.save()
                return f"Task {key} faild."
            
        if method == 'seqgraph':
            seqgraph_env_path = os.path.join(settings.ENVS_CONFIG['base'], settings.ENVS_CONFIG['name']['dsm_biotools'])
            if have_graph == 'false':
                seqgraph_shell_path = os.path.join(settings.BASE_DIR, 'app', 'shell', 'seqtk_quast.sh')
                seqgraph_argments = [task_dir, 'seqgraph', fasta_path, seqgraph_env_path]
                seqgraph_result = subprocess.run([seqgraph_shell_path] + seqgraph_argments, shell=False)
                try:
                    if seqgraph_result.returncode == 0:
                        task = TaskInfoModel.objects.get(key=key)
                        if flag < len(methods):
                            task.status = 2
                            task.save()
                        else:
                            task.status = 0
                            task.save()
                    else:
                        task = TaskInfoModel.objects.get(key=key)
                        task.status = 1 # 流程程序出错
                        task.save()
                        return f"Task {key} faild."
                except Exception as e:
                    task = TaskInfoModel.objects.get(key=key)
                    task.status = 1 # 流程程序出错
                    task.save()
                    return f"Task {key} faild."
            else:
                graph_path = os.path.join(task_dir, key + '.graph')
                seqgraph_shell_path = os.path.join(settings.BASE_DIR, 'app', 'shell', 'seqgraph.sh')
                seqgraph_argments = [settings.SEQGRAPH_SOFTWARE_PATH, task_dir, 'seqgraph', graph_path, fasta_path, seqgraph_env_path]
                seqgraph_result = subprocess.run([seqgraph_shell_path] + seqgraph_argments, shell=False)
                try:
                    if seqgraph_result.returncode == 0:
                        task = TaskInfoModel.objects.get(key=key)
                        if flag < len(methods):
                            task.status = 2
                            task.save()
                        else:
                            task.status = 0
                            task.save()
                    else:
                        task = TaskInfoModel.objects.get(key=key)
                        task.status = 1 # 流程程序出错
                        task.save()
                        return f"Task {key} faild."
                except Exception as e:
                    task = TaskInfoModel.objects.get(key=key)
                    task.status = 1 # 流程程序出错
                    task.save()
                    return f"Task {key} faild."
        flag = flag + 1
    return f"Task {key} with analysis completed."