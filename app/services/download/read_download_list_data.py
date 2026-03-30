from django.conf import settings
from app.utils.get_files_from_dir import get_files_from_dir
from app.utils.format_size import format_size
import os

def read_download_list_data():
    
    files = get_files_from_dir(settings.DOWNLOAD_DATA_PATH)
    format_files = []
    for file in files:
        format_files.append({
            'file': file,
            'size': format_size(os.path.getsize(os.path.join(settings.DOWNLOAD_DATA_PATH, file)))
        })
    result = {
        'data': format_files,
    }

    return result