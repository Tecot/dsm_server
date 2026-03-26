from django.conf import settings
from app.utils.get_files_from_dir import get_files_from_dir
import os

def read_download_list_data():
    
    files = get_files_from_dir(settings.DOWNLOAD_DATA_PATH)
    format_files = []
    for file in files:
        format_files.append({
            'file': file
        })
    
    result = {
        'data': format_files,
    }

    return result