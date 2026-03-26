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
from app.services.download.zip_utils import ZipUtils
from django.http import StreamingHttpResponse

class DownloadView(View):
    @staticmethod
    def get(request, srp):
        file_path = os.path.join(settings.DOWNLOAD_DATA_PATH, srp)
        response = StreamingHttpResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/zip'
        response['Content-Disposition'] = 'attachment; filename="large_file.zip"'
        return response