'''
File name: 
Author: Tecot (tyx_cqbs@163.com)
Version: V1.0
Date: 2024-12-11 13:31:06
Description: 
'''
'''
File name: 
Author: Tecot (tyx_cqbs@163.com)
Version: V1.0
Date: 2024-11-20 15:37:35
Description: 
'''
from django.http import JsonResponse
from datetime import datetime
from django.conf import settings
from app.models import TaskInfoModel

import os
from app.tasks.tasks import long_running_task

def analysis_service(request):
    try:
        now = datetime.now()
        str_timestamp = now.strftime("%Y_%m_%d__%H_%M_%S")
        key = 'mmd' + '-' + str_timestamp
        value = 'analysis'
        request.session[key] = value

        # 新建文件保存目录
        task_dir_path = os.path.join(settings.MEDIA_ROOT, key)
        if not os.path.exists(task_dir_path):
            os.mkdir(task_dir_path)

        # 保存文件
        fasta = request.FILES['fasta']
        fasta_name = f"{key}{os.path.splitext(fasta.name)[1]}"
        target1_data_path = os.path.join(settings.MEDIA_ROOT, key, fasta_name)
        with open(target1_data_path, 'wb+') as destination:
                for chunk in fasta.chunks():
                    destination.write(chunk)
        have_graph = request.POST['have_graph']
        if have_graph == 'true':  
            graph = request.FILES['graph'] 
            graph_name = f"{key}{os.path.splitext(graph.name)[1]}"
            target2_data_path = os.path.join(settings.MEDIA_ROOT, key, graph_name)
            with open(target2_data_path, 'wb+') as destination:
                    for chunk in graph.chunks():
                        destination.write(chunk)
        # 将key value 移交给数据库
        record = TaskInfoModel.objects.create(key=key, status=2)
        record.save()

        methods = request.POST['labels'].split(',')


        # 这里是计算任务(提交给celery做异步任务)
        long_running_task.delay(key, fasta_name, have_graph, methods)

        response = JsonResponse({
            'code': 0, 
            'data': {
                'key': key, 
                'value': value,
                'age': settings.SESSION_COOKIE_AGE
            } 
        })
        return response
    except Exception as e:
        return JsonResponse({ 'code': 0, 'msg': 'Error!' })
    
