'''
File name: 
Author: Tecot (tyx_cqbs@163.com)
Version: V1.0
Date: 2024-12-23 10:54:32
Description: 
'''
import os
from django.http import FileResponse
from django.views import View
from django.conf import settings
from wsgiref.util import FileWrapper

class DownloadView(View):
    @staticmethod
    def get(request, srp):
        print(f"Received download request for: {srp}")
        file_path = os.path.join(settings.DOWNLOAD_DATA_PATH, srp)
        response = FileResponse(
            FileWrapper(open(file_path, 'rb'), 8192),  # 8KB分块传输
            content_type='application/zip'
        )
        response['Content-Disposition'] = f'attachment; filename="{srp}"'
        return response